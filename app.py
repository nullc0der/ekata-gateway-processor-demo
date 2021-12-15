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
