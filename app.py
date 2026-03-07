"""
Payment Service - Initial Implementation
Processes payments for orders
"""
import os
import logging
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)

app = Flask(__name__)

PAYMENT_METHODS = {
    "credit_card": {"name": "Credit Card", "fee": 2.5},
    "debit_card": {"name": "Debit Card", "fee": 1.5},
    "paypal": {"name": "PayPal", "fee": 3.0},
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/payment/process', methods=['POST'])
def process_payment():
    data = request.get_json()
    logger.info(f"Processing payment: {data}")
    amount = data.get('amount')
    payment_method = data.get('payment_method', 'credit_card')

    if payment_method not in PAYMENT_METHODS:
        return jsonify({"error": "Invalid payment method"}), 400

    config = PAYMENT_METHODS[payment_method]
    final_amount = amount + config['fee']

    return jsonify({
        "payment_id": f"PAY-{data.get('order_id')}",
        "status": "success",
        "amount": final_amount
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
