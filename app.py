import requests
import hmac
import hashlib
from decimal import Decimal

from flask import Flask, render_template, jsonify, request


app = Flask(__name__)


@app.route('/')
def index():
    shop_items = [
        {
            'name': 'Shoe',
            'price': '20.99',
            'image': {
                'link': '/static/img/shoe.webp',
                'alt': 'Shoe image'
            }
        },
        {
            'name': 'T-Shirt',
            'price': '14.99',
            'image': {
                'link': '/static/img/tshirt.webp',
                'alt': 'T-Shirt image'
            }
        },
        {
            'name': 'Cap',
            'price': '5.99',
            'image': {
                'link': '/static/img/cap.jpg',
                'alt': 'Cap image'
            }
        },
        {
            'name': 'Jeans',
            'price': '18.99',
            'image': {
                'link': '/static/img/jeans.jpg',
                'alt': 'Jeans image'
            }
        },
        {
            'name': 'Raspberry PI 4',
            'price': '54.99',
            'image': {
                'link': '/static/img/pi4.png',
                'alt': 'PI 4 image'
            }
        },
        {
            'name': 'RAM DDR4 8GB',
            'price': '65.99',
            'image': {
                'link': '/static/img/ram.png',
                'alt': 'RAM image'
            }
        },
        {
            'name': 'PinePhone',
            'price': '199.99',
            'image': {
                'link': '/static/img/pinephone.png',
                'alt': 'Pinephone Image'
            }
        }
    ]
    return render_template('index.html', shop_items=shop_items)


@app.route('/create-form', methods=['POST'])
def create_form():
    data = {
        'amount_requested': int(Decimal(request.json['item_price']) * 100),
        'fiat_currency': 'USD',
        'project_id': 'd489c31e-8a93-40f1-95c6-7eca8622901e',
        'api_key': 'NL12-CxRtDOh5JycnBlhFIoOfbCLGF7kug5oZFDCRv0'
    }
    res = requests.post(
        'https://gatewayprocessorapi.ekata.io/api/v1/payment-form/create',
        json=data)
    return jsonify({'form_id': res.json()['id']})


@app.route('/payment-success', methods=['POST'])
def payment_success():
    print(request.json)
    message = f"{request.json['payment_id']}" + \
              f"{request.json['wallet_address']}" + \
        f"{request.json['amount_received']}"
    signature = hmac.new(
        "lxvD4Aiv9ozxePVsUNoNLTKiS24RdlpMkZJW6pbz8Rs".encode(),
        message.encode(),
        hashlib.sha256).hexdigest()
    if signature == request.json['signature']:
        print("signature matched, we can ship")
    return "success"


@app.route('/success')
def success():
    return render_template("success.html")


@app.route('/payment-webhook', methods=['POST'])
def payment_webhook():
    print(request.json)
    message = f"{request.json['payment_id']}" + \
              f"{request.json['wallet_address']}" + \
        f"{request.json['amount_received']}"
    signature = hmac.new(
        "lxvD4Aiv9ozxePVsUNoNLTKiS24RdlpMkZJW6pbz8Rs".encode(),
        message.encode(),
        hashlib.sha256).hexdigest()
    if signature == request.json['signature']:
        print("signature matched, we can ship")
    return "success"
