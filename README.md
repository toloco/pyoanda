# PYOANDA

[![Build Status](https://travis-ci.org/toloco/pyoanda.svg?branch=master)](https://travis-ci.org/toloco/pyoanda)
[![Coverage Status](https://coveralls.io/repos/toloco/pyoanda/badge.svg)](https://coveralls.io/r/toloco/pyoanda)
[![Latest Version](https://pypip.in/version/pyoanda/badge.svg)](https://pypi.python.org/pypi/pyoanda/)
[![Supported Python versions](https://pypip.in/py_versions/pyoanda/badge.svg)](https://pypi.python.org/pypi/pyoanda/)
[![Supported Python implementations](https://pypip.in/implementation/pyoanda/badge.svg)](https://pypi.python.org/pypi/pyoanda/)
[![Development Status](https://pypip.in/status/pyoanda/badge.svg)](https://pypi.python.org/pypi/pyoanda/)
[![Wheel Status](https://pypip.in/wheel/pyoanda/badge.svg)](https://pypi.python.org/pypi/pyoanda/)

Python library that wraps [Oanda](http://oanda.com) API. Built on top of requests, it’s easy to use and makes sense.

Pyoanda is released under the [MIT license](https://raw.githubusercontent.com/toloco/pyoanda/master/LICENSE). The source code is on [GitHub](https://github.com/toloco/pyoanda/) and [issues are also tracked on GitHub](https://github.com/toloco/pyoanda/issues).



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
python setup.py test

or 

nosetest pyoanda

```


See [Pypi](https://pypi.python.org/pypi/pyoanda/0.1.0) project page.

