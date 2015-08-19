.. _usage:
=====
Usage
=====

.. code-block:: python

    from pyoanda import Client, PRACTICE

    c = Client(
        environment=PRACTICE,
        account_id="Your Oanda account ID",
        access_token="Your Oanda access token"
    )

    c.get_instrument_history(
        instrument="EUR_GBP",
        candle_format="midpoint",
        granularity="S30"
    )

.. Note:: that if you are indenting to use the sandbox environment, you should first use the  API to create an account then use the account_id to run the example above.

.. code-block:: python

    from pyoanda import Client, SANDBOX

    c = Client(environment=SANDBOX)

    # Create an account
    user = c.create_account()

    # Retrieve the username and accountId values for future use
    print "username: %s\naccount_id: %d" % (user['username'], user['accountId'])
