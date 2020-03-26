#!/usr/bin/python3
#
# Script for generating Nginx redirects in map file.
#
# Usage:
# nginx_map_generator.py <urls.txt> 
#
# The input file from which the URLs in the map file will be generated
# must be in the following format:
#
# http(s)://oldurl.tld http(s)://newurl.tld
#
# Note that the delimiter is single whitespace.
#
# The output file will be called "rewrites.map". Follow the instructions
# after generating a map file in order to implement it in your
# configuration.
#
# Author: Valentin Dzhorov
#

from sys import argv
import re

script, raw_input_file = argv

class Convert(object):

	def __init__(self, source):
		# Open source file
		self.outputFile = "rewrites.map"
		self.source = source

	def strip_newline(self, line):
		return line.strip()

	def regex_replace(self, line):
		return(re.sub\
		(r"^(https?:[\/]{2}[a-z0-9]*\.[a-z0-9]+)(.*)\s(https?:[\/]{2}[a-z0-9]*\.[a-z0-9]+)(.*)",\
		r"\2 \4;", line))

	def read_source_file(self):
		# Create filehandle with the raw source file
		sourceFile = open(self.source, mode='r')
		return sourceFile
		sourceFile.close()

	def write_map_file(self):
		# Write processed results from convert_to_map() to an output file.
		print(f"Opening file \"{self.outputFile}\" for writing. This file will be TRUNCATED!")
		input("Press ENTER to continue.")
		try:
			convertedFile = open(self.outputFile, mode='w')
		except IOError:
			print("IOError: Cannot open file!")
			return 1

		for line in self.convert_to_map():
			convertedFile.write(line)
			convertedFile.write("\n")

		self.end_msg()

	def convert_to_map(self):
		# Get sourceData. Take two columns separated by delimiter.
		# 1. Parse file
		# 2. Strip https?://domain.com
		# 3. Input proper header and footer
		headerString = "map $request_uri $new_uri {"
		footerString = "}"
		convertedData = [headerString]
		sourceFile = self.read_source_file()

		for line in sourceFile.readlines():
			line = self.strip_newline(line)
			line = self.regex_replace(line)
			convertedData.append(line)
		
		sourceFile.close()
		convertedData.append(footerString)

		return convertedData

	def end_msg(self):
		print(f"""
			Map file has been succefully written in $CWD/{self.outputFile}!
			In order to implement it in your Nginx configuration, you will need to:

			1. Include your generated {self.outputFile} in your Nginx configuration.
			This can be done with the configuration line:

			include includes/{self.outputFile}

			2. You may need to increase your Nginx map_hash_bucket_size and server_names_hash_bucket_size
			if you are using large quantity of rewrites.
			Read more in the official Nginx documentation: http://nginx.org/en/docs/http/ngx_http_core_module.html

			Example for large map files:

			map_hash_bucket_size 1024;
  		server_names_hash_bucket_size 256;

  		3. Process the map rewrites. This can be done by including the following block in your Nginx server {{...}} block:

  		if ($new_uri != "") {{
      rewrite ^(.*)$ $new_uri? permanent;
  		}}

  		4. Reload Nginx configuration
			""".replace('\t', ''))

convert = Convert(raw_input_file)
convert.read_source_file()
convert.convert_to_map()
convert.write_map_file()
