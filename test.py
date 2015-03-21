import json
import yaml

if __name__ == "__main__":
    from pyoanda.client import Client
    with open("../config.yaml") as f:
        config = yaml.load(f.read())
    c = Client(
        domain=config["domains"]["api"], 
        domain_stream=config["domains"]["stream"], 
        account_id=config["access"]["account_id"],
        access_token=config["access"]["access_token"]
    )

    print(c.get_instruments())
    print(c.get_prices("EUR_GBP", stream=False))
    print(c.get_instrument_history(instrument="EUR_GBP", candle_format="midpoint", granularity="S30"))
    for line in c.get_prices("EUR_GBP", stream=True).iter_lines(1):
        if line:
            print(line.decode("utf-8"))

