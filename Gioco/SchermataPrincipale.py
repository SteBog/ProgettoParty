import pygame
import os

def encode_pos(tup):
	"""
	Trasformare un tuple in stringa
	"""
	return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4])

def decode_pos(stringa):
	"""
	Trasformare una stringa in tuple
	"""
	pos = stringa.split(",")
	return int(pos[0]), int(pos[1]), int(pos[2]), int(pos[3]), int(pos[4])

def split_pos(stringa):
	"""
	Splittare le posizioni di più utenti in un oggetto iterabile
	"""
	pos = stringa.split("/")
	return pos

PERCORSO = os.path.realpath(__file__)[:-29]

class Schermata_Principale:
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza):
		self.NET = connessione

		self.FINESTRA = finestra
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Campo_Final_Spikes.jpg")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		self.SCREEN_HEIGHT = schermo_altezza
		self.SCREEN_WIDTH = schermo_larghezza

		self.esecuzione_in_corso = True
		self.numero_giocatore = None

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			remotePos = self.NET.send(encode_pos((0, 0, 0, 1, 0)))	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
			if remotePos:
				self.numero_giocatore = remotePos[0]

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

			##############################################################################
			#   Listener per spegnere il gioco quando clicchi sulla
			#   x rossa
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.esecuzione_in_corso = False

			##############################################################################
			#
			##############################################################################

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzione_in_corso = False

			pygame.display.update()