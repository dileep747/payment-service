"""
Payment Service - With Discount Support
Processes payments for orders
"""
import os
import logging
from flask import Flask, request, jsonify

logger = logging.getLogger(__name__)

app = Flask(__name__)

# TODO: Add Prometheus metrics here
# CHANGED: Added metadata with discount support
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
    logger.info(f"Processing payment: {data}")
    amount = data.get('amount')
    payment_method = data.get('payment_method', 'credit_card')
    use_discount = data.get('use_discount', False)

    if payment_method not in PAYMENT_METHODS:
        return jsonify({"error": "Invalid payment method"}), 400

    payment_config = PAYMENT_METHODS[payment_method]

    # CHANGED: Added discount calculation
    if use_discount:
        # BUG: This will crash when metadata is None (PayPal case)
        discount_percent = payment_config['metadata']['discount_percent']
        discount_amount = amount * discount_percent / 100
        final_amount = amount - discount_amount
    else:
        final_amount = amount

    # Add processing fee
    processing_fee = payment_config['metadata']['processing_fee']  # BUG: Also crashes for PayPal
    final_amount += processing_fee

    return jsonify({
        "payment_id": f"PAY-{data.get('order_id')}",
        "status": "success",
        "amount": final_amount
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
