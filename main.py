import time
from datetime import datetime
import requests
import json

delay = 1800  # seconds
discord_webhook = 'MY_WEBHOOK'  # enter in your webhook url
currencies_list = ['BTC', 'ETH', 'LTC', 'BCH']

'''
donate me a cup of coffee using:
ETH: 0xCf99569890771d869BfC28C776D07F59b0636D72
'''


def get_price(currency: str):
    price_url = 'https://api.coinbase.com/v2/prices/{}-USD/spot'.format(currency)
    request = requests.get(price_url)
    request = json.loads(request.text)
    return request['data']['amount']


def push_to_discord(currencies: list) -> str:
    fields = []
    for currency in currencies:
        price = get_price(currency)
        fields.append({
            'name': currency,
            'value': '$' + str(price),
            'inline': True
        })
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
    embeds = [{
        'type': 'rich',
        'color': 123456,
        'timestamp': timestamp,
        'fields': fields
    }]
    payload = {'embeds': embeds}
    r = requests.post(discord_webhook, json=payload)
    if r.status_code != 204:
        print('Failed to push Webhook.\nPossible error:\n\t- Invalid Webhook')
    return timestamp


if __name__ == '__main__':
    while True:
        pushed_timestamp = push_to_discord(currencies_list)
        print(pushed_timestamp)  # print to console to make sure program isn't frozen
        time.sleep(delay)
