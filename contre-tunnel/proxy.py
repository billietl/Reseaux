#!/usr/bin/env python

import re, httplib
import cherryproxy

class Proxy(cherryproxy.CherryProxy):
   def filter_request(self):
      for _ in xrange(0,5):
         conn = httplib.HTTPConnection(__proxy__)
         conn.request(self.req.method, self.req.full_url, self.req.data, self.req.headers)
         r1 = conn.getresponse()
         conn.close()

   def filter_request_headers(self):
      accepted = True
      headers = self.req.headers.keys()
      if not ('user-agent' in headers and ['user-agent'] != None):
         accepted = False
      if re.match('192\.168\.\d+\.\d+', self.req.netloc) :
         accepted = False
      if not accepted:
         self.set_response_forbidden(reason="how about no?")

   def filter_response(self):
      pass

if __name__ == '__main__':
    cherryproxy.main(Proxy)

