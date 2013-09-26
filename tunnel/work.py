#!/usr/bin/env python

from time import sleep 
import base64
import urlparse
import socket
import threading
import httplib
import urllib
from collections import deque

# Utiliser extend et popleft pour le buffer
output_buffer = deque()
input_buffer = deque()
local_client_is_up = True

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
	global input_buffer
	global output_buffer
	# Ouverture du socket sur un port aleatoire pour le client local
	HOST = 'localhost'
	PORT = int (input("Sur quel port souhaitez-vous vous connecter ?"))
	s = socket.create_connection((HOST,PORT))
	# On veut une socket non-bliquante
	s.setblocking(0)
	# Ouverture d'un thread qui mangera les donnees du client
	read_thread = threading.Thread(None, read_local_client_data, None, (s,), {})
	write_thread = threading.Thread(None, write_local_client_data, None, (s,), {})
	while 1:
		sleep(5)
		# Init connection HTTP
		conn = httplib.HTTPConnection("192.168.12.94:8080")
		headers = {"Cache-Control": "no-store"}
		# modif des data en fonction des event
		try:
			data = output_buffer.popleft()
		except IndexError:
			data = ''
		# envoie de la request
		try:
			conn.request("GET", "/&data="+data, '', headers)
		except socket.error:
			conn.close()
			sleep(5)
			continue
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

if __name__ == "__main__":
    main()
