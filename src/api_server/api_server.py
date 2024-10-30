from flask import Flask, request, jsonify
from pymongo import MongoClient
from kafka import KafkaConsumer, KafkaProducer
import threading

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['purchase_db']
collection = db['purchases']

producer = KafkaProducer(bootstrap_servers='localhost:9092')
consumer = KafkaConsumer('purchases',
                         bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         group_id='purchase-group')

def consume_messages():
    for message in consumer:
        purchase = message.value
        collection.insert_one(purchase)

threading.Thread(target=consume_messages, daemon=True).start()

@app.route('/buy', methods=['POST'])
def buy_item():
    data = request.json
    producer.send('purchases', data)
    return jsonify({"message": "Item purchased successfully."}), 201

@app.route('/getAllBoughtItems', methods=['GET'])
def get_all_bought_items():
    items = list(collection.find({}, {'_id': 0}))
    return jsonify(items), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)