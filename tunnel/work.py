#!/usr/bin/env python

import socket
import threading
import httplib
from collections import deque

# Utiliser extend et popleft pour le buffer
output_buffer = deque()
input_buffer = deque()
local_client_is_up = True

def read_local_client_data(connection):
	while 1:
		# On recupere les donnees
		data = connection.recv(1024)
		if not data: break
		output_buffer.extend(base64.b64encode(data))
		local_client_is_up = False

def write_local_client_data(connection):
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
	

	# Ouverture du socket sur un port aleatoire pour le client local

	HOST = 'localhost'    # The remote host
	PORT = int (input("Sur quel port souhaitez-vous vous connecter ?"))             # The same port as used by the server
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	# Ouverture d'un thread qui mangera les donnees du client
	read_thread = threading.Thread(None, read_local_client_data, None, (s,), {})
	write_thread = threading.Thread(None, write_local_client_data, None, (s,), {})
	

	# Init connection HTTP
	conn = httplib.HTTPConnection("192.168.12.94:8080")
	headers = {"Content-Type": "application/octet-stream","Content-Transfer-Encoding": "base64", "Cache-Control": "no-store"}


	while 1:
		# modif des data en fonction des event
		params = urllib.urlencode({'data': output_buffer.popleft()})

		# envoie de la request
		conn.request("POST", "", param, headers)
		
		# reception de la response
		r1 = conn.getresponse()
		
		# test du status  si la responce est ok
		print r1.status, r1.reason

		data = r1.read()
		print data
		
		# Post dans le buffer le retour du serveur
		input_buffer.extend(data)

	conn.close()
	s.close()



