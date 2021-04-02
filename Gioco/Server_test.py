# coding=utf-8
import socket
import json
from _thread import *
import mysql.connector
import datetime

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
#	Connessione database
##############################################################################

mydb = mysql.connector.connect(
	host="localhost",
	user="adminer",
	password="CBC349aa",
	database="Party"
)

mycursor = mydb.cursor()

query_inserisci_partita = "INSERT INTO Partita() VALUES ()"

query_inserisci_round = "INSERT INTO Round(Round.IDFMinigioco, Round.IDFPartita) VALUES (%s, %s)"

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
	"coordinata_x": 10,
	"coordinata_y": 925,
	"rivolto_a_destra": False,
	"ancora_vivo": False,
	"pronto": False,
	"punti": 0
}

elenco_minigiochi = ["Spintoni", "Gara", "Pong", "Paracadutismo"]

class Pallina:
	def __init__(self):
		self.x = 1920 // 2
		self.y = 1080 // 2
		self.direzione_verticale = 0	#	1 alto, 0 dritto, -1 basso
		self.direzione_orizzontale = 1	#	1 verso destra, -1 verso sinistra

	def collisione_giocatore(self, giocatore):
		if (self.y >= giocatore["coordinata_y"] and self.y <= giocatore["coordinata_y"] + 92) \
			and (self.x >= giocatore["coordinata_x"] and self.x <= giocatore["coordinata_x"] + 64):
			print("Collisione")

			if self.x < giocatore["coordinata_x"] + 32: 
				self.direzione_orizzontale = -1
				self.x -= 100
			else: 
				self.direzione_orizzontale = 1
				self.x += 100

			if self.y < giocatore["coordinata_y"] + 31: 
				self.direzione_verticale = 1
				self.y -= 100
			elif self.y > giocatore["coordinata_y"] + 61: 
				self.direzione_verticale = -1
				self.y += 100
			else: self.direzione_verticale = 0

	def collisione_mappa(self):
		if self.y < 0: self.direzione_verticale = -1
		if self.y > 1060: self.direzione_verticale = 1

	def is_gol(self):
		if self.x < 0: return -1		#	Gol per quelli a sinistra
		elif self.x > 1900: return 1	#	Gol per quelli a destra
		else: return 0

	def muovi(self):
		if self.direzione_verticale == 1: self.y -= 10
		elif self.direzione_verticale == -1: self.y += 10

		if self.direzione_orizzontale == 1: self.x += 10
		else: self.x -= 10

class Partita:
	def __init__(self):
		mycursor.execute(query_inserisci_partita, None)
		mydb.commit()
		self.id_partita = mycursor.lastrowid

		self.giocatori = [giocatore] * 4

		self.minigioco_in_corso = None
		self.vincitore = None

		self.info = {
			"vincitore": None,
			"numero_giocatore": None,
			"minigioco": self.minigioco_in_corso,
			"x": 1920 // 2,
			"y": 1080 // 2
		}
	
	def inserisci_round(self, idf_minigioco):
		valori = (idf_minigioco, self.id_partita)

		mycursor.execute(query_inserisci_round, valori)
		mydb.commit()

		return mycursor.lastrowid

	def gioco_finito(self):
		for player in self.giocatori:
			if player["ancora_vivo"]:
				return False
		return True

	def tutti_pronti(self):
		for player in self.giocatori:
			if not player["pronto"]:
				return False
		return True

	def home(self, conn, numero):
		while True:
			try:
				data = decode_pos(conn.recv(2048).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero

					if self.tutti_pronti():
						self.minigioco_in_corso = 1

					self.info["minigioco"] = self.minigioco_in_corso
					info_local["minigioco"] = self.minigioco_in_corso

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if self.minigioco_in_corso == 0: self.spintoni(conn, numero)
					elif self.minigioco_in_corso == 1: self.pong(conn, numero)
					elif self.minigioco_in_corso == 2: self.gara(conn, numero)
			except:
				break

	def spintoni(self, conn, numero):
		try:
			if numero == 0:
				mycursor.execute(query_inserisci_round, (1, self.id_partita))
				mydb.commit()
		except Exception:
			print(Exception.args)

		while True:
			try:
				data = decode_pos(conn.recv(2048).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero

					if data["info"]["vincitore"] is not None: 
						self.minigioco_in_corso = None
						info_local["vincitore"] = data["info"]["vincitore"]

					self.info["minigioco"] = self.minigioco_in_corso
					info_local["minigioco"] = self.minigioco_in_corso

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if data["info"]["vincitore"] is not None: return
			except:
				break

	def pong(self, conn, numero):
		try:
			if numero == 0:
				mycursor.execute(query_inserisci_round, (2, self.id_partita))
				mydb.commit()
		except Exception:
			print(Exception.args)

		pallina = Pallina()
		risultato = [0, 0]

		while True:
			try:
				data = decode_pos(conn.recv(2048).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero

					pallina.collisione_giocatore(self.giocatori[numero])
					pallina.collisione_mappa()
					
					if self.tutti_pronti(): pallina.muovi()

					####################################################
					#	Specificare la posizione per tutti
					#	e poi assegnarla all'info del
					#	singolo giocatore
					####################################################
					self.info["x"] = pallina.x
					self.info["y"] = pallina.y

					info_local["x"] = pallina.x
					info_local["y"] = pallina.y

					if pallina.is_gol() == -1: 
						risultato[0] += 1
						pallina.x = 1920 // 2
						pallina.y = 1080 // 2
					elif pallina.is_gol() == 1: 
						risultato[1] += 1
						pallina.x = 1920 // 2
						pallina.y = 1080 // 2

					if risultato[0] > 2: info_local["vincitore"] = [0, 2]
					elif risultato[1] > 2: info_local["vincitore"] = [1, 3]
					else: info_local["vincitore"] = None
					

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if info_local["vincitore"] is not None: return
			except:
				break

	def gara(self, conn, numero):
		try:
			if numero == 0:
				mycursor.execute(query_inserisci_round, (3, self.id_partita))
				mydb.commit()
		except Exception:
			print(Exception.args)

		while True:
			try:
				data = decode_pos(conn.recv(2048).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero

					if data["info"]["vincitore"] is not None: 
						self.minigioco_in_corso = None
						info_local["vincitore"] = data["info"]["vincitore"]

					self.info["minigioco"] = self.minigioco_in_corso
					info_local["minigioco"] = self.minigioco_in_corso

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if data["info"]["vincitore"] is not None: return
			except:
				break

	def paracadutismo(self, conn, numero):
		try:
			if numero == 0:
				mycursor.execute(query_inserisci_round, (4, self.id_partita))
				mydb.commit()
		except Exception:
			print(Exception.args)

		while True:
			try:
				data = decode_pos(conn.recv(2048).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero

					if self.gioco_finito():
						massimo = -1
						winner = None
						for player in self.giocatori:
							if player["punti"] > massimo:
								massimo = player["punti"]
								winner = player["numero_giocatore"]

						info_local["vincitore"] = winner

					self.info["minigioco"] = self.minigioco_in_corso
					info_local["minigioco"] = self.minigioco_in_corso

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if data["info"]["vincitore"] is not None: return
			except:
				break



def t_client(conn, num_gio, partita):
	global numero_giocatori

	conn.send(str.encode(encode_pos({"giocatori": partita.giocatori, "info": partita.info})))

	partita.home(conn, num_gio)

	print("Connessione terminata")
	partita.giocatori[num_gio] = giocatore
	numero_giocatori -= 1
	conn.close()


while True:
	conn, addr = sock.accept()
	print("\nConnesso a: ", addr)

	if (numero_giocatori % 4 == 0): partite.append(Partita())
	start_new_thread(t_client, (conn, numero_giocatori, partite[-1]))

	numero_giocatori += 1