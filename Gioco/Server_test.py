# coding=utf-8
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
QUANTITA_DATI_TRASMESSI = 1024

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

query_inserisci_partita = "INSERT INTO Partita() VALUES ()"

query_inserisci_round = "INSERT INTO Round(Round.IDFMinigioco, Round.IDFPartita) VALUES (%s, %s)"

query_inserisci_giocatore = "INSERT INTO GiocatorePartita(IDFUtente, IDFPartita, NumeroGiocatore) VALUES (%s, %s, %s)"

query_inserisci_classificato = "INSERT INTO ClassificatoRound(IDFRound, IDFGiocatore, Posizione) VALUES (%s, %s, %s)"

query_select_personaggio = "SELECT Utenti.FotoProfilo FROM Utenti WHERE Utenti.IDUtente = "

query_aggiorna_vincitore = "UPDATE Partita SET Partita.Vincitore = %s WHERE Partita.IDPartita = %s"

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
	"rivolto_a_destra": True,
	"personaggio": None,
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

			if self.x < giocatore["coordinata_x"] + 32: 
				self.direzione_orizzontale = -1
				self.x -= 25
			else: 
				self.direzione_orizzontale = 1
				self.x += 25

			if self.y < giocatore["coordinata_y"] + 31: 
				self.direzione_verticale = 1
				self.y -= 25
			elif self.y > giocatore["coordinata_y"] + 61: 
				self.direzione_verticale = -1
				self.y += 25
			else: self.direzione_verticale = 0

	def collisione_mappa(self):
		if self.y < 0: self.direzione_verticale = -1
		if self.y > 1060: self.direzione_verticale = 1

	def is_gol(self):
		if self.x < 0: return -1		#	Gol per quelli a destra
		elif self.x > 1900: return 1	#	Gol per quelli a sinistra
		else: return 0

	def muovi(self):
		if self.direzione_verticale == 1: self.y -= 2
		elif self.direzione_verticale == -1: self.y += 2

		if self.direzione_orizzontale == 1: self.x += 2
		else: self.x -= 2

class Partita:
	def __init__(self):
		self.id_partita = None
		#self.id_partita = mycursor.lastrowid

		self.giocatori = [giocatore] * 4

		self.minigioco_in_corso = None
		self.minigiochi_giocati = 0
		self.vincitore = None

		self.pallina = Pallina()
		self.risultato = [0, 0]

		self.info = {
			"vincitore": None,
			"vincitore_partita": None,
			"numero_giocatore": None,
			"minigioco": self.minigioco_in_corso,
			"x": 1920 // 2,
			"y": 1080 // 2,
			"id_round": None
		}
	
	def inserisci_round(self, idf_minigioco, mydb):
		valori = (idf_minigioco, self.id_partita)
		mycursor = mydb.cursor()

		mycursor.execute(query_inserisci_round, valori)
		mydb.commit()

		return mycursor.lastrowid

	def inserisci_giocatore_partita(self, conn, numero, connessione_db):
		mycursor = connessione_db.cursor()

		data = decode_pos(conn.recv(QUANTITA_DATI_TRASMESSI).decode())
		valori = (data["info"]["ID_Utente"], self.id_partita, numero)

		mycursor.execute(query_inserisci_giocatore, valori)
		connessione_db.commit()

		id_giocatore_partita = mycursor.lastrowid

		mycursor.execute(query_select_personaggio + str(data["info"]["ID_Utente"]))
		myresult = mycursor.fetchall()

		personaggio = None
		for x in myresult: 
			personaggio = x[0]

		info_local = self.info
		info_local["numero_giocatore"] = numero
		self.giocatori[numero]["ancora_vivo"] = True
		self.giocatori[numero]["personaggio"] = int(personaggio)

		risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
		conn.sendall(str.encode(risposta))

		vincitore = self.home(conn, numero, personaggio, id_giocatore_partita, connessione_db)

		query_aggiorna_vincitore = "UPDATE Partita SET Partita.Vincitore = " + str(vincitore) + " WHERE Partita.IDPartita = " + str(self.id_partita)
		mycursor.execute(query_aggiorna_vincitore)
		connessione_db.commit()

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

	def posizione_classifica(self, numero_giocatore, classifica):
		for i in range(4):
			if numero_giocatore == classifica[i]:
				return i
		return -1

	def home(self, conn, numero, personaggio, id_gio_par, connessione_db):
		mycursor = connessione_db.cursor()
		while True:
			try:
				data = decode_pos(conn.recv(QUANTITA_DATI_TRASMESSI).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero
					self.giocatori[numero]["personaggio"] = int(personaggio)

					if self.tutti_pronti() and numero == 1:
						self.minigioco_in_corso = self.minigiochi_giocati % 3
						self.minigiochi_giocati += 1

					self.info["minigioco"] = self.minigioco_in_corso
					info_local["minigioco"] = self.minigioco_in_corso

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if self.minigioco_in_corso == 0: 
						ritorno = self.spintoni(conn, numero, personaggio, connessione_db)

						mycursor.execute(query_inserisci_classificato, (self.info["id_round"], id_gio_par, ritorno))
						connessione_db.commit()

						self.minigioco_in_corso = None
					elif self.minigioco_in_corso == 1: 
						ritorno = self.pong(conn, numero, personaggio, connessione_db)

						if ritorno[0] == numero or ritorno[1] == numero:
							mycursor.execute(query_inserisci_classificato, (self.info["id_round"], id_gio_par, 0))
							connessione_db.commit()
						else:
							mycursor.execute(query_inserisci_classificato, (self.info["id_round"], id_gio_par, 1))
							connessione_db.commit()

						self.minigioco_in_corso = None
					elif self.minigioco_in_corso == 2: 
						ritorno = self.gara(conn, numero, personaggio, connessione_db)

						mycursor.execute(query_inserisci_classificato, (self.info["id_round"], id_gio_par, ritorno))
						connessione_db.commit()

						self.minigioco_in_corso = None

					self.info["vincitore"] = None
					if self.info["vincitore_partita"] is not None:
						return self.info["vincitore_partita"]

					if data["info"]["vincitore_partita"] is not None:
						self.info["vincitore_partita"] = data["info"]["vincitore_partita"]
						self.minigioco_in_corso = None
			except Exception as e:
				print(str(e))
				print("Home")
				print(self.info)
				break

	def spintoni(self, conn, numero, personaggio, mydb):
		try:
			if numero == 0:
				id_round = self.inserisci_round(1, mydb)
				self.info["id_round"] = id_round
		except Exception as e:
			print(str(e))

		while True:
			try:
				data = decode_pos(conn.recv(QUANTITA_DATI_TRASMESSI).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero
					self.giocatori[numero]["personaggio"] = int(personaggio)

					if data["info"]["vincitore"] is not None:
						self.info["vincitore"] = data["info"]["vincitore"]

					self.info["minigioco"] = self.minigioco_in_corso
					info_local["minigioco"] = self.minigioco_in_corso
					info_local["vincitore"] = self.info["vincitore"]

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if self.info["vincitore"] is not None:
						self.minigioco_in_corso = None

						posizione = self.posizione_classifica(numero, info_local["vincitore"])
						return posizione
			except Exception as errore:
				print(str(errore))
				print("Spintoni")
				break

	def pong(self, conn, numero, personaggio, mydb):
		try:
			if numero == 0:
				id_round = self.inserisci_round(2, mydb)
				self.info["id_round"] = id_round
		except Exception as e:
			print(str(e))

		self.risultato = [0, 0]
		while True:
			try:
				data = decode_pos(conn.recv(QUANTITA_DATI_TRASMESSI).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero
					self.giocatori[numero]["personaggio"] = int(personaggio)

					self.pallina.collisione_giocatore(self.giocatori[numero])
					self.pallina.collisione_mappa()
					
					if self.tutti_pronti(): self.pallina.muovi()

					####################################################
					#	Specificare la posizione per tutti
					#	e poi assegnarla all'info del
					#	singolo giocatore
					####################################################

					if self.pallina.is_gol() == -1: 
						self.risultato[1] += 1
						self.pallina.x = 1920 // 2
						self.pallina.y = 1080 // 2
					elif self.pallina.is_gol() == 1: 
						self.risultato[0] += 1
						self.pallina.x = 1920 // 2
						self.pallina.y = 1080 // 2

					if self.risultato[0] > 2: info_local["vincitore"] = [0, 2]
					elif self.risultato[1] > 2: info_local["vincitore"] = [1, 3]
					
					self.info["x"] = self.pallina.x
					self.info["y"] = self.pallina.y

					info_local["x"] = self.pallina.x
					info_local["y"] = self.pallina.y

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if info_local["vincitore"] is not None:
						self.pallina = Pallina()
						self.minigioco_in_corso = None
						return info_local["vincitore"]
			except:
				break

	def gara(self, conn, numero, personaggio, mydb):
		try:
			if numero == 0:
				id_round = self.inserisci_round(3, mydb)
				self.info["id_round"] = id_round
		except Exception:
			print(Exception.args)

		while True:
			try:
				data = decode_pos(conn.recv(QUANTITA_DATI_TRASMESSI).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero
					self.giocatori[numero]["personaggio"] = int(personaggio)

					if data["info"]["vincitore"] is not None: 
						self.info["vincitore"] = data["info"]["vincitore"]

					self.info["minigioco"] = self.minigioco_in_corso
					info_local["minigioco"] = self.minigioco_in_corso
					info_local["vincitore"] = self.info["vincitore"]

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if data["info"]["vincitore"] is not None:
						self.minigioco_in_corso = None
						
						posizione = self.posizione_classifica(numero, info_local["vincitore"])
						return posizione
			except:
				break

	def paracadutismo(self, conn, numero, personaggio):
		try:
			if numero == 0:
				id_round = self.inserisci_round(4)
		except Exception:
			print(Exception.args)

		while True:
			try:
				data = decode_pos(conn.recv(QUANTITA_DATI_TRASMESSI).decode())
				info_local = self.info
				info_local["numero_giocatore"] = numero

				if not data:
					print("Disconnesso")
				else:
					self.giocatori[numero] = data["giocatore"]
					self.giocatori[numero]["numero_giocatore"] = numero
					self.giocatori[numero]["personaggio"] = int(personaggio)

					if self.gioco_finito():
						massimo = -1
						winner = None
						for player in self.giocatori:
							if player["punti"] > massimo:
								massimo = player["punti"]
								winner = player["numero_giocatore"]

						self.info["vincitore"] = winner

					self.info["minigioco"] = self.minigioco_in_corso
					info_local["minigioco"] = self.minigioco_in_corso
					info_local["vincitore"] = self.info["vincitore"]

					risposta = encode_pos({"giocatori": self.giocatori, "info": info_local})
					conn.sendall(str.encode(risposta))

					if data["info"]["vincitore"] is not None:
						self.minigioco_in_corso = None
						
						posizione = self.posizione_classifica(numero, info_local["vincitore"])
						return posizione
			except:
				break



def t_client(conn, num_gio, partita):
	global numero_giocatori

	mydb = mysql.connector.connect(
		host="localhost",
		user="adminer",
		password="CBC349aa",
		database="Party"
	)

	if num_gio == 0:
		mycursor = mydb.cursor()
		mycursor.execute(query_inserisci_partita, None)
		mydb.commit()
		partita.id_partita = mycursor.lastrowid

	conn.send(str.encode(encode_pos({"giocatori": partita.giocatori, "info": partita.info})))

	partita.inserisci_giocatore_partita(conn, num_gio, mydb)

	print("Connessione terminata")
	partita.giocatori[num_gio] = giocatore
	numero_giocatori -= 1
	conn.close()


while True:
	conn, addr = sock.accept()
	print("\nConnesso a: ", addr)

	if (numero_giocatori % 4 == 0): 
		partite.append(Partita())
		print("NUOVA PARTITA")
	start_new_thread(t_client, (conn, numero_giocatori, partite[-1]))

	numero_giocatori += 1