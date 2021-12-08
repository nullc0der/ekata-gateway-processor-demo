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
        'project_id': 'd36ad22a-c545-4e94-9f3f-712f5a7ed759',
        'api_key': 'Lk_fe2r4TVr7KXMyyzd4T5miFQcAo8Q_RlY0gP8jTc0'
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
        "Xoww80Frr4mDI5E8JhrxLAQG1IHv-__rvCBTf-2cdBo".encode(),
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
        "Xoww80Frr4mDI5E8JhrxLAQG1IHv-__rvCBTf-2cdBo".encode(),
        message.encode(),
        hashlib.sha256).hexdigest()
    if signature == request.json['signature']:
        print("signature matched, we can ship")
    return "success"
