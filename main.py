from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
@app.route('/currency_converter')
def currency_converter():
    amount = request.args.get('amount')
    from_currency = request.args.get('from_currency')
    to_currency = request.args.get('to_currency')

    url = f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        conversion_rate = data['rates'][to_currency]
        converted_amount = float(amount) * conversion_rate
        formatted_amount = '{:.2f}'.format(converted_amount)
        return f'{amount} {from_currency} is {formatted_amount} {to_currency}'
    else:
        return f'Unable to convert {from_currency} to {to_currency}'

@app.route('/currencies')
def get_currencies():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)

    # if response.status_code == 200:
    data = response.json()
    currencies = list(data['rates'].keys())
    return jsonify(currencies)
    # else:
    return 'Unable to retrieve currencies'

if __name__ == '__main__':
    app.run(debug=True)