#!/usr/bin/env python

from time import sleep 
import base64
import urlparse
import socket
import threading
import BaseHTTPServer
import select
from collections import deque

# Utiliser extend et popleft pour le buffer
output_buffer = deque()
input_buffer = deque()
local_client_is_up = True

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
      global input_buffer
      global output_buffer
      # Extrais les donnees de la requete
      data = s.path[s.path.index('=')+1:]
      input_buffer.extend((data,))
      # Envoi de la reponse
      if local_client_is_up:
         s.send_response(200)
      else:
         s.send_response(410)
      s.send_header("Content-Type", "application/octet-stream")
      s.send_header("Content-Encoding", "base64")
      s.send_header("Cache-Control", "no-store")
      s.end_headers()
      try:
         s.wfile.write(output_buffer.popleft())
      except IndexError:
         s.wfile.write("")

def communicate_with_local(connection):
	global local_client_is_up
	global output_buffer
	global input_buffer
	while local_client_is_up:
#           sleep(1)
           read_me, write_me, err_dude = select.select([connection], [connection], [], 120)
           for s in read_me:
              data = s.recv(1024)
              if len(data)==0:
                 local_client_is_up = False
              data = base64.b64encode(data)
              output_buffer.extend((data,))
           for s in write_me:
              try:
                 data = input_buffer.popleft()
                 data = base64.b64decode(data)
                 s.sendall(data)
              except IndexError:
                 pass

def main():
   global local_client_is_up
   global input_buffer
   global output_buffer
   # Ouverture du socket sur un port aleatoire pour le client local
   local_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   local_sock.bind(('',0))
   print "Connectez-vous sur le port ",local_sock.getsockname()[1]
   local_sock.listen(1)
   local_conn, addr = local_sock.accept()
   # Ouverture d'un thread qui mangera les donnees du client
   comm_thread = threading.Thread(None, communicate_with_local, None, (local_conn,), {})
   # Ouverture du serveur http
   server_address = ('',80)
   tunnel_server = BaseHTTPServer.HTTPServer(server_address, HTTP_tunnel_handler)
   # Lancement du thread
   comm_thread.start()
   # Lancement du service
   while local_client_is_up:
      tunnel_server.handle_request()
   # Fermeture du service
   tunnel_server.handle_request()
   comm_thread.join()
   local_conn.close()
   local_sock.close()
   print "Fermeture du tunnel"
   exit(0)

if __name__ == "__main__":
    main()
