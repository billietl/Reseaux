#!/usr/bin/env python

import httplib


def main():
	conn = httplib.HTTPConnection("192.168.12.94:8080")
	

	while 1:
		conn.request("GET", "/")
		
		r1 = conn.getresponse()
		print r1.status, r1.reason

		data = r1.read()
		print data
	

	conn.close()
