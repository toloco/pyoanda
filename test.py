# import requests
import json
import yaml
# import sys

# from optparse import OptionParser

# from constants import OANDA_DOMAIN


# def create_stream():
#     with open("./contrib/config.yaml") as f:
#         config = yaml.load(f.read())
#     access = config["access"]

#     instruments = "EUR_GBP"
#     url = "https://{}/v1/prices".format(OANDA_DOMAIN)
#     headers = {'Authorization' : 'Bearer {}'.format(access["access_token"])}
#     params = {'instruments' : instruments, 'accountId' : access["account_id"]}
#     req = requests.Request('GET', url, headers = headers, params = params)

#     with requests.Session() as s:
#         resp = s.send(req.prepare(), stream = True, verify = False)
#         assert resp.status_code == 200
#         return resp


# def demo(displayHeartbeat):
#     try:
#         response = create_stream()
#     except AssertionError:
#         print("Can't connect")
#         sys.exit(1)


#     for line in response.iter_lines(1):
#         if line:
#             try:
#                 msg = json.loads(line.decode("utf-8"))
#             except Exception as e:
#                 import ipdb; ipdb.set_trace()
#                 print("Caught exception when converting message into json\n" + str(e))
#                 return
            
#             if displayHeartbeat:
#                 print(line)
#             else:
#                 if 'instrument' in msg or 'tick' in msg:
#                     print(line)

# def main():
#     usage = "usage: %prog [options]"
#     parser = OptionParser(usage)
#     parser.add_option("-b", "--displayHeartBeat", dest = "verbose", action = "store_true", 
#                         help = "Display HeartBeat in streaming data")
#     displayHeartbeat = False

#     (options, args) = parser.parse_args()
#     if len(args) > 1:
#         parser.error("incorrect number of arguments")
#     if options.verbose:
#         displayHeartbeat = True
#     demo(displayHeartbeat)


if __name__ == "__main__":
    from pyoanda.client import Client
    with open("./contrib/config.yaml") as f:
        config = yaml.load(f.read())
    c = Client(config["domains"]["api"])   
    print(c.login(
            account_id=config["access"]["account_id"],
            access_token=config["access"]["access_token"]
        ))

