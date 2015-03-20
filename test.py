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
    # print(c.get_instruments())
    # print(c.get_prices("EUR_GBP", stream=False))


    for line in c.get_prices("EUR_GBP", stream=True).iter_lines(1):
        if line:
            data = line.decode("utf-8")
            print(data)
            

                # print(json.loads(line.decode("utf-8")))
                # if 'instrument' in msg or 'tick' in msg:
                #     print(line)
