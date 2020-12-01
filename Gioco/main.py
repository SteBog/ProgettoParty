import pygame
import socket
from Network import Connessione

pygame.init()

class Giocatore:
	def __init__(self, x, y, numPlayer=1):
		self.x = x
		self.y = y
		self.HEIGHT = 260
		self.WIDTH = 210
		self.immagini = []
		for i in range(0, 12):
			if i < 10:
				percorso = "/Users/stebog/OneDrive/Internet Explorer/Python/Progetto_TPSIT/Gioco/Immagini/w_p" + str(numPlayer) + "/Wraith_0" + str(numPlayer) + "_Moving Forward_00" + str(i) + ".png"
			else:
				percorso = "/Users/stebog/OneDrive/Internet Explorer/Python/Progetto_TPSIT/Gioco/Immagini/w_p" + str(numPlayer) + "/Wraith_0" + str(numPlayer) + "_Moving Forward_0" + str(i) + ".png"
			self.immagini.append(pygame.image.load(percorso))
			self.immagini[i] = pygame.transform.scale(self.immagini[i], (self.HEIGHT, self.WIDTH))
		self.rivoltoDestra = True
		self.velocita = 10
		self.indexAnimation = 0

	def disegna(self, finestra):
		if self.indexAnimation < 11:
			self.indexAnimation += 1
		elif self.indexAnimation >= 11:
			self.indexAnimation = 0

		if self.rivoltoDestra:
			finestra.blit(self.immagini[self.indexAnimation], (self.x, self.y))
		else:
			finestra.blit(pygame.transform.flip(self.immagini[self.indexAnimation], True, False), (self.x, self.y)) #   Se sta andando a sinistra flippa l'immagine prima di "stamparla"

	def muovi(self, tasti):
		#   Evitare che la velocità in diagonale sia (10^2 + 10^2)^1/2 ma renderla 10 (come in orizzontale e verticale)
		if (tasti[pygame.K_UP] or tasti[pygame.K_DOWN]) and (tasti[pygame.K_LEFT] or tasti[pygame.K_RIGHT]):
			self.velocita = 7
		else:
			self.velocita = 10

		#   A seconda del tasto premuto muovere il giocatore
		if tasti[pygame.K_UP] and self.y >= 0:
			self.y -= self.velocita

		if tasti[pygame.K_DOWN] and self.y <= SCREENHEIGHT - self.HEIGHT:
			self.y += self.velocita

		if tasti[pygame.K_LEFT] and self.x >= 0:
			self.x -= self.velocita

			if self.rivoltoDestra:
				self.rivoltoDestra = False

		if tasti[pygame.K_RIGHT] and self.x <= SCREENWIDTH - self.WIDTH:
			self.x += self.velocita

			if not self.rivoltoDestra:
				self.rivoltoDestra = True

def encode_pos(tup):
	"""
	Trasformare un tuple in stringa
	"""
	return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])

def decode_pos(stringa):
	"""
	Trasformare una stringa in tuple
	"""
	pos = stringa.split(",")
	return int(pos[0]), int(pos[1]), int(pos[2])

def split_pos(stringa):
	"""
	Splittare le posizioni di più utenti in un oggetto iterabile
	"""
	pos = stringa.split("/")
	return pos

if __name__ == "__main__":
	FINESTRA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	SCREENWIDTH, SCREENHEIGHT = pygame.display.get_surface().get_size()
	IMMAGINE_SFONDO = pygame.image.load("/Users/stebog/OneDrive/Internet Explorer/Python/Progetto_TPSIT/Gioco/Sfondo Beta Pygame.png")

	FINESTRA.blit(IMMAGINE_SFONDO, (0, 0))
	esecuzioneInCorso = True

	net = Connessione()
	localPlayer = Giocatore(x=500, y=500)
	remotePlayers = []

	while esecuzioneInCorso:
		pygame.time.delay(17)
		##############################################################################
		#	Gestione multi-player
		##############################################################################
		remotePos = net.send(encode_pos((localPlayer.x, localPlayer.y, int(localPlayer.rivoltoDestra))))	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
		if remotePos:
			remotePos = split_pos(remotePos)
		else:
			print("Errore")
			
			#	Se si ricevono più posizioni di quelle rappresentate su schermo aggiungere altri giocatori sullo schermo
		conGioc = 0
		for i in remotePos:
			if i != "0,0,0":
				conGioc += 1

		for i in range(conGioc - len(remotePlayers)):
			remotePlayers.append(Giocatore(x=1, y=1))

		#	Modificare posizione giocatori remoti
		for remotePlayer, pos in zip(remotePlayers, remotePos):
			if pos:
				remotePlayer.x = decode_pos(pos)[0]
				remotePlayer.y = decode_pos(pos)[1]
				remotePlayer.rivoltoDestra = decode_pos(pos)[2]

		FINESTRA.blit(IMMAGINE_SFONDO, (0, 0))

		##############################################################################
		#   Listener per spegnere il gioco quando clicchi sulla
		#   x rossa
		##############################################################################

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				esecuzioneInCorso = False

		##############################################################################
		#
		##############################################################################

		keys = pygame.key.get_pressed()

		if keys[pygame.K_ESCAPE]: esecuzioneInCorso = False
		localPlayer.muovi(keys)
		localPlayer.disegna(FINESTRA)
		
		for remotePlayer in remotePlayers:
			remotePlayer.disegna(FINESTRA)

		pygame.display.update()

pygame.quit()