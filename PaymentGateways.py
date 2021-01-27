import requests
from requests.auth import HTTPBasicAuth

i = 0


# Validating the Credit Card Number:
# ---------------------------------
def card_validator(card_number):
    try:
        card_number = list(card_number.strip())
        last_digit = card_number.pop()
        card_number.reverse()

        processed_digits = []

        for index, digits in enumerate(card_number):
            if index % 2 == 0:
                doubled_digits = int(digits) * 2
                if doubled_digits > 9:
                    doubled_digits = doubled_digits - 9
                processed_digits.append(doubled_digits)
            else:
                processed_digits.append(int(digits))

        final = int(last_digit) + sum(processed_digits)

        if final % 10 == 0:
            return True
        else:
            return False

    except:
        return False


# Stripe API for Cheap payment process:
# ------------------------------------
def stripe():
    url = 'https://api.stripe.com/v1/checkout/sessions'
    data = {
        "success_url": "https://localhost:8080/thanks",
        "cancel_url": "https://localhost:8080/thanks",
        "payment_method_types[0]": "card",
        "line_items[0][price]": "price_1IEDOoBjl4ynhlDwWvufrlAS",
        "line_items[0][quantity]": "2",
        "mode": "payment"
    }
    response = requests.post(url=url, data=data, auth=HTTPBasicAuth(
        'sk_test_51IBh3aBjl4ynhlDw9tXdexBCWsUX5E6lELVEUL9TiexLLTrORoenmBkrMr8JQSJoSdj9H2RvWZENvU6ZLWnfKi7L00UhwZ3nMs',
        ''))
    return response


# Cash free API for premium payment process:
# -----------------------------------------
def cash_free(amount):
    global i
    i += 1
    if i == 4:
        i -= 1

    url = 'https://test.cashfree.com/api/v1/order/create'

    data = {

        "appId": "50480462db9e359ed987f030108405",
        "secretKey": "d3fd0e40cc3dc2a2459b75651bba35e0be4d6c99",
        "orderId": i,
        "orderAmount": str(amount),
        "customerName": "Mano",
        "customerPhone": "1234567889",
        "customerEmail": "abc@gmail.com",
    }

    response = requests.post(url=url, data=data)

    return response


# Razor Pay API for premium payment process:
# -----------------------------------------
def razor(amount):
    url = 'https://api.razorpay.com/v1/orders'
    data = {
        "amount": amount,
        "currency": "INR",
        "receipt": "order_rcptid_11"
    }

    response = requests.post(url=url, data=data,
                             auth=HTTPBasicAuth('rzp_test_jBtQNXJxzwswxd', 'n1IUQx4ljFiKGD8CgVjfTame'))
    return response
