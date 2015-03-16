from .utils import by_api

class Client(object):
	CHECK_ACCOUNT_URL = "{0}/v1/accounts/{1}"
	def __init__(self, domain):
		self.domain = domain

	def login(self, account_id, access_token):
		self.access_token = access_token
		self.account_id = account_id
		return self.__check_credentials__()

	def __check_credentials__(self):
		url = self.CHECK_ACCOUNT_URL.format(self.domain, self.account_id)
		print(url)
		by_api(url, self.access_token)
		# except:
		# 	return False
		# else:
		# 	return True