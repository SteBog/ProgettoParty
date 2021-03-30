# coding=utf-8
from Server import spintoni
import socket
import json
from _thread import *
import mysql.connector

##############################################################################
#	Creazione processo server
##############################################################################

#INDIRIZZO_IP_SERVER = "127.0.0.1"
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

##############################################################################
#	Funzioni per dialogo con gli host
##############################################################################

def encode_pos(oggetto):
	return json.dumps(oggetto)

def decode_pos(stringa_json):
	return json.loads(stringa_json)

##############################################################################
#	Variabili per gestione gioco
##############################################################################

numero_giocatori = 0
partite = []
giocatore = {
	"numero_giocatore": -1,
	"coordinata_x": 0,
	"coordinata_y": 0,
	"rivolto_a_destra": False,
	"ancora_vivo": False,
	"pronto": False,
	"punti": 0
}

elenco_minigiochi = ["Spintoni", "Gara", "Pong", "Paracadutismo"]
class Partita:
	def __init__(self, connessione):
		self.id_partita = 0
		self.conn = connessione

		self.numero_giocatore = 0
		self.giocatori = [giocatore] * 4

		self.minigioco_in_corso = None
		self.vincitore = None

		self.info = {
			"vincitore": None,
			"numero_giocatore": self.numero_giocatore,
			"minigioco": self.minigioco_in_corso,
			"x": 1920 // 2,
			"y": 1080 // 2
		}

	def gioco_finito(self):
		for player in self.giocatori:
			if player["ancora_vivo"]:
				return False
		return True

	def home(self):
		data = decode_pos(conn.recv(2048).decode())

		if not data:
			print("Disconnesso")
		else:
			if self.giocatori[0]["numero_giocatore"] != -1 and self.giocatori[1]["numero_giocatore"] != -1 and \
			self.giocatori[2]["numero_giocatore"] != -1 and self.giocatori[3]["numero_giocatore"] != -1:
				self.minigioco_in_corso = 0

			risposta = encode_pos({"giocatori": self.giocatori, "info": self.info})
			conn.sendall(str.encode(risposta))

	def spintoni(self):
		data = decode_pos(conn.recv(2048).decode())

		if not data:
			print("Disconnesso")
		else:
			self.giocatori[self.numero_giocatore] = data["giocatore"]
			self.giocatori[self.numero_giocatore]["numero_giocatore"] = self.numero_giocatore

			risposta = encode_pos({"giocatori": self.giocatori, "info": self.info})
			conn.sendall(str.encode(risposta))

	def gara(self):
		data = decode_pos(conn.recv(2048).decode())

		if not data:
			print("Disconnesso")
		else:
			self.giocatori[self.numero_giocatore] = data["giocatore"]
			self.giocatori[self.numero_giocatore]["numero_giocatore"] = self.numero_giocatore

			risposta = encode_pos({"giocatori": self.giocatori, "info": self.info})
			conn.sendall(str.encode(risposta))

	def paracadutismo(self):
		data = decode_pos(conn.recv(2048).decode())

		if not data:
			print("Disconnesso")
		else:
			self.giocatori[self.numero_giocatore] = data["giocatore"]
			if self.gioco_finito():
				massimo = -1
				winner = None
				for player in self.giocatori:
					if player["punti"] > massimo:
						massimo = player["punti"]
						winner = player["numero_giocatore"]

			self.info["vincitore"] = winner


			risposta = encode_pos({"giocatori": self.giocatori, "info": self.info})
			conn.sendall(str.encode(risposta))



def t_client(conn, num_gio, partita):
	partita.numero_giocatore = num_gio
	partita.conn = conn

	while True:
		try:
			spintoni()
		except:
			break

	print("Connessione terminata")
	partita.giocatori[partita.numero_giocatore] = giocatore
	numero_giocatori -= 1
	conn.close()


while True:
	conn, addr = sock.accept()
	print("\nConnesso a: ", addr)

	numero_giocatori += 1
	if (numero_giocatori % 4 == 1): partite.append(Partita(conn))

	start_new_thread(t_client, (conn, numero_giocatori, partite[-1]))