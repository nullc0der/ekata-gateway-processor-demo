import requests
import hmac
import hashlib
from flask import Flask, render_template, jsonify, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create-form', methods=['POST'])
def create_form():
    data = {
        'amount_requested': float(request.json['item_price']) * 100,
        'fiat_currency': 'USD',
        'project_id': 'aab69f8c-a992-4c78-b834-fddf281a8064',
        'api_key': 'F-h8RcjNRXx2yi3dFsvM-WfhHYG8-nPCSLc8dL840VE'
    }
    res = requests.post(
        'http://localhost:8000/api/v1/payment-form/create',
        json=data)
    return jsonify({'form_id': res.json()['id']})


@app.route('/payment-success', methods=['POST'])
def payment_success():
    print(request.json)
    message = f"{request.json['payment_id']}" + \
              f"{request.json['wallet_address']}" + \
        f"{request.json['amount_received']}"
    signature = hmac.new(
        "1YKefjxGgJIPXiL4IkLUIKaCTC3L_cK-B-GWfmyuIkY".encode(),
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
        "1YKefjxGgJIPXiL4IkLUIKaCTC3L_cK-B-GWfmyuIkY".encode(),
        message.encode(),
        hashlib.sha256).hexdigest()
    if signature == request.json['signature']:
        print("signature matched, we can ship")
    return "success"
