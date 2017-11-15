import os
import stripe
from flask import Flask, request, jsonify, g

app = Flask(__name__)
API_KEY = os.environ.get('STRIPE_SECRET_TEST_KEY')
DEFAULT_API_VERSION = '2017-06-05'

stripe.api_key = API_KEY

@app.route('/ephemeral_keys', methods=['POST'])
def ephemeral_key_provider():
    _populate_customer()
    api_version = request.form.get('api_version', DEFAULT_API_VERSION)
    key = stripe.EphemeralKey.create(customer=g.get('cus'), api_version=api_version)
    return jsonify(key)

def _populate_customer():
    if not g.get('cus'):
        customers = stripe.Customer.all().data
        if not customers:
            raise ValueError('Must have at least one customer in your test environment.')
        g.cus = customers[0].id

if __name__ == '__main__':

    if not API_KEY:
        raise ValueError("Please pass the `STRIPE_SECRET_TEST_KEY` envionment variable.")

    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
