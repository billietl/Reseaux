#!/usr/bin/env python

from time import sleep 
import base64
import urlparse
import socket
import threading
import httplib
import urllib
import select
from collections import deque

# Utiliser extend et popleft pour le buffer
output_buffer = deque()
input_buffer = deque()
local_client_is_up = True

def communicate_with_local(connection):
	global local_client_is_up
	global output_buffer
	global input_buffer
	while 1:
		read_me, write_me, err_dude = select.select([connection], [connection], [], 120)
		for s in read_me:
			data = s.recv(1024)
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
	HOST = 'localhost'
	PORT = int (input("Quel port voulez-vous rendre disponible ? "))
	conn_local = socket.create_connection((HOST,PORT))
	# Ouverture d'un thread qui mangera les donnees du client
	comm_thread = threading.Thread(None, communicate_with_local, None, (conn_local,), {})
	comm_thread.start()
	while 1:
		sleep(0.1)
		# Init connection HTTP
		conn_tunnel = httplib.HTTPConnection("192.168.12.94:8080")
		headers = {"Cache-Control": "no-store"}
		# modif des data en fonction des event
		try:
			vers_tunnel_data = output_buffer.popleft()
		except IndexError:
			vers_tunnel_data = ''
		# envoie de la request
		try:
			print "j'envoie comme requete HTTP : \"" + vers_tunnel_data + "\""
			conn_tunnel.request("GET", "/&data="+vers_tunnel_data, '', headers)
		except socket.error:
			output_buffer.extendleft((vers_tunnel_data,))
			conn_tunnel.close()
			sleep(5)
			continue
		# reception de la response
		r1 = conn_tunnel.getresponse()
		if r1.status == 200 :
			depuis_tunnel_data = r1.read()
			# Post dans le buffer le retour du serveur
			input_buffer.extend(depuis_tunnel_data)
		else :
			output_buffer.extendleft((vers_tunnel_data,))
			sleep(5)
		conn_tunnel.close()
	conn_local.close()

if __name__ == "__main__":
    main()
