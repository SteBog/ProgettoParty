# coding=utf-8
import socket
import json
from _thread import *

INDIRIZZO_IP_SERVER = "87.250.73.23"
PORTA_SERVER = 8100

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	sock.bind((INDIRIZZO_IP_SERVER, PORTA_SERVER))
except socket.error as e:
	str(e)

sock.listen(4)

print("Server online")
print("Attendo connessione...")

def crea_giocatore():
	giocatore = {
		"minigioco": 0,
		"numero_giocatore": -1,
		"coordinata_x": 0,
		"coordinata_y": 0,
		"rivolto_a_destra": 0,
		"ancora_vivo": 0,
	}
	return giocatore

def encode_pos():
	return json.dumps(giocatori)

def decode_pos(stringa_json):
	return json.loads(stringa_json)

giocatori = []

for i in range(4):
	giocatori.append(crea_giocatore())

numGiocatore = 0
	


def t_client(conn, numGio):
	conn.send(str.encode(encode_pos()))
	risposta = str(numGio)

	while True:
		try:
			data = decode_pos(conn.recv(2048).decode())
			giocatori[numGio] = data["giocatore"]

			if not data:
				print("Disconnesso")
				break
			else:
				risposta = str(numGio)
				risposta += encode_pos()

			conn.sendall(str.encode(risposta))
		except:
			break
	
	print("Connessione terminata")
	conn.close()
	global numGiocatore
	numGiocatore -= 1

while True:
	conn, addr = sock.accept()
	print("Connesso a: ", addr)
	print("Giocatore numero: ", numGiocatore)

	start_new_thread(t_client, (conn, numGiocatore))
	numGiocatore += 1