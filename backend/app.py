import logging
from flask import Flask, request, jsonify
from uuid import uuid4
from models import Payment
from bank_simulator import simulate_bank_process

app = Flask(__name__)

payments = {}

@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json
    required_fields = ['merchant_id', 'card_number', 'expiry_month', 'expiry_year', 'amount', 'currency', 'cvv']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        logging.warning(f"Missing fields: {', '.join(missing_fields)}")
        return jsonify({'error': 'Missing fields', 'fields': missing_fields}), 400

    try:
        payment_id = str(uuid4())
        payment = Payment(
            payment_id=payment_id,
            merchant_id=data['merchant_id'],
            card_number=data['card_number'],
            expiry_month=data['expiry_month'],
            expiry_year=data['expiry_year'],
            amount=data['amount'],
            currency=data['currency'],
            cvv=data['cvv'],
            status='pending'
        )

        if simulate_bank_process(payment):
            payment.status = 'success'
        else:
            payment.status = 'failure'

        payments[payment_id] = payment
        
        logging.info(f"Processed payment: {payment_id} with status: {payment.status}")
        return jsonify({'payment_id': payment_id, 'status': payment.status}), 200 if payment.status == 'success' else 402

    except Exception as e:
        logging.error(f"Error processing payment: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

@app.route('/retrieve_payment/<payment_id>', methods=['GET'])
def retrieve_payment(payment_id):
    payment = payments.get(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404

    try:
        return jsonify({
            'payment_id': payment.payment_id,
            'merchant_id': payment.merchant_id,
            'masked_card_number': payment.masked_card_number,
            'expiry_month': payment.expiry_month,
            'expiry_year': payment.expiry_year,
            'amount': payment.amount,
            'currency': payment.currency,
            'status': payment.status
        }), 200
    except Exception as e:
        logging.error(f"Error retrieving payment: {str(e)}")
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
