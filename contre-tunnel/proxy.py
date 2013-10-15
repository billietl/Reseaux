#!/usr/bin/env python

import sys, select, urlparse, re, httplib, string
import BaseHTTPServer
import cherryproxy

class Proxy(cherryproxy.CherryProxy):
   def filter_request(self):
      pass

   def filter_request_headers(self):
      pass

   def filter_response(self):
      pass


def usage():
    print "proxy.py <port>"
    exit(1)

def main():
   proxy = Proxy(port=__port__, server_name='TIIR_PROXY(powered_by_CherryProxy)/0.12', debug=True)
   proxy.start()

if __name__ == '__main__':
    cherryproxy.main(Proxy)

