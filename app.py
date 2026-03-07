"""
Payment Service - With Discount Support and Structured Logging
Processes payments for orders
"""
import os
import logging
import json
from flask import Flask, request, jsonify

# CHANGED: Structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# TODO: Add Prometheus metrics here
PAYMENT_METHODS = {
    "credit_card": {
        "name": "Credit Card",
        "metadata": {"discount_percent": 0, "processing_fee": 2.5}
    },
    "debit_card": {
        "name": "Debit Card",
        "metadata": {"discount_percent": 0, "processing_fee": 1.5}
    },
    "paypal": {
        "name": "PayPal",
        "metadata": None
    },
}

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/api/payment/process', methods=['POST'])
def process_payment():
    data = request.get_json()
    logger.info(f"Processing payment: {json.dumps(data)}")  # CHANGED: JSON logging
    amount = data.get('amount')
    payment_method = data.get('payment_method', 'credit_card')
    use_discount = data.get('use_discount', False)

    if payment_method not in PAYMENT_METHODS:
        return jsonify({"error": "Invalid payment method"}), 400

    payment_config = PAYMENT_METHODS[payment_method]

    if use_discount:
        discount_percent = payment_config['metadata']['discount_percent']  # BUG: Still crashes
        discount_amount = amount * discount_percent / 100
        final_amount = amount - discount_amount
    else:
        final_amount = amount

    processing_fee = payment_config['metadata']['processing_fee']  # BUG: Still crashes
    final_amount += processing_fee

    return jsonify({
        "payment_id": f"PAY-{data.get('order_id')}",
        "status": "success",
        "amount": final_amount
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
