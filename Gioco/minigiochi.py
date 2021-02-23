import pygame
import os
import json
import time

def player_to_dictionary(giocatore):
	risultato = {
		"numero_giocatore": giocatore.numero_giocatore,
		"coordinata_x": giocatore.x,
		"coordinata_y": giocatore.y,
		"rivolto_a_destra": giocatore.rivolto_destra,
		"ancora_vivo": giocatore.ancora_vivo,
		"pronto": giocatore.pronto,
		"punti": giocatore.punti
	}
	return risultato

def encode_pos(stringa_json):
	return json.dumps(stringa_json)

def decode_pos(stringa_json):
	return json.loads(stringa_json)

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
		self.pronto = False
		self.punti = 0
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
			self.rivolto_destra = False

		if tasti[pygame.K_RIGHT] and self.x <= screen_width - self.WIDTH:
			self.x += self.velocita
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

class MiniGioco:
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza):
		self.NET = connessione
		self.count_high_ping = 0
		self.immagine_latenza_elevata = pygame.image.load(PERCORSO + "/Gioco/Immagini/high_latency.png")
<<<<<<< HEAD
		self.immagine_latenza_elevata = pygame.transform.scale(self.immagine_latenza_elevata, (128, 128))
=======
		self.immagine_latenza_elevata = pygame.transform.scale(self.immagine_latenza_elevata, (70, 65))
>>>>>>> 2bc370ca3ef49168417baaa22f9e4f46989cc577

		self.FINESTRA = finestra

		self.local_player = Giocatore(x=1000, y=300)
		self.local_player.ancora_vivo = True
		self.remote_players = [Giocatore(x=0, y=0), Giocatore(x=0, y=0), Giocatore(x=0, y=0)]

		self.SCREEN_HEIGHT = schermo_altezza
		self.SCREEN_WIDTH = schermo_larghezza

		self.esecuzione_in_corso = True
		self.tutti_pronti = False

		self.info = {
			"minigioco": "None"
		}

	def aggiorna_dati_da_server(self):
		ping = time.perf_counter_ns()
		dati_server = self.NET.send(encode_pos({"giocatore": player_to_dictionary(self.local_player), "info": self.info}))	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
		ping = time.perf_counter_ns() - ping	#	latenza espressa in nano secondi
		self.high_latency_warning(ping)
		if dati_server:
			self.local_player.numero_giocatore = int(dati_server[0])
			dati_server = decode_pos(dati_server[1:])
		else:
			dati_server = None

		index_remote_players = 0
		while index_remote_players < 3:
			if index_remote_players != self.local_player.numero_giocatore:
				self.remote_players[index_remote_players].x = int(dati_server["giocatori"][index_remote_players]["coordinata_x"])
				self.remote_players[index_remote_players].y = int(dati_server["giocatori"][index_remote_players]["coordinata_y"])
				self.remote_players[index_remote_players].rivolto_destra = int(dati_server["giocatori"][index_remote_players]["rivolto_a_destra"])
				self.remote_players[index_remote_players].ancora_vivo = int(dati_server["giocatori"][index_remote_players]["ancora_vivo"])
				self.remote_players[index_remote_players].numero_giocatore = int(dati_server["giocatori"][index_remote_players]["numero_giocatore"])
				self.remote_players[index_remote_players].pronto = int(dati_server["giocatori"][index_remote_players]["pronto"])
				self.remote_players[index_remote_players].punti = int(dati_server["giocatori"][index_remote_players]["punti"])
				self.info = dati_server["info"]
			index_remote_players += 1

	def high_latency_warning(self, ping):
		print(ping // 1000000)
		if ping // 1000000 > 60:
			self.count_high_ping += 1
		else:
			self.count_high_ping = 0

		if self.count_high_ping > 10:
			self.FINESTRA.blit(self.immagine_latenza_elevata, (1700, 100))

	def pronto_check(self, keys):
		if not self.local_player.pronto and keys[pygame.K_SPACE]:
			self.local_player.pronto = True

		if not self.tutti_pronti:
			var_appoggio = 0
			while self.remote_players[var_appoggio].pronto:
				var_appoggio += 1
			if var_appoggio >= len(self.remote_players) and self.local_player.pronto:
				self.tutti_pronti = True


class SpintoniSuPiattaforma(MiniGioco):
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore):
		super().__init__(finestra, connessione, schermo_altezza, schermo_larghezza)
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Mappa1.jpg")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		if int(numero_giocatore) == 0: self.local_player = Giocatore(x=650, y=250)
		elif int(numero_giocatore) == 1: self.local_player = Giocatore(x=1200,y=250)
		elif int(numero_giocatore) == 2: self.local_player = Giocatore(x=650, y=750)
		elif int(numero_giocatore) == 3: self.local_player = Giocatore(x=1200, y=750)

		self.local_player.ancora_vivo = True
		self.local_player.numero_giocatore = int(numero_giocatore)

		self.info = {
			"minigioco": "Spintoni"
		}

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))
			self.aggiorna_dati_da_server()

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
				if giocatore.ancora_vivo:
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
			self.velocita = 7
		else:
			self.velocita = 10

		#   A seconda del tasto premuto muovere il giocatore
		if tasti[pygame.K_UP] and self.y >= 0:
			self.y -= self.velocita

		if tasti[pygame.K_DOWN] and self.y <= screen_height - self.HEIGHT:
			self.y += self.velocita

		if tasti[pygame.K_LEFT] and self.x >= screen_width * x_minimo:
			self.x -= self.velocita
			self.rivolto_destra = False

		if tasti[pygame.K_RIGHT] and self.x <= screen_width * x_massimo - self.WIDTH:
			self.x += self.velocita
			self.rivolto_destra = True

class PallinaPong:
	def __init__(self):
		self.x = 950
		self.y = 530
		self.WIDTH = 20
		self.HEIGHT = 20
		self.velocita = 10
		self.IMMAGINE = pygame.image.load(PERCORSO + "/Gioco/Immagini/Palla.png")
		self.IMMAGINE = pygame.transform.scale(self.IMMAGINE, (self.WIDTH, self.HEIGHT))
		self.direzione_orizzontale = False
		self.direzione_verticale = False
		self.rettangolo_collisione = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

	def disegna(self, finestra):
		self.rettangolo_collisione = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)
		finestra.blit(self.IMMAGINE, (self.x, self.y))

	def muovi(self):
		if self.direzione_orizzontale == 1:
			self.x += self.velocita
		else:
			self.x -= self.velocita

		if self.direzione_verticale == 1:
			self.y -= self.velocita
		elif self.direzione_verticale == -1:
			self.y += self.velocita

	def collisione(self, avversario):
		#	Direzione orizzontale = 1  -> verso destra
		#	Direzione orizzontale = -1 -> verso sinistra

		#	Direzione verticale = 1  -> verso l'alto
		#	Direzione verticale = 0  -> dritto
		#	Direzione verticale = -1 -> verso il basso
		
		if self.rettangolo_collisione.colliderect(avversario.rettangolo_collisione):
			if int(avversario.numero_giocatore) < 2:
				self.direzione_orizzontale = 1
			else:
				self.direzione_orizzontale = -1

			if self.y >= avversario.y - self.HEIGHT and self.y <= avversario.y + 20:
				self.direzione_verticale = 1
			elif self.y <= avversario.y + avversario.HEIGHT and self.y >= avversario.y + avversario.HEIGHT - 20:
				self.direzione_verticale = -1
			else:
				self.direzione_verticale = 0

			self.velocita += 2

	def controlla_bordi(self, schermo_larghezza, schermo_altezza):
		"""
		1  = gol giocatori a sinistra
		-1 = gol giocatori a destra
		0  = no gol
		"""
		if self.y <= 0:
			self.direzione_verticale = -1
		elif self.y >= schermo_altezza - self.HEIGHT:
			self.direzione_verticale = 1
		
		if self.x > schermo_larghezza:
			return 1
		elif self.x < -self.WIDTH:
			return -1
		else:
			return 0

class Pong(MiniGioco):
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore):
		super().__init__(finestra, connessione, schermo_altezza, schermo_larghezza)
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Sfondo Beta Pygame.png")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		if int(numero_giocatore) == 0: self.local_player = GiocatorePong(x=650, y=250)
		elif int(numero_giocatore) == 1: self.local_player = GiocatorePong(x=650, y=750)
		elif int(numero_giocatore) == 2: self.local_player = GiocatorePong(x=1200,y=250)
		elif int(numero_giocatore) == 3: self.local_player = GiocatorePong(x=1200, y=750)
		
		self.local_player.numero_giocatore = int(numero_giocatore)
		self.local_player.ancora_vivo = True

		self.remote_players = [GiocatorePong(0, 0), GiocatorePong(0, 0), GiocatorePong(0, 0)]

		self.pallina = PallinaPong()
		self.punteggio_sinistra = 0
		self.punteggio_destra = 0
		self.FONT = pygame.font.SysFont("comicsans", 50)

		self.info = {
			"minigioco": "Pong"
		}

	def segna_risultato(self, finestra, schermo_larghezza):
		txt_punteggio_sinistra = self.FONT.render(str(self.punteggio_sinistra), 1, (0, 0, 0))
		txt_punteggio_destra = self.FONT.render(str(self.punteggio_destra), 1, (0, 0, 0))
		finestra.blit(txt_punteggio_sinistra, ((schermo_larghezza - txt_punteggio_sinistra.get_width()) // 2 - 20, 30))
		finestra.blit(txt_punteggio_destra, ((schermo_larghezza - txt_punteggio_sinistra.get_width()) // 2 + 20, 30))

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)

			self.aggiorna_dati_da_server()

			if int(self.local_player.numero_giocatore) < 2:
				self.local_player.meta_campo = "sx"
			else:
				self.local_player.meta_campo = "dx"

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

			##############################################################################
			#   Listener per spegnere il gioco quando clicchi sulla
			#   x rossa
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.esecuzione_in_corso = False

			##############################################################################
			#	Listener tasti e spegnimento gioco con Escape
			##############################################################################

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzione_in_corso = False

			##############################################################################
			#	Gestire il proprio giocatore
			##############################################################################

			self.local_player.muovi(keys, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)
			self.local_player.disegna(self.FINESTRA)

			##############################################################################
			#	Gestione pallina, rimbalzo e collisione con giocatori
			##############################################################################

			self.pallina.collisione(self.local_player)
			for remote_player in self.remote_players:
				self.pallina.collisione(remote_player)

			self.pallina.muovi()
			self.pallina.disegna(self.FINESTRA)
			e_gol = self.pallina.controlla_bordi(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
			if e_gol == 1:
				self.punteggio_sinistra += 1
				self.pallina.x = 950
				self.pallina.y = 530
				self.pallina.direzione_orizzontale = -1
				self.pallina.direzione_verticale = 0
			elif e_gol == -1:
				self.punteggio_destra += 1
				self.pallina.x = 950
				self.pallina.y = 530
				self.pallina.direzione_orizzontale = 1
				self.pallina.direzione_verticale = 0

			for remote_player in self.remote_players:
				if remote_player.ancora_vivo:
					remote_player.disegna(self.FINESTRA)

			self.segna_risultato(self.FINESTRA, self.SCREEN_WIDTH)

			pygame.display.update()


class GiocatoreGara(Giocatore):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.ultimo_tasto = None

	def muovi(self, tasti):
		#	ultimo_tasto = 1 -> freccia in su
		#	ultimo_tasto = 0 -> freccia in giu
		if not self.ultimo_tasto == 1 and tasti[pygame.K_UP] and not tasti[pygame.K_DOWN]:
			self.x += 3
			self.ultimo_tasto = 1

		if not self.ultimo_tasto == 0 and tasti[pygame.K_DOWN] and not tasti[pygame.K_UP]:
			self.x += 3
			self.ultimo_tasto = 0

class Gara(MiniGioco):
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore):
		super().__init__(finestra, connessione, schermo_altezza, schermo_larghezza)
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Sfondo Beta Pygame.png")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		if int(numero_giocatore) == 0: self.local_player = GiocatoreGara(x=150, y=200)
		elif int(numero_giocatore) == 1: self.local_player = GiocatoreGara(x=150, y=500)
		elif int(numero_giocatore) == 2: self.local_player = GiocatoreGara(x=150,y=800)
		elif int(numero_giocatore) == 3: self.local_player = GiocatoreGara(x=150, y=1100)

		self.local_player.ancora_vivo = True
		self.remote_players = [GiocatoreGara(0, 0), GiocatoreGara(0, 0), GiocatoreGara(0, 0)]

		self.info = {
			"minigioco": "Gara"
		}

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)

			self.aggiorna_dati_da_server()

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
			#	Visualizzare e muovere solo i giocatori connessi e pronti
			##############################################################################

			self.local_player.muovi(keys)
			self.local_player.disegna(self.FINESTRA)

			for remote_player in self.remote_players:
				if remote_player.ancora_vivo:
					remote_player.disegna(self.FINESTRA)

			pygame.display.update()


class GiocatoreBN(Giocatore):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.casella_squadra = 0	#	su quale casella del proprio campo si trova

	def muovi(self, tasti):
		if tasti[pygame.K_UP] and self.casella_squadra > 3:
			self.casella_squadra -= 4
			self.y -= 150
			
		if tasti[pygame.K_DOWN] and self.casella_squadra < 12:
			self.casella_squadra += 4
			self.y += 150

		if tasti[pygame.K_LEFT] and self.casella_squadra % 4 != 0:
			self.casella_squadra -= 1
			self.x -= 150

		if tasti[pygame.K_RIGHT] and self.casella_squadra % 4 != 3:
			self.casella_squadra += 1
			self.x += 150


class BattagliaNavale(MiniGioco):
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore):
		super().__init__(finestra, connessione, schermo_altezza, schermo_larghezza)
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Sfondo Beta Pygame.png")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		if int(numero_giocatore) % 2 == 0: 
			self.local_player = GiocatoreBN(x=218, y=204)
			self.local_player.casella_squadra = 0
		elif int(numero_giocatore) % 2 == 1:
			self.local_player = GiocatoreBN(x=218, y=654)
			self.local_player.casella_squadra = 12

		self.local_player.ancora_vivo = True
		self.local_player.numero_giocatore = numero_giocatore

		self.remote_players = [GiocatoreBN(0, 0), GiocatoreBN(0, 0), GiocatoreBN(0, 0)]

		self.info = {
			"minigioco": "BattagliaNavale",
			"celle_avversari": [0 for _ in range(16)],
			"casella_giocatore": self.local_player.casella_squadra,
			"turno": 0,
			"scelta": -1
		}
		self.scelta = 0
		self.disegna_celle()

	def disegna_celle(self):
		for i in range(4):
			for j in range(4):
				pygame.draw.rect(self.FINESTRA, (0, 0, 0), pygame.Rect(150 * i + 200, 150 * j + 200, 100, 100))
		for i in range(16):
			if self.info["celle_avversari"][i] == 0:
				pygame.draw.rect(self.FINESTRA, (0, 0, 0), pygame.Rect(150 * (i % 4) + 1170, 150 * (i // 4) + 200, 100, 100))
			if self.info["celle_avversari"][i] == 1:
				pygame.draw.rect(self.FINESTRA, (0, 0, 255), pygame.Rect(150 * (i % 4) + 1170, 150 * (i // 4) + 200, 100, 100))
			if self.info["celle_avversari"][i] == 2:
				pygame.draw.rect(self.FINESTRA, (255, 0, 0), pygame.Rect(150 * (i % 4) + 1170, 150 * (i // 4) + 200, 100, 100))

	def attacca(self, tasti):
		if tasti[pygame.K_UP] and self.scelta > 3:
			self.scelta -= 4
			
		if tasti[pygame.K_DOWN] and self.scelta < 12:
			self.scelta += 4

		if tasti[pygame.K_LEFT] and self.scelta % 4 != 0:
			self.scelta -= 1

		if tasti[pygame.K_RIGHT] and self.scelta % 4 != 3:
			self.scelta += 1

		pygame.draw.rect(self.FINESTRA, (255, 0, 0), pygame.Rect(150 * (self.scelta % 4) + 1170, 150 * (self.scelta // 4) + 200, 100, 100))

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			
			self.aggiorna_dati_da_server()

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))
			self.disegna_celle()

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
			if keys[pygame.K_SPACE]: self.tutti_pronti = True

			if self.tutti_pronti:
				self.attacca(keys)
				if (self.local_player.numero_giocatore < 2 and self.info["turno"] == 0) or (self.local_player.numero_giocatore >= 2 and self.info["turno"] == 1):
					if keys[pygame.K_RETURN] and not self.info["celle_avversari"][self.scelta]:
						self.info["scelta"] = self.scelta
			else:
				self.local_player.muovi(keys)

			self.local_player.disegna(self.FINESTRA)

			for remote_player in self.remote_players:
				if remote_player.ancora_vivo:
					remote_player.disegna(self.FINESTRA)

			pygame.display.update()


class GiocatoreParacadutismo(Giocatore):
	def muovi(self):
		self.y -= 10

class Paracadutismo(MiniGioco):
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore):
		super().__init__(finestra, connessione, schermo_altezza, schermo_larghezza)
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Sfondo Beta Pygame.png")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		if int(numero_giocatore) == 0: self.local_player = GiocatoreParacadutismo(x=200, y=200)
		elif int(numero_giocatore) == 1: self.local_player = GiocatoreParacadutismo(x=600, y=200)
		elif int(numero_giocatore) == 2: self.local_player = GiocatoreParacadutismo(x=1000,y=200)
		elif int(numero_giocatore) == 3: self.local_player = GiocatoreParacadutismo(x=1400, y=200)

		self.local_player.ancora_vivo = True
		self.local_player.numero_giocatore = numero_giocatore

		self.remote_players = [GiocatoreParacadutismo(0, 0), GiocatoreParacadutismo(0, 0), GiocatoreParacadutismo(0, 0)]

		self.ancora_in_volo = True
		self.PUNTEGGIO_MASSIMO = 100000000

		self.info = {
			"minigioco": "Paracadutismo"
		}

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			self.local_player.punti += 30

			self.aggiorna_dati_da_server()

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

			if keys[pygame.K_SPACE]:
				self.ancora_in_volo = False

			if self.local_player.punti > self.PUNTEGGIO_MASSIMO:
				self.local_player.ancora_vivo = False

			if not self.ancora_in_volo: self.local_player.muovi()
			self.local_player.disegna(self.FINESTRA)

			for remote_player in self.remote_players:
				if remote_player.ancora_vivo:
					remote_player.disegna(self.FINESTRA)

			pygame.display.update()