#!/usr/bin/env python

from time import sleep 
import base64
import urlparse
import socket
import threading
import BaseHTTPServer
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
      data = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('data', None)
      input_buffer.extend(data)
      # Envoi de la reponse
      s.send_response(200)
      s.send_header("Content-Type", "application/octet-stream")
      s.send_header("Content-Transfer-Encoding", "base64")
      s.send_header("Cache-Control", "no-store")
      s.end_headers()
      try:
         s.wfile.write(output_buffer.popleft())
      except IndexError:
         s.wfile.write("")

def read_local_client_data(connection):
   global local_client_is_up
   global output_buffer
   while 1:
      # On recupere les donnees
      data = connection.recv(1024)
      if not data: break
      output_buffer.extend(base64.b64encode(data))
   local_client_is_up = False

def write_local_client_data(connection):
   global local_client_is_up
   global input_buffer
   while 1:
      # On envoie des donnees si besoin
      try:
         connection.sendall(base64.b64decode(input_buffer.popleft()))
      except IndexError:
         sleep(0.1)
      except Error:
         local_client_is_up = False
      if not local_client_is_up: break

def main():
   global local_client_is_up
   # Ouverture du socket sur un port aleatoire pour le client local
   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   sock.bind(('',0))
   print "Connectez-vous sur le port ",sock.getsockname()[1]
   sock.listen(1)
   conn, addr = sock.accept()
   # Ouverture d'un thread qui mangera les donnees du client
   read_thread = threading.Thread(None, read_local_client_data, None, (conn,), {})
   write_thread = threading.Thread(None, write_local_client_data, None, (conn,), {})
   # Ouverture du serveur http
   server_address = ('',8080)
   fresh_server = BaseHTTPServer.HTTPServer(server_address, HTTP_tunnel_handler)
   # Lancement du thread
   read_thread.start()
   write_thread.start()
   # Lancement du service
   while local_client_is_up:
      fresh_server.handle_request()
   # Fermeture du service
   conn.close()
   print "Fermeture du tunnel"
   exit(0)

if __name__ == "__main__":
    main()
