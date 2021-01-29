# coding=utf-8
import socket
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

pos = [(0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)]
#	pos[0] = coordinata X
#	pos[1] = coordinata Y
#	pos[2] = è rivolto a destra?
#	pos[3] = è ancora vivo?
#	pos[4] = numero giocatore
numGiocatore = 0


def encode_pos(tup, numero):
	"""
	Trasformare un tuple in stringa
	"""
	return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(numero)

def decode_pos(str):
	"""
	Trasformare una stringa in tuple
	"""
	pos = str.split(",")
	return int(pos[0]), int(pos[1]), int(pos[2]), int(pos[3]), int (pos[4])

def t_client(conn, numGio):
	conn.send(str.encode(encode_pos(pos[numGio], numGio)))
	risposta = str(numGio)

	while True:
		try:
			data = decode_pos(conn.recv(2048).decode())
			pos[numGio] = data

			if not data:
				print("Disconnesso")
				break
			else:
				risposta = str(numGio)
				for i in range(len(pos)):
					if i != numGio:
						risposta += encode_pos(pos[i], numGio) + "/"

				risposta = risposta[:-1]

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