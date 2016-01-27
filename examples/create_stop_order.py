import yaml,json,datetime
from dateutil.parser import parse
from pyoanda import Client, PRACTICE, TRADE
from pyoanda.exceptions import BadRequest
from datetime import *

# how to create a stop order without pulling out all your hair :-)

client = Client(environment=PRACTICE, account_id='replace with your account id', access_token='replace with your access token )

class AbstractDict(object):__dict__ = {}
#   ---- we use this to avoid error :: -----#
# AttributeError: 'dict' object has no attribute '__dict__'
# because 'create_order()' has this ::params=order.__dict__
# ---------------------------------------------------------#

timer = datetime.today() + timedelta(days=1)
timer = timer.isoformat("T") + "Z" #expiration time in UTC.

trade_params = {'instrument':'EUR_JPY','units':10,'side':'buy','type':'stop',
                'stopLoss':80.95,'takeProfit':170.56,'price':83.34,'expiry':timer
               }
test = AbstractDict()
test.__dict__= trade_params
stop_order = client.create_order(order=test) 



