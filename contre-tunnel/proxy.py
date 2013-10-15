#!/usr/bin/env python

import sys, select, urlparse, re, httplib, string
import BaseHTTPServer

def filter(request):
   ''' Retourne True si la requete est legit, false si c est un tunnel '''
   requestok = True
   header = str(request.headers).upper()
   if 'USER-AGENT' not in header: requestok = False
   return requestok

class httpRequest(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(s):
      httpRequest.do_something(s)
   def do_POST(s):
      httpRequest.do_something(s)
   def do_HEAD(s):
      httpRequest.do_something(s)
   def do_something(s):
      if filter(s):
         command = s.command
         path = s.path
         url = urlparse.urlparse(s.path).netloc
         version = s.request_version
         headers = s.headers
         data = s.rfile.read()
         # proxyfication de la requete
         http_con = httplib.HTTPConnection(url)
         http_con.request(command, path, data, headers)
         http_rep = http_con.get_response()
         response_headers = http_rep.getheaders()
         response_status = http_rep.status
         if response_status <= 299 and http_rep.status >=200:
            response_data = http_rep.read()   
         else:
            response_data = ''
         http_con.close()
         # envoi de la reponse proxyfiee
         s.send_response(response_status)
         for h in response_headers:
            s.send_header(h[0], h[1])
         s.end_headers()
         s.wfile.write(response_data)
      else:
         s.send_error(403, 'YOU SHALL NOT PASS !!!')
         

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
    global __port__
    __port__ = int(sys.argv[1])
    main()

