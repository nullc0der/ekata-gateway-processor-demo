import os
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
    return render_template(
        'index.html',
        shop_items=shop_items,
        api_key=os.environ.get("GATEWAY_PROCESSOR_PROJECT_ID"),
        form_url=os.environ.get("GATEWAY_PROCESSOR_FORM_URL"))


@app.route('/create-form', methods=['POST'])
def create_form():
    data = {
        'amount_requested': int(Decimal(request.json['item_price']) * 100),
        'fiat_currency': 'USD',
        'project_id': os.environ.get("GATEWAY_PROCESSOR_PROJECT_ID"),
        'api_key': os.environ.get("GATEWAY_PROCESSOR_PROJECT_API_KEY")
    }
    res = requests.post(
        f'{os.environ.get("GATEWAY_PROCESSOR_API_URL")}/payment-form/create',
        json=data)
    return jsonify({'form_id': res.json()['id']})


@app.route('/payment-success', methods=['POST'])
def payment_success():
    print(request.json)
    message = f"{request.json['payment_id']}" + \
              f"{request.json['wallet_address']}" + \
        f"{request.json['amount_received']}"
    signature = hmac.new(
        os.environ.get("GATEWAY_PROCESSOR_PROJECT_API_SECRET").encode(),
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
        os.environ.get("GATEWAY_PROCESSOR_PROJECT_API_SECRET").encode(),
        message.encode(),
        hashlib.sha256).hexdigest()
    if signature == request.json['signature']:
        print("signature matched, we can ship")
    return "success"
