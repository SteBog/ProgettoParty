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

PERCORSO = os.path.realpath(__file__)[:-20]

class Giocatore:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.HEIGHT = 278 // 3
		self.WIDTH = 193 // 3
		self.immagini = []
		for i in range(0, 12):
			if i < 10:
				percorso_frame = PERCORSO + "/Gioco/Immagini/w_p1/Wraith_01_Moving Forward_00" + str(i) + ".png"
			else:
				percorso_frame = PERCORSO + "/Gioco/Immagini/w_p1/Wraith_01_Moving Forward_0" + str(i) + ".png"
			self.immagini.append(pygame.image.load(percorso_frame))
			self.immagini[i] = pygame.transform.scale(self.immagini[i], (self.WIDTH, self.HEIGHT))
		self.rivolto_destra = True
		self.velocita = 10
		self.ancora_vivo = False
		self.index_animation = 0
		self.numero_giocatore = 0
		self.rettangolo_collisione = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
		

	def disegna(self, finestra):
		if self.index_animation < 11:
			self.index_animation += 1
		elif self.index_animation >= 11:
			self.index_animation = 0

		self.rettangolo_collisione = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

		if self.rivolto_destra:
			finestra.blit(self.immagini[self.index_animation], (self.x, self.y))
		else:
			finestra.blit(pygame.transform.flip(self.immagini[self.index_animation], True, False), (self.x, self.y)) #   Se sta andando a sinistra flippa l'immagine prima di "stamparla"

	def muovi(self, tasti, screen_height, screen_width):
		#   Evitare che la velocità in diagonale sia (10^2 + 10^2)^1/2 ma renderla 10 (come in orizzontale e verticale)
		if (tasti[pygame.K_UP] or tasti[pygame.K_DOWN]) and (tasti[pygame.K_LEFT] or tasti[pygame.K_RIGHT]):
			self.velocita = 7
		else:
			self.velocita = 10

		#   A seconda del tasto premuto muovere il giocatore
		if tasti[pygame.K_UP] and self.y >= 0:
			self.y -= self.velocita

		if tasti[pygame.K_DOWN] and self.y <= screen_height - self.HEIGHT:
			self.y += self.velocita

		if tasti[pygame.K_LEFT] and self.x >= 0:
			self.x -= self.velocita

			if self.rivolto_destra:
				self.rivolto_destra = False

		if tasti[pygame.K_RIGHT] and self.x <= screen_width - self.WIDTH:
			self.x += self.velocita

			if not self.rivolto_destra:
				self.rivolto_destra = True

	def collisione(self, avversario):
		if self.rettangolo_collisione.colliderect(avversario.rettangolo_collisione):
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

class SpintoniSuPiattaforma:
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza):
		self.NET = connessione

		self.FINESTRA = finestra
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Mappa1.jpg")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		self.local_player = Giocatore(x=1000, y=300)
		self.local_player.ancora_vivo = True
		self.remote_players = [Giocatore(x=0, y=0), Giocatore(x=0, y=0), Giocatore(x=0, y=0)]

		self.SCREEN_HEIGHT = schermo_altezza
		self.SCREEN_WIDTH = schermo_larghezza

		self.esecuzione_in_corso = True

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			##############################################################################
			#	Gestione multi-player
			##############################################################################
			remotePos = self.NET.send(encode_pos((self.local_player.x, self.local_player.y, int(self.local_player.rivolto_destra), int(self.local_player.ancora_vivo), 0)))	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
			if remotePos:
				self.local_player.numero_giocatore = remotePos[0]
				remotePos = remotePos[1:]
				remotePos = split_pos(remotePos)
			else:
				remotePos = []

			#	Modificare posizione giocatori remoti
			for remote_player, pos in zip(self.remote_players, remotePos):
				if pos:
					remote_player.x = decode_pos(pos)[0]
					remote_player.y = decode_pos(pos)[1]
					remote_player.rivolto_destra = decode_pos(pos)[2]
					remote_player.ancora_vivo = decode_pos(pos)[3]
					remote_player.numero_giocatore = decode_pos(pos)[4]

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

			##############################################################################
			#	Visualizzare e muovere solo i giocatori ancora vivi
			##############################################################################

			for giocatore in self.remote_players:
				self.local_player.collisione(giocatore)

			if self.local_player.ancora_vivo:
				self.local_player.muovi(keys, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
				self.local_player.disegna(self.FINESTRA)
				if (self.local_player.x - 960)**2 + (self.local_player.y - 540)**2 > 425**2:	#	verificare che il giocatore sia all'interno del cerchio (piattaforma)
					self.local_player.ancora_vivo = False

			for remote_player in self.remote_players:
				if remote_player.ancora_vivo:
					remote_player.disegna(self.FINESTRA)

			pygame.display.update()

class GiocatorePong(Giocatore):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.meta_campo = None
	
	def muovi(self, tasti, screen_height, screen_width):
		if self.meta_campo == "sx":
			x_minimo = 0
			x_massimo = 0.5
		else:
			x_minimo = 0.5
			x_massimo = 1

		#   Evitare che la velocità in diagonale sia (10^2 + 10^2)^1/2 ma renderla 10 (come in orizzontale e verticale)
		if (tasti[pygame.K_UP] or tasti[pygame.K_DOWN]) and (tasti[pygame.K_LEFT] or tasti[pygame.K_RIGHT]):
			self.velocita = 7*2
		else:
			self.velocita = 10*2

		#   A seconda del tasto premuto muovere il giocatore
		if tasti[pygame.K_UP] and self.y >= 0:
			self.y -= self.velocita

		if tasti[pygame.K_DOWN] and self.y <= screen_height - self.HEIGHT:
			self.y += self.velocita

		if tasti[pygame.K_LEFT] and self.x >= screen_width * x_minimo:
			self.x -= self.velocita

			if self.rivolto_destra:
				self.rivolto_destra = False

		if tasti[pygame.K_RIGHT] and self.x <= screen_width * x_massimo - self.WIDTH:
			self.x += self.velocita

			if not self.rivolto_destra:
				self.rivolto_destra = True

class Pong:
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza):
		self.NET = connessione

		self.FINESTRA = finestra
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Sfondo Beta Pygame.png")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		self.local_player = GiocatorePong(x=200, y=300)
		self.local_player.ancora_vivo = True
		self.remote_players = [GiocatorePong(x=0, y=0), GiocatorePong(x=0, y=0), GiocatorePong(x=0, y=0)]

		self.SCREEN_HEIGHT = schermo_altezza
		self.SCREEN_WIDTH = schermo_larghezza

		self.esecuzione_in_corso = True

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			##############################################################################
			#	Gestione multi-player
			##############################################################################
			remotePos = self.NET.send(encode_pos((self.local_player.x, self.local_player.y, int(self.local_player.rivolto_destra), int(self.local_player.ancora_vivo), 0)))	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
			if remotePos:
				self.local_player.numero_giocatore = remotePos[0]
				remotePos = remotePos[1:]
				remotePos = split_pos(remotePos)
			else:
				remotePos = []

			if int(self.local_player.numero_giocatore) < 2:
				self.local_player.meta_campo = "sx"
			else:
				self.local_player.meta_campo = "dx"
			#	Modificare posizione giocatori remoti
			for remote_player, pos in zip(self.remote_players, remotePos):
				if pos:
					remote_player.x = decode_pos(pos)[0]
					remote_player.y = decode_pos(pos)[1]
					remote_player.rivolto_destra = decode_pos(pos)[2]
					remote_player.ancora_vivo = decode_pos(pos)[3]
					remote_player.numero_giocatore = decode_pos(pos)[4]

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

			##############################################################################
			#	Visualizzare e muovere solo i giocatori ancora vivi
			##############################################################################

			self.local_player.muovi(keys, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
			self.local_player.disegna(self.FINESTRA)

			for remote_player in self.remote_players:
				if remote_player.ancora_vivo:
					remote_player.disegna(self.FINESTRA)

			pygame.display.update()