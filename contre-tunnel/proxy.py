#!/usr/bin/env python

import sys, select, urlparse, re, httplib, string
import BaseHTTPServer

def filter(request):
   ''' Retourne True si la requete est legit, false si c est un tunnel '''
   requestok = True
   header = str(request.headers).upper()
   if 'USER-AGENT' not in header: requestok = False
   return True#requestok

class httpRequest(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(s):
      httpRequest.do_something(s)
   def do_POST(s):
      httpRequest.do_something(s)
   def do_HEAD(s):
      httpRequest.do_something(s)
   def do_something(s):
      if filter(s):
         print "decodage de la requete entrante"
         command = s.command
         path = s.path
         url = urlparse.urlparse(s.path).netloc
         headers_tmp = str(s.headers).split("\n")
         print headers_tmp
         headers = dict()
         for h in headers_tmp:
            if not h == '': headers[h.split(" ", 1)[0]] = h.split(" ", 1)[1].strip()
         print "lecture du flux de donnees"
         if command=="POST":
            data = s.rfile.read()
         else:
            data = ''
         print "decode"
         # proxyfication de la requete
         print "envoi de la requete proxifiee"
         try:
            http_con = httplib.HTTPConnection(url)
            print headers
            http_con.request(command, path, data, headers)
            print "envoye"
            print "recuperation de la reponse"
            http_rep = http_con.get_response()
            print "recupere"
            response_headers = http_rep.getheaders()
            response_status = http_rep.status
            print str(response_status)
            if response_status <= 299 and http_rep.status >=200:
               response_data = http_rep.read()   
            else:
               response_data = ''
            http_con.close()
            print "done"
         # envoi de la reponse proxyfiee
            print "renvoi de la reponse"
            s.send_response(response_status)
            for h in response_headers:
               s.send_header(h[0], h[1])
            s.end_headers()
            s.wfile.write(response_data)
            print "renvoye"
         except Exception:
            s.send_response(502, 'No route to host, dumbass !')
            s.end_headers()
            s.wfile.write('')
      else:
         s.send_error(403, 'How about no ?')
         

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

