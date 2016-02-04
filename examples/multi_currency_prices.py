
from pyoanda import Client, PRACTICE

client = Client(
    environment=PRACTICE,
    account_id="{{ACCOUNT_ID}}",
    access_token="{{ACCOUNT_TOKEN}}"
)

# Get prices for a list of instruments

pair_list = ('AUD_JPY', 'EUR_JPY', 'GBP_JPY', 'AUD_USD')

dataset = client.get_prices(
    instruments=','.join(pair_list),
    stream=False
)

"""
Response sample
{
    "prices": [
        {
            "ask": 81.551,
            "bid": 81.53,
            "instrument": "AUD_JPY",
            "time": "2016-01-26T07:39:56.525788Z"
        },
        {
            "ask": 127.975,
            "bid": 127.957,
            "instrument": "EUR_JPY",
            "time": "2016-01-26T07:39:55.712253Z"
        },
        {
            "ask": 167.269,
            "bid": 167.239,
            "instrument": "GBP_JPY",
            "time": "2016-01-26T07:39:58.333404Z"
        },
        {
            "ask": 0.69277,
            "bid": 0.6926,
            "instrument": "AUD_USD",
            "time": "2016-01-26T07:39:50.358020Z"
        }
    ]
}
"""

# simplistic way of extracting data from the json response::
aud_jpy = [d for d in dataset['prices'] if d['instrument'] == 'AUD_JPY']
bid = [d['bid'] for d in aud_jpy][-1]
ask = [d['ask'] for d in aud_jpy][-1]
time = [d['time'] for d in aud_jpy][-1]
