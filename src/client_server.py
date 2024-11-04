from flask import Flask, request, render_template, redirect, url_for, session
from flask_cors import CORS
from kafka import KafkaProducer
from dotenv import load_dotenv
import json
import requests
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

API_SERVER_URL = 'http://192.168.49.2:30001' # minikube ip

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{API_SERVER_URL}/', data={'username': username, 'password': password})
        if response.status_code == 200:
            session['username'] = username
            return redirect(url_for('items'))
        else:
            return render_template('login.html', loginError=response.json().get('error', 'Login failed.'))   
    return render_template('login.html')

@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        username = session.get('username', 'Guest')
        item_name = request.json.get('item_name')
        if not username:
            return {"error": "User not logged in."}, 403
        response = requests.post(f'{API_SERVER_URL}/items', json={'item_name': item_name, 'username': username})   
        if response.status_code == 201:
            return {"message": "Item purchased successfully."}, 201
        return {"error": "Failed to purchase item."}, 400
    response = requests.get(f'{API_SERVER_URL}/items')
    if response.status_code == 200:
        return render_template('items.html', items=response.json(), username=session.get('username'))
    return "Error fetching items"
'''
@app.route('/cart', methods=['GET'])
def get_all_bought_items():
    username = session.get('username', 'Guest')
    response = requests.get(f'{API_SERVER_URL}/cart')
    cart_items = response.json()
    return render_template('cart.html', username=username, cart_items=cart_items['cart_items'], total_price=cart_items['total_price'])
'''
@app.route('/cart', methods=['GET'])
def get_all_bought_items():
    if request.method == 'POST':
        username = session.get('username', 'Guest')
        item_name = request.json.get('item_name')
        if not username:
            return {"error": "User not logged in."}, 403
        response = requests.post(f'{API_SERVER_URL}/cart', json={'item_name': item_name, 'username': username})   
        if response.status_code == 201:
            return {"message": "Item purchased successfully."}, 201
        return {"error": "Failed to purchase item."}, 400
    response = requests.get(f'{API_SERVER_URL}/cart')
    if response.status_code == 200:
        return render_template('cart.html', items=response.json(), username=session.get('username'))
    return "Error fetching items"

@app.route('/logout', methods=['POST'])
def logout():
    requests.post(f'{API_SERVER_URL}/logout')
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
