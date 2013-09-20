#!/usr/bin/env python

import BaseHTTPServer
from collections import deque

# Utiliser extend et popleft pour le buffer
buffer = deque()
local_client_is_up

class HTTP_tunnel_handler(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(s):
      HTTP_tunnel_handler.do_something(s)
   def do_POST(s):
      HTTP_tunnel_handler.do_something(s)
   def do_HEAD(s):
      s.send_response(200)
      s.send_header("Content-type", "text/html")
      s.end_headers()
   def do_something(s):
      s.send_response(200)
      s.send_header("Content-Type", "application/octet-stream")
      s.send_header("Content-Transfer-Encoding", "base64")
      s.send_header("Cache-Control", "no-store")
      s.end_headers()
      s.wfile.write("Some data")

def eat_local_client_data():
   # omnomnomnomnom
   # unset flag

def main():
   # Ouverture port local
   server_address = ('',8080)
   fresh_server = BaseHTTPServer.HTTPServer(server_address, HTTP_tunnel_handler)
   # omnomnomnomnom
   while local_client_is_up:
      fresh_server.handle_request()

if __name__ == "__main__":
    main()
