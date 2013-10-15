#!/usr/bin/env python

import sys, select

def filter(request):
   ''' Retourne True si la requete est legit, false si c est un tunnel '''
   return True

class httpRequest(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(s):
      httpRequest.do_something(s)
   def do_POST(s):
      httpRequest.do_something(s)
   def do_HEAD(s):
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
   def do_something(s):
      if filter(s):
         url = s.path
         headers = s.headers
      else:
         s.send_response(400)
         

def usage():
    print "proxy.py <port>"
    exit(1)

def main():
    serveraddress = ('', __port__)
    proxyserver = BaseHTTPServer.HTTPServer(serveraddress, httpRequest)
    while True:
	proxyserver.handle_request()
	return 0

if __name__ == '__main__':
    if len(sys.argv)<2:
        usage()
    if not sys.argv[1].isdigit():
        usage()
    global __port__ = int(sys.argv[1])
    main()

