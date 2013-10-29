#!/usr/bin/env python

import re, httplib
import cherryproxy

class Proxy(cherryproxy.CherryProxy):
   def denie(self):
      self.set_response_forbidden(reason="how about no?")

   def filter_request(self):
      for _ in xrange(0,5):
         conn = httplib.HTTPConnection(self.req.netloc)
         conn.request(self.req.method, self.req.full_url, self.req.data, self.req.headers)
         r1 = conn.getresponse()
         conn.close()

   def filter_request_headers(self):
      accepted = True
      headers = self.req.headers.keys()
      if not ('user-agent' in headers):
         print "User-Agent vide ou incorrect !"
         accepted = False
      if not re.match('.*(\:[80|403])?', self.req.netloc):
         print "Je suis un proxy web ! Tu m'entends ? WEB !"
         accepted = False
      if 'SSH' in base64.b64decode(self.req.query):
         print "Ai-je bien lu 'SSH' ?"
         accepted = False
      if not accepted:
         self.denie()
      pass

   def filter_response(self):
      headers = dict(self.resp.headers)
      if not headers['content-encoding'] in self.req.headers['accept-encoding'].split(','):
         print "Tu sais quoi ? Ton serveur t'as repondu de la merde !"
         self.denie()

if __name__ == '__main__':
    cherryproxy.main(Proxy)

