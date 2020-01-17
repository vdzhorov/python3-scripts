#!/usr/bin/python3
#
# Simple python script to check if a domain is pointed to certain
# DNS nameservers, e.g. ns1.example.com and ns2.example.com
#
# The script takes one positional argument, which is a file.
# The file must contain the domains, which you are querying for.
# They are separated by newline. 
# 
# Example: ./ns_lookup.py domains.txt
# 
# You will also need to fill in the list "name_servers" with the nameservers,
# which you are mathing each domain against.
#
# Author: Valentin Dzhorov
# 

import dns.resolver
from sys import argv, exit

script, inputFile = argv

class Lookup(object):

	def __init__(self, inputFile, nameServers=[]):
		self.inputFile = inputFile
		self.nameServers = nameServers

	def strip_newline(self, line):
		return(line.strip())

	def read_file(self):
		fileHandle = None
		try:
			fileHandle = open(self.inputFile, mode='r')
		except FileNotFoundError:
			print("File does not exist")
			exit(1)
		except PermissionError:
			print("Cannot open file, permission denied.")
			exit(1)

		domainList = fileHandle.readlines()
		fileHandle.close()
		return(domainList)

	def perform_query(self):
		domainList = self.read_file()
		for name in domainList:
			name = self.strip_newline(name)
			answer = dns.resolver.query(name, 'NS', raise_on_no_answer=False)
			if answer.rrset is not None:
				try:
					for ns in self.nameServers:
						str(answer.rrset).index(ns)
				except ValueError:
					pass
				else:
					print(f"{name} matches!")
			else:
				pass

name_servers = ['ns1.delta.bg', 'ns2.delta.bg']

query = Lookup(inputFile, name_servers)
query.perform_query()
