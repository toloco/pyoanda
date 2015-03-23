# PYOANDA 

Python library that wraps [Oanda](http://oanda.com) API.


Status: __ALPHA__


### Code example

```python
    from pyoanda.client import Client

    c = Client(
        domain="https://api-fxpractice.oanda.com, 
        domain_stream="https://stream-fxpractice.oanda.com", 
        account_id="Your Oanda account ID",
        access_token="Your Oanda access token"
    )

    c.get_instrument_history(
    	instrument="EUR_GBP",
    	candle_format="midpoint",
    	granularity="S30"
    )
```

### Run test
```shell
py.test
```


[Pypi Page](https://pypi.python.org/pypi/pyoanda/0.1.0)