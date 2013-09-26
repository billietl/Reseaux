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
				data = base64.b64decode(data[0])
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
	s = socket.create_connection((HOST,PORT))
	# Ouverture d'un thread qui mangera les donnees du client
	comm_thread = threading.Thread(None, communicate_with_local, None, (s,), {})
	comm_thread.start()
	while 1:
		sleep(5)
		# Init connection HTTP
		conn = httplib.HTTPConnection("192.168.12.94:8080")
		headers = {"Cache-Control": "no-store"}
		# modif des data en fonction des event
		try:
			data = output_buffer.popleft()
		except IndexError:
			data = base64.b64decode('')
		# envoie de la request
		try:
			print "j'envoie comme requete HTTP : \"" + data + "\""
			conn.request("GET", "/&data="+data, '', headers)
		except socket.error:
			output_buffer.extendleft((data,))
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
