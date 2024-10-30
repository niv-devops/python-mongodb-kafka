from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_SERVER_URL = 'http://localhost:5000'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buy', methods=['POST'])
def buy():
    item = request.form['item']
    response = requests.post(f'{API_SERVER_URL}/buy', json={'item': item})
    return response.json()

@app.route('/getAllBoughtItems', methods=['GET'])
def get_all_bought_items():
    response = requests.get(f'{API_SERVER_URL}/getAllBoughtItems')
    return response.json()

if __name__ == '__main__':
    app.run(debug=True, port=5001)
