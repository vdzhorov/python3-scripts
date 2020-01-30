import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Handler(object):

	def __init__(self, icinga_url, icinga_user, icinga_pass):
		self.icinga_url = icinga_url
		self.icinga_user = icinga_user
		self.icinga_pass = icinga_pass
		self.headers = {
    'Accept': 'application/json',
		}

	def api_status(self):
		request = self.prepare_request('GET', '/')
		return request

	def prepare_request(self, method, uri, json=None, verify=False):
		try:
			if method == 'GET' or method == 'get':
				request = requests.get(self.icinga_url + uri, json=json, headers=self.headers, verify=verify, auth=(self.icinga_user, self.icinga_pass))
			elif method == 'POST' or method == 'get':
				request = requests.post(self.icinga_url + uri, json=json, headers=self.headers, verify=verify, auth=(self.icinga_user, self.icinga_pass))
			else:
				raise ValueError('Incorrect method')
		except ValueError as e:
			print("Unahndled exception in request method: ", e)
		return request

	def get_all_hosts(self):
		request = self.error_handling(self.prepare_request('GET', '/v1/objects/hosts'))
		for host in request.json()['results']:
			print(host['attrs']['__name'])

	def set_host_downtime(self, host):
		time_now = time.time()
		time_after = time_now + 60*60
		json_data = {'pretty': True,
						'type': 'Host',
						'filter': 'match(\"' + host + '\", host.name)',
						'all_services': True,
						'author': 'icingaadmin',
						'comment': 'Automated downtime set',
						'fixed': True,
						'start_time': time_now,
						'end_time': time_after
						}

		request = self.error_handling(self.prepare_request('POST', '/v1/actions/schedule-downtime', json_data))
		self.print_request_status(request)
		return request

	def remove_host_downtime(self, host):
		time_now = time.time()
		time_after = time_now + 60*60
		json_data = {'pretty': True,
						'type': 'Host',
						'filter': 'match(\"' + host + '\", host.name)'
						}

		request = self.error_handling(self.prepare_request('POST', '/v1/actions/remove-downtime', json_data))
		self.print_request_status(request)
		return request

	def print_request_status(self, request):
		for r in request.json()['results']:
			print(r['status'])

	def error_handling(self, r):
		try:
			request = r
			if '500' in str(request):
				raise ValueError('500')
			elif '400' in str(request):
				raise ValueError('400')
		except ValueError as e:
			print("Error handling request. Return code", e)
			return 1
		return r
