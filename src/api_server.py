from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import logging
import threading
import os
import sys
if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

load_dotenv()
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

client = MongoClient("mongodb://mongodb.python-mongodb:27017/")
db = client['broncos']
customers_collection = db['customers']
items_collection = db['items']

producer = KafkaProducer(bootstrap_servers='kafka:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def consume_messages():
    consumer = KafkaConsumer('purchases',
                         bootstrap_servers='kafka:9092',
                         auto_offset_reset='earliest',
                         group_id='purchase-group',
                         value_deserializer=lambda x: json.loads(x.decode('utf-8'))) 
    logging.info("Consumer started. Listening for messages...")   
    for message in consumer:
        purchase_data = message.value
        username = purchase_data['username']
        item = purchase_data['item']
        logging.info(f"Received purchase: {username} purchased {item}")
        customers_collection.update_one(
            {'username': username},
            {'$inc': {item: 1}}
        )

threading.Thread(target=consume_messages, daemon=True).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']     
        customer = customers_collection.find_one({'username': username})
        if customer:
            if customer['password'] == password:
                session['username'] = username
                return jsonify({"success": True}), 200
            elif customer:
                return jsonify({"success": False, "error": "🏈 Wrong Password! 🏈"}), 401
            return render_template('login.html', loginError="🏈 Wrong Password! 🏈") # Remove later
        else:
            customers_collection.insert_one({'username': username, 'password': password, 'blue': 0, 'orange': 0, 'white': 0})
            session['username'] = username
            return jsonify({"success": True}), 200
    return render_template('login.html') # remove later

@app.route('/items', methods=['GET', 'POST'])
def items():
    username = session.get('username', 'Guest')
    if request.method == 'POST':
        item_name = request.json.get('item_name')
        username = request.json.get('username')
        if username:
            producer.send('purchases', {'username': username, 'item': item_name})
            return jsonify({"message": "Item purchased successfully."}), 201
        return jsonify({"error": "User not logged in."}), 403
    items = list(items_collection.find({}, {'_id': 0}))
    return jsonify(items)

'''
@app.route('/cart', methods=['GET', 'POST'])
def get_all_bought_items():
    username = session.get('username', 'Guest')
    if request.method == 'GET':
        customer = customers_collection.find_one({'username': username})
        cart_items = []
        total_price = 0
        if customer:
            for item_name in customer:
                if item_name not in ['_id', 'username', 'password']:
                    item = items_collection.find_one({'item': item_name})
                    if item:
                        quantity = customer[item_name]
                        cart_items.append({
                            'item': item['item'],
                            'image': item['image'],
                            'price': item['price'],
                            'quantity': quantity
                        })
        total_price = sum(item['price'] * item['quantity'] for item in cart_items)
        return jsonify({
            'cart_items': cart_items,
            'total_price': total_price
        })
'''
@app.route('/cart', methods=['GET', 'POST'])
def get_all_bought_items():
    username = session.get('username', 'Guest')
    if request.method == 'POST':
        item_name = request.json.get('item_name')
        username = request.json.get('username')
        if username:
            producer.send('purchases', {'username': username, 'item': item_name})
            return jsonify({"message": "Item purchased successfully."}), 201
        return jsonify({"error": "User not logged in."}), 403
    items = list(items_collection.find({}, {'_id': 0}))
    return jsonify(items)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)