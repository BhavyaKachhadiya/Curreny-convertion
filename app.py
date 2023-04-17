import uvicorn
from fastapi import FastAPI

import requests

app = FastAPI()

@app.get('/currency_converter')
def currency_converter(amount: float, from_currency: str, to_currency: str):
    url = f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        conversion_rate = data['rates'][to_currency]
        converted_amount = float(amount) * conversion_rate
        formatted_amount = '{:.2f}'.format(converted_amount)
        response_data = {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "converted_amount": converted_amount,
            "formatted_amount": formatted_amount
        }
        return response_data
    else:
        return {"error": f'Unable to convert {from_currency} to {to_currency}'}

@app.get('/currencies')
def get_currencies():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        currencies = list(data['rates'].keys())
        return currencies
    else:
        return {"error": "Unable to retrieve currencies"}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
