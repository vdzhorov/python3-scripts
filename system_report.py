#!/usr/bin/python3.6
# Simple Python script used for reporting system information
# Author: Valentin Dzhorov

import os
import psutil
from socket import gethostname
from shutil import disk_usage
from multiprocessing import cpu_count

class bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class System_report(object):

	def __init__(self):
		self.say("---System usage report script---", '', 'BLUE')

	def round_mem(self, disk):
		return round(disk // (2**30))

	def say(self, title, msg, severity):
		if 'OK' in severity:
			color = bcolors.OKGREEN
		elif 'WARNING' in severity:
			color = bcolors.WARNING
		elif 'FAIL' in severity:
			color = bcolors.FAIL
		elif 'BLUE' in severity:
			color = bcolors.OKBLUE
		elif 'PROCS' in severity:
			color = 'PROCS'
		else:
			color = ''

		if color == bcolors.WARNING:
			print(f"{color}WARNING: {title}{bcolors.ENDC}", msg)
		elif color == bcolors.FAIL:
			print(f"{color}CRITICAL: {title}{bcolors.ENDC}", msg)
		elif color == bcolors.OKGREEN:
			print(f"{color}OK: {title}{bcolors.ENDC}", msg)
		elif color == 'PROCS':
			print(f"\t{bcolors.BOLD}{title}{bcolors.ENDC}", msg)
		else:
			print(f"{color}{title}{bcolors.ENDC}", msg)

	def uname(self):
		self.sysname, self.nodename, self.release, \
		self.version, self.machine = os.uname()
		self.say("System information:", "{}{} {} {} {} {}{}".format(bcolors.BOLD, self.sysname, self.nodename, \
			self.release, self.version, self.machine, bcolors.ENDC), 'OK')

	def hostname(self):
		self.say("Hostname:", f"{bcolors.BOLD}{gethostname()}{bcolors.ENDC}", "OK")

	def disk_usage(self):
		self.total, self.used, self.free = disk_usage("/")
		self.disk_usage_string = f"{bcolors.BOLD}Total: {self.round_mem(self.total)}GB, Used: {self.round_mem(self.used)}GB, Free: {self.round_mem(self.free)}GB{bcolors.ENDC}"
		if round((self.used / self.total) * 100) > 70:
			severity = 'WARNING'
		elif round((self.used / self.total) * 100) > 80:
			severity = 'FAIL'
		else:
			severity = 'OK'

		self.say("Disk usage of /:", self.disk_usage_string, severity)

	def memory_usage(self):
		self.total, self.available, self.percent, \
		self.used, self.free, self.active, self.inactive, \
		self.buffers, self.cached, self.shared = psutil.virtual_memory()
		self.memory_usage_string = f"{bcolors.ENDC} {bcolors.BOLD}Total: {self.round_mem(self.total)}GB, Used: {self.round_mem(self.used)}GB, Free: {self.round_mem(self.available)}GB"
		if round((self.used / self.total) * 100) > 70:
			severity = 'WARNING'
		elif round((self.used / self.total) * 100) > 80:
			severity = 'FAIL'
		else:
			severity = 'OK'

		self.say("Memory Usage:", self.memory_usage_string, severity)

	def load(self):
		self.load1, self.load5, self.load15 = os.getloadavg()
		self.load_string = f"{bcolors.BOLD}1min: {self.load1}, 5min: {self.load5}, 15min: {self.load15}{bcolors.ENDC}"
		if self.load1 > cpu_count() / 2:
			severity = 'WARNING'
		elif self.load1 > cpu_count():
			severity = 'FAIL'
		else:
			severity = 'OK'
		self.say("Load average:", self.load_string, severity)

	def top_processes(self):
		self.listOfProcs = []
		for proc in psutil.process_iter():
			self.pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
			self.pinfo['vms'] = self.round_mem(proc.memory_info().vms)
			self.listOfProcs.append(self.pinfo)
			self.listOfProcs = sorted(self.listOfProcs, key=lambda procObj: procObj['vms'], reverse=True)
		
		self.say("Top running processes:", '', 'OK')
		for proc in self.listOfProcs[:5]:
			self.say(f"PID: {proc['pid']}, Name: {proc['name']}, User: {proc['username']}", '', 'PROCS')

	def call(self):
		self.uname()
		self.hostname()
		self.disk_usage()
		self.memory_usage()
		self.load()
		self.top_processes()

System_report().call()
