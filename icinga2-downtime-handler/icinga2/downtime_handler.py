import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Handler(object):

	def __init__(self, icinga_url, icinga_user, icinga_pass):
		self.icinga_url = icinga_url
		self.icinga_user = icinga_user
		self.icinga_pass = icinga_pass

	def prepare_request(self, method):
		response = None
		if method == 'GET' or method == 'get':
			response = requests.get(self.icinga_url, verify=False, auth=(self.icinga_user, self.icinga_pass))
		elif method == 'POST'or method == 'post':
			response = requests.post(self.icinga_url, verify=False, auth=(self.icinga_user, self.icinga_pass))

		return response

	def get_status(self):
		result = None
		result = self.prepare_request('GET')
		return result

	def set_status(self):
		pass
