from flask import Flask, jsonify, request, make_response, url_for, render_template, session
import json
import requests
from requests.auth import HTTPBasicAuth
import datetime
import traceback
import PaymentGateways

app = Flask(__name__)
attempt = 0


# Index Page for card payment
# ---------------------------
@app.route('/')
def index_page():
    return render_template('index.html')


# Process Payment Methods:
# -----------------------
@app.route('/payment/process', methods=['POST'])
def ProcessPayment():
    global attempt

    params = request.get_json()
    if params is None:
        return make_response(
            jsonify({'Message': 'Please fill necessary fields', 'Error': 'Cant get field values'}), 400)

    CreditCardNumber = params['CreditCardNumber']
    CardHolder = params['CardHolder']
    ExpirationDate = params['ExpirationDate']
    SecurityCode = params['SecurityCode']
    Amount = params['Amount']

    # Validating the Card Number:
    # --------------------------
    if CreditCardNumber == '':
        return make_response(
            jsonify({'Message': 'Please Enter Credit Card Number', 'Error': 'The request is invalid'}), 400)

    if not PaymentGateways.card_validator(CreditCardNumber):
        return make_response(
            jsonify({'Message': 'Please Enter Valid Credit Card Number', 'Error': 'The request is invalid'}), 400)

    present_date = datetime.datetime.now().date()
    if ExpirationDate or ExpirationDate != '':
        ExpirationDate = datetime.datetime.strptime(ExpirationDate, "%m/%Y").date()
        print(ExpirationDate)
    else:
        return make_response(
            jsonify({'Message': 'Please Enter Expiration Date', 'Error': 'The request is invalid'}), 400)

    # Validating the Expiration Date:
    # ------------------------------
    if ExpirationDate < present_date:
        return make_response(
            jsonify({'Message': 'Please Enter Valid Expiration Date', 'Error': 'The request is invalid'}), 400)

    # Validating the Card Holder:
    # --------------------------
    if not CardHolder:
        return make_response(
            jsonify({'Message': 'Please enter the Card Holder Name', 'Error': 'The request is invalid'}), 400)

    # Validating the Empty Amount:
    # ---------------------------
    if Amount == '':
        return make_response(
            jsonify({'Message': 'Minimum Amount should be 1', 'Error': 'The request is invalid'}), 400)

    # Validating the negative and below 0 Amount:
    # -------------------------------------------
    if int(Amount) <= 0:
        return make_response(
            jsonify({'Message': 'Please enter the Valid Amount', 'Error': 'The request is invalid'}), 400)

    # Cheap Payment Process:
    # ---------------------
    if int(Amount) <= 20:
        try:
            response = PaymentGateways.stripe().json()
            status_code = PaymentGateways.stripe().status_code

            if status_code == 200:
                return make_response(
                    jsonify({'Message': 'CheapPaymentProcess', 'Total Amount': response['amount_total']}), 200)
            else:
                return make_response(
                    jsonify({'Message': '', 'Error': response['error']}), 400)

        except Exception as err:
            return make_response(
                jsonify({'Message': 'Something went wrong', 'Error': err, "TraceBack": traceback.format_exc()}), 400)

    # Expensive Payment Process:
    # -------------------------
    if 20 < int(Amount) <= 500:
        try:
            status_code = PaymentGateways.cash_free(Amount).status_code
            response = PaymentGateways.cash_free(Amount).json()
            print(status_code)
            print(response)
            if status_code == 200:
                return make_response(
                    jsonify({'Message': 'ExpensivePaymentProcess'}), 200)

            elif status_code != 200:
                stripe_status_code = PaymentGateways.stripe().status_code
                stripe_response = PaymentGateways.stripe().json()

                if stripe_status_code == 200:
                    return make_response(
                        jsonify({'Message': 'The process done with CheapPaymentProcess',
                                 'Total_Amount': stripe_response['amount_total'], 'ExpensivePayment_Error': response['reason']}), 200)
                else:
                    return make_response(
                        jsonify({'Message': 'The payment can not done please Retry',
                                 'Error': stripe_response['error']['message']}), 400)

        except Exception as err:
            return make_response(
                jsonify({'Message': 'Oops! Something went wrong with Your transaction', 'err': err}), 400)

    # Premium Payment Process:
    # -----------------------
    if int(Amount) > 500:
        try:
            status_code = PaymentGateways.razor(Amount).status_code
            response = PaymentGateways.razor(Amount).json()

            if status_code == 200:
                return make_response(
                    jsonify({'Message': 'You have made Premium Payment Process', "Amount": response['amount']}), 200)

            elif status_code != 200:
                attempt += 1

                if attempt == 1 or attempt == 2:
                    return make_response(
                        jsonify({'Message': 'Having trouble with Payment Process',
                                 'Error': response}), 400)

                else:
                    return make_response(
                        jsonify({'Message': 'You made 3 attempts please try after sometimes'}), 400)

        except Exception as err:
            return make_response(
                jsonify({'Message': '', 'Error': err}), 400)


# Index Page for card payment
# ---------------------------
@app.route('/thanks')
def thanks():
    return 'welcome'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=500, debug=True)
