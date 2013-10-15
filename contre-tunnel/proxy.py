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

if __name__ == '__main__':
    cherryproxy.main(Proxy)

