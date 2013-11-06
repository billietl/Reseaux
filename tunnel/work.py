#!/usr/bin/env python

from time import sleep 
import base64
import urlparse
import socket
import threading
import httplib
import urllib
import sys
import select
import random
import string
from collections import deque

def usage():
    print "work.py <site de destination> <proxy>"
    exit(1)

# Utiliser extend et popleft pour le buffer
output_buffer = deque()
input_buffer = deque()
local_client_is_up = True

def communicate_with_local(connection):
	global local_client_is_up
	global output_buffer
	global input_buffer
	while local_client_is_up:
                sleep(0.1)
		read_me, write_me, err_dude = select.select([connection], [connection], [], 120)
		for s in read_me:
			data = s.recv(512)
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
	global __proxy__
	global __l_autre_bout_du_tunnel__
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
		conn_tunnel = httplib.HTTPConnection(__proxy__)
		headers = {
                    "Cache-Control": "no-store",
                    "User-Agent": "Overclocked minitel over avian carrier",
                    "Content-Length": "0",
                    "Accept-Encoding": "base64"
                }
		# modif des data en fonction des event
		try:
			vers_tunnel_data = output_buffer.popleft()
		except IndexError:
			vers_tunnel_data = ''
		# envoie de la request
                chemin_bidon = ''.join(random.choice(string.ascii_uppercase+string.digits+string.lowercase) for x in range(20))+".html"
		try:
			conn_tunnel.request("POST", "http://"+__l_autre_bout_du_tunnel__+"/"+chemin_bidon+"?data="+vers_tunnel_data, '', headers)
			# reception de la reponse
                        r1 = conn_tunnel.getresponse()
			if r1.status == 200:
				depuis_tunnel_data = r1.read()
				# Post dans le buffer le retour du serveur
				input_buffer.extend((depuis_tunnel_data,))
			elif r1.status == 410:
				r1.read()
				local_client_is_up = False
				comm_thread.join()
				input_buffer.clear()
				output_buffer.clear()
				conn_local.close()
				conn_local = socket.create_connection((HOST,PORT))
				local_client_is_up = True
				comm_thread = threading.Thread(None, communicate_with_local, None, (conn_local,), {})
				comm_thread.start()
			else :
				output_buffer.extendleft((vers_tunnel_data,))
				sleep(5)
			conn_tunnel.close()
		except (socket.error, httplib.BadStatusLine):
			output_buffer.extendleft((vers_tunnel_data,))
			conn_tunnel.close()
			sleep(5)
			continue
	conn_local.close()

if __name__ == "__main__":
    if len(sys.argv)<3:
	    usage()
    global __proxy__
    __proxy__ = sys.argv[2]
    global __l_autre_bout_du_tunnel__
    __l_autre_bout_du_tunnel__ = sys.argv[1]
    main()
