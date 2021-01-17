import pygame
import os

def encode_pos(tup):
	"""
	Trasformare un tuple in stringa
	"""
	return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

def decode_pos(stringa):
	"""
	Trasformare una stringa in tuple
	"""
	print(stringa)
	pos = stringa.split(",")
	return int(pos[0]), int(pos[1]), int(pos[2]), int(pos[3])

def split_pos(stringa):
	"""
	Splittare le posizioni di più utenti in un oggetto iterabile
	"""
	pos = stringa.split("/")
	return pos

PERCORSO = os.path.realpath(__file__)[:-20]
print(PERCORSO)

class Giocatore:
	def __init__(self, x, y, numPlayer=1):
		self.x = x
		self.y = y
		self.HEIGHT = 278 // 3
		self.WIDTH = 193 // 3
		self.immagini = []
		for i in range(0, 12):
			if i < 10:
				percorso = PERCORSO + "/Gioco/Immagini/w_p" + str(numPlayer) + "/Wraith_0" + str(numPlayer) + "_Moving Forward_00" + str(i) + ".png"
			else:
				percorso = PERCORSO + "/Gioco/Immagini/w_p" + str(numPlayer) + "/Wraith_0" + str(numPlayer) + "_Moving Forward_0" + str(i) + ".png"
			self.immagini.append(pygame.image.load(percorso))
			self.immagini[i] = pygame.transform.scale(self.immagini[i], (self.WIDTH, self.HEIGHT))
		self.rivoltoDestra = True
		self.velocita = 10
		self.ancoraVivo = True
		self.indexAnimation = 0
		self.rettangoloCollisione = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
		

	def disegna(self, finestra):
		if self.indexAnimation < 11:
			self.indexAnimation += 1
		elif self.indexAnimation >= 11:
			self.indexAnimation = 0

		self.rettangoloCollisione = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

		if self.rivoltoDestra:
			finestra.blit(self.immagini[self.indexAnimation], (self.x, self.y))
		else:
			finestra.blit(pygame.transform.flip(self.immagini[self.indexAnimation], True, False), (self.x, self.y)) #   Se sta andando a sinistra flippa l'immagine prima di "stamparla"

	def muovi(self, tasti, screenHeight, screenWidth):
		#   Evitare che la velocità in diagonale sia (10^2 + 10^2)^1/2 ma renderla 10 (come in orizzontale e verticale)
		if (tasti[pygame.K_UP] or tasti[pygame.K_DOWN]) and (tasti[pygame.K_LEFT] or tasti[pygame.K_RIGHT]):
			self.velocita = 7
		else:
			self.velocita = 10

		#   A seconda del tasto premuto muovere il giocatore
		if tasti[pygame.K_UP] and self.y >= 0:
			self.y -= self.velocita

		if tasti[pygame.K_DOWN] and self.y <= screenHeight - self.HEIGHT:
			self.y += self.velocita

		if tasti[pygame.K_LEFT] and self.x >= 0:
			self.x -= self.velocita

			if self.rivoltoDestra:
				self.rivoltoDestra = False

		if tasti[pygame.K_RIGHT] and self.x <= screenWidth - self.WIDTH:
			self.x += self.velocita

			if not self.rivoltoDestra:
				self.rivoltoDestra = True

	def collisione(self, avversario):
		if self.rettangoloCollisione.colliderect(avversario.rettangoloCollisione):
			if avversario.x >= self.x - (self.WIDTH / 3) and avversario.x <= self.x + (self.WIDTH / 3):
				#	verticale
				if self.y < avversario.y:
					self.y -= 100
				else:
					self.y += 100
			elif avversario.y >= self.y - (self.HEIGHT / 3) and avversario.y <= self.y + (self.HEIGHT / 3):
				#	orizzontale
				if self.x < avversario.x:
					self.x -= 100
				else:
					self.x += 100
			else:
				#	diagonale
				if self.y < avversario.y:
					self.y -= 70
				else:
					self.y += 70

				if self.x < avversario.x:
					self.x -= 70
				else:
					self.x += 70


class sopravviviSuPiattaforma:
	def __init__(self, finestra, connessione, schermoAltezza, schermoLarghezza):
		self.FINESTRA = finestra
		self.net = connessione
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Mappa1.jpg")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		self.localPlayer = Giocatore(x=1000, y=300)
		self.testPlayer = Giocatore(x=960, y=540)
		self.remotePlayers = []

		self.SCREENHEIGHT = schermoAltezza
		self.SCREENWIDTH = schermoLarghezza

		self.esecuzioneInCorso = True

	def main(self):
		while self.esecuzioneInCorso:
			pygame.time.delay(20)
			##############################################################################
			#	Gestione multi-player
			##############################################################################
			remotePos = self.net.send(encode_pos((self.localPlayer.x, self.localPlayer.y, int(self.localPlayer.rivoltoDestra), int(self.localPlayer.ancoraVivo))))	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
			if remotePos:
				remotePos = split_pos(remotePos)
			else:
				pass
				
			#	Se si ricevono più posizioni di quelle rappresentate su schermo aggiungere altri giocatori sullo schermo
			conGioc = 0
			for i in remotePos:
				if i != "0,0,0,0":
					conGioc += 1

			for i in range(conGioc - len(self.remotePlayers)):
				self.remotePlayers.append(Giocatore(x=1, y=1))

			#	Modificare posizione giocatori remoti
			for remotePlayer, pos in zip(self.remotePlayers, remotePos):
				if pos:
					remotePlayer.x = decode_pos(pos)[0]
					remotePlayer.y = decode_pos(pos)[1]
					remotePlayer.rivoltoDestra = decode_pos(pos)[2]
					remotePlayer.ancoraVivo = decode_pos(pos)[3]

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

			##############################################################################
			#   Listener per spegnere il gioco quando clicchi sulla
			#   x rossa
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.esecuzioneInCorso = False

			##############################################################################
			#
			##############################################################################

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzioneInCorso = False

			##############################################################################
			#	To do:
			#	Usare la funzione collisione di sopra
			#	su tutti i giocatori:
			#	ogni giocatore deve verificare che non vi siano
			#	collisioni con tutti gli altri giocatori
			#	singolarmente
			##############################################################################

			for giocatore in self.remotePlayers:
				self.localPlayer.collisione(giocatore)

			if self.localPlayer.ancoraVivo:	#	visualizzare e permettere il movimento solo ai giocatori che non sono usciti dal cerchio
				self.localPlayer.muovi(keys, self.SCREENHEIGHT, self.SCREENWIDTH)
				self.localPlayer.disegna(self.FINESTRA)
				if (self.localPlayer.x - 960)**2 + (self.localPlayer.y - 540)**2 > 425**2:	#	verificare che il giocatore sia all'interno del cerchio (piattaforma)
					self.localPlayer.ancoraVivo = False
					print("x: " + str(self.localPlayer.x) + " y: " + str(self.localPlayer.y))

			for remotePlayer in self.remotePlayers:
				if remotePlayer.ancoraVivo:
					remotePlayer.disegna(self.FINESTRA)

			pygame.display.update()