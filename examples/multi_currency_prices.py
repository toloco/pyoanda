
    from pyoanda import Client, PRACTICE

    client = Client(environment=PRACTICE,account_id="Your Oanda account ID",access_token="Your Oanda access token")

    # Get prices for a list of instruments

    pair_list = ['AUD_JPY','EUR_JPY','GBP_JPY','AUD_USD']

    dataset = client.get_prices(instruments=','.join(pair_list),stream=False)

     #json response::
     {u'prices': [{u'ask': 81.551,
         u'bid': 81.53,
         u'instrument': u'AUD_JPY',
         u'time': u'2016-01-26T07:39:56.525788Z'},
        {u'ask': 127.975,
         u'bid': 127.957,
         u'instrument': u'EUR_JPY',
         u'time': u'2016-01-26T07:39:55.712253Z'},
        {u'ask': 167.269,
         u'bid': 167.239,
         u'instrument': u'GBP_JPY',
         u'time': u'2016-01-26T07:39:58.333404Z'},
        {u'ask': 0.69277,
        u'bid': 0.6926,
        u'instrument': u'AUD_USD',
        u'time': u'2016-01-26T07:39:50.358020Z'}]}
    
    
     # simplistic way of extracting data from the json response::
    
     aud_jpy = [d for d in dataset['prices'] if d['instrument']=='AUD_JPY']
     bid = [d['bid'] for d in aud_jpy][-1]
     ask = [d['ask'] for d in aud_jpy][-1]
     time = [d['time'] for d in aud_jpy][-1]
     
     



