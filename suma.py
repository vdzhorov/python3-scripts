#!/usr/bin/env /usr/bin/python3.6
#This is used for simple calculation of domain pricing. It requires 1 argument passed to the script.

from sys import argv

scriptname, suma = argv

for i in range(1, 11):
	if i == 1:
		print(f"Price for first year: {round(float(suma) * i, 2)}")
	elif i > 1:
		print(f"Price for {i} years: {round(float(suma) * i, 2)}")