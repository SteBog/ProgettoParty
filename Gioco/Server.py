# coding=utf-8
import socket
import json
from _thread import *

##############################################################################
#	Creazione processo server
##############################################################################

INDIRIZZO_IP_SERVER = "127.0.0.1"
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

numGiocatore = 0
vincitore = None

giocatore = {
	"numero_giocatore": -1,
	"coordinata_x": 0,
	"coordinata_y": 0,
	"rivolto_a_destra": False,
	"ancora_vivo": False,
	"pronto": False,
	"punti": 0
}

giocatori = []

for _ in range(4): giocatori.append(giocatore)

def encode_pos(oggetto):
	return json.dumps(oggetto)

def decode_pos(stringa_json):
	return json.loads(stringa_json)

def gioco_finito():
	for player in giocatori:
		if player["ancora_vivo"]:
			return False
	return True

##############################################################################
#	Funzioni gestione singolo minigioco
##############################################################################

def spintoni(par_data, par_info):
	global vincitore

	if par_data["info"]["vincitore"]: vincitore = par_data["info"]["vincitore"]
	par_info["vincitore"] = vincitore

	return par_info

def pong():
	global vincitore

def paracadutismo(par_info):
	if gioco_finito():
		massimo = -1
		winner = None
		for player in giocatori:
			print(player["punti"])
			if player["punti"] > massimo:
				massimo = player["punti"]
				winner = player["numero_giocatore"]

		par_info["vincitore"] = winner
	return par_info
	

def gara(par_data, par_info):
	global vincitore

	if par_data["info"]["vincitore"]: vincitore = par_data["info"]["vincitore"]
	par_info["vincitore"] = vincitore

	return par_info

def battaglia_navale():
	global vincitore

##############################################################################
#	Thread di gestione di singolo giocatore
##############################################################################

def t_client(conn, numGio):
	global numGiocatore
	info = {
		"numero_giocatore": numGio,
		"vincitore": None
	}
	conn.send(str.encode(encode_pos({"giocatori": giocatori, "info": info})))
	risposta = ""

	while True:
		try:
			data = decode_pos(conn.recv(2048).decode())

			if not data:
				print("Disconnesso")
				break
			else:
				giocatori[numGio] = data["giocatore"]
				giocatori[numGio]["numero_giocatore"] = numGio

				if data["info"]["minigioco"] == "Spintoni": info = spintoni(data, info)
				if data["info"]["minigioco"] == "Gara": info = gara(data, info)
				if data["info"]["minigioco"] == "Paracadutismo": info = paracadutismo(info)

				risposta = encode_pos({"giocatori": giocatori, "info": info})

			conn.sendall(str.encode(risposta))
		except:
			break
	
	print("Connessione terminata")
	giocatori[numGio] = giocatore
	numGiocatore -= 1
	conn.close()



while True:
	conn, addr = sock.accept()
	print("\nConnesso a: ", addr)
	print("Giocatore numero: ", numGiocatore)

	start_new_thread(t_client, (conn, numGiocatore))
	numGiocatore += 1