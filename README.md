# PYOANDA

[![Build Status](https://travis-ci.org/toloco/pyoanda.svg?branch=master)](https://travis-ci.org/toloco/pyoanda)
[![Coverage Status](https://coveralls.io/repos/toloco/pyoanda/badge.svg)](https://coveralls.io/r/toloco/pyoanda)
[![PyPi version](https://img.shields.io/pypi/v/pyoanda.svg)](https://pypi.python.org/pypi/pyoanda)
[![PyPi downloads](https://img.shields.io/pypi/dm/pyoanda.svg)](https://pypi.python.org/pypi/pyoanda)

Oanda’s API python wrapper. Robust and Fast API wrapper for your Forex bot
Python library that wraps [Oanda](http://oanda.com) API. Built on top of requests, it’s easy to use and makes sense.

Pyoanda is released under the [MIT license](https://raw.githubusercontent.com/toloco/pyoanda/master/LICENSE). The source code is on [GitHub](https://github.com/toloco/pyoanda/) and [issues are also tracked on GitHub](https://github.com/toloco/pyoanda/issues).

### Install 
#### Pypi
```bash
pip install pyoanda
```

#### Manual
```bash
git clone git@github.com:toloco/pyoanda.git
cd pyoanda
python setup.py install
# Make sure it works
python setup.py test
```

### Code example

```python
    from pyoanda import Client, SANDBOX

    c = Client(
        environment=SANDBOX,
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


See [Pypi](https://pypi.python.org/pypi/pyoanda) project page.


