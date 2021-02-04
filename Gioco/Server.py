# coding=utf-8
import socket
import json
from random import randint
import time
from _thread import *

INDIRIZZO_IP_SERVER = "87.250.73.23"
PORTA_SERVER = 8100

SECONDI_SPAWN_MONETA = 2

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
		"pronto": 0
	}
	return giocatore

def crea_moneta(numero):
	moneta = {
		"id_moneta": numero,
		"tipo_moneta": randint(1, 10),
		"coordinata_x" : randint(20, 1900),
		"coordinata_y": randint(20, 1060),
	}
	return moneta

def encode_pos(oggetto):
	return json.dumps(oggetto)

def decode_pos(stringa_json):
	return json.loads(stringa_json)

giocatori = []
monete = []
contatore_monete = 1


for i in range(4):
	giocatori.append(crea_giocatore())

numGiocatore = 0



def t_client(conn, numGio):
	conn.send(str.encode(encode_pos({"giocatori": giocatori})))
	risposta = str(numGio)

	while True:
		try:
			data = decode_pos(conn.recv(2048).decode())
			giocatori[numGio] = data["giocatore"]

			if not data:
				print("Disconnesso")
				break
			else:
				if data["giocatore"]["minigioco"] == "Spintoni":
					risposta = str(numGio)
					risposta += encode_pos({"giocatori": giocatori})
				if data["giocatore"]["minigioco"] == "Pong":
					risposta = str(numGio)
					risposta += encode_pos({"giocatori": giocatori})
				if data["giocatore"]["minigioco"] == "RaccogliMonete":
					risposta = str(numGio)
					#	Restituire posizione giocatori e delle monete

			conn.sendall(str.encode(risposta))
		except:
			break
	
	print("Connessione terminata")
	conn.close()
	global numGiocatore
	numGiocatore -= 1

def gestione_raccogli_moneta(conn):
	print("Nuovo thread: raccogli le monete")
	time.sleep(SECONDI_SPAWN_MONETA)

while True:
	conn, addr = sock.accept()
	print("Connesso a: ", addr)
	print("Giocatore numero: ", numGiocatore)

	start_new_thread(t_client, (conn, numGiocatore))
	numGiocatore += 1