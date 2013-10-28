#!/usr/bin/env python

import re, httplib
import cherryproxy

class Proxy(cherryproxy.CherryProxy):
   def filter_request(self):
      if not ('content-length' in self.req.headers and len(self.req.data) == int(self.req.headers['content-length'])):
         print "content-length de mauvaise taille !"
         self.set_response_forbidden(reason="how about no?")
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
      if not accepted:
         self.set_response_forbidden(reason="how about no?")

   def filter_response(self):
      if not self.res.headers['content-encoding'] in self.req.headers['accept-encoding'].split(',').trim():
         print "Tu sais quoi ? Ton serveur t'as repondu de la merde !"
         self.set_response_forbidden(reason="how about no?")

if __name__ == '__main__':
    cherryproxy.main(Proxy)

