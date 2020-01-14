#!/usr/bin/python3
#
# Script for performing whois searches which are filtered.
# You can say what fields you want to be displayed and only they will be shown.
# Author: Valentin Dzhorov
#

import subprocess, re
from sys import argv

script, domain = argv

class Whois(object):

	def __init__(self, search_words):
		self.search_words = search_words

	def bytes_to_string(self, byte_seq):
		return(byte_seq.decode())

	def strip_string(self, string):
		return(string.replace(' ', '', 1))

	def string_to_list(self, string, delimiter):
		return(string.split(delimiter))

	def regex_search(self, line, params):
		for p in params:
			if re.search(f"^{p}:", line):
				if 'ok' in line:
					return(self.strip_string(re.sub(r"^(.*)$", r"\033[92m \1\033[0m", line)))
				elif 'clientTransferProhibited' in line:
					return(self.strip_string(re.sub(r"^(.*)$", r"\033[93m \1\033[0m", line)))
				elif 'Redemption' in line:
					return(self.strip_string(re.sub(r"^(.*)$", r"\033[91m \1\033[0m", line)))
				else:
					return(self.strip_string(re.sub(r"^(.*?:)", r"\033[94m \1\033[0m", line)))

	def whois(self, domain):
		self.output = subprocess.check_output(f"whois {domain}", shell=True)
		self.output = self.bytes_to_string(self.output)
		self.string_list = self.string_to_list(self.output, '\n')
		for line in self.string_list:
			line = self.regex_search(line, self.search_words)
			if line != None:
				print(line)
			
new_whois = Whois(['Domain Name', 'Registrar', 'Registrar WHOIS Server', 'Updated Date', 'Creation Date', \
		'Registry Expiry Date', 'Domain Status', 'Name Server', 'Registrar'])

new_whois.whois(domain)
