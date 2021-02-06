# coding=utf-8
import socket
import json
from random import randint
import time
from _thread import *

##############################################################################
#	Creazione processo server
##############################################################################

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

##############################################################################
#	Funzioni per dialogo con gli host
##############################################################################

def crea_giocatore():
	giocatore = {
		"minigioco": 0,
		"numero_giocatore": -1,
		"coordinata_x": 0,
		"coordinata_y": 0,
		"rivolto_a_destra": 0,
		"ancora_vivo": 0,
		"pronto": 0,
		"punti": 0
	}
	return giocatore

def encode_pos(oggetto):
	return json.dumps(oggetto)

def decode_pos(stringa_json):
	return json.loads(stringa_json)

##############################################################################
#	Funzioni per gestione minigiochi e giocatori
##############################################################################

numGiocatore = 0
giocatori = []

for i in range(4):
	giocatori.append(crea_giocatore())

def gestione_spintoni(numero_giocatore):
	risposta = str(numero_giocatore)
	risposta += encode_pos({"giocatori": giocatori})
	return risposta

def gestione_pong(numero_giocatore):
	risposta = str(numero_giocatore)
	risposta += encode_pos({"giocatori": giocatori})
	return risposta

def gestione_gara(numero_giocatore):
	risposta = str(numero_giocatore)
	risposta += encode_pos({"giocatori": giocatori})
	return risposta

def gestione_paracadutismo(numero_giocatore):
	risposta = str(numero_giocatore)
	risposta += encode_pos({"giocatori": giocatori})
	return risposta

##############################################################################
#	Thread di gestione di singolo giocatore
##############################################################################

def t_client(conn, numGio):
	conn.send(str.encode(encode_pos({"giocatori": giocatori})))
	risposta = str(numGio)

	while True:
		try:
			data = decode_pos(conn.recv(2048).decode())

			if not data:
				print("Disconnesso")
				break
			else:
				giocatori[numGio] = data["giocatore"]

				if data["giocatore"]["minigioco"] == "Spintoni":
					risposta = gestione_spintoni(numGio)
				if data["giocatore"]["minigioco"] == "Pong":
					risposta = gestione_pong(numGio)
				if data["giocatore"]["minigioco"] == "Gara":
					risposta = gestione_gara(numGio)
				if data["giocatore"]["minigioco"] == "Paracadutismo":
					risposta = gestione_paracadutismo(numGio)

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