import pygame
import time
import json
import os

def encode_pos(stringa_json):
	return json.dumps(stringa_json)

def decode_pos(stringa_json):
	return json.loads(stringa_json)

PERCORSO = os.path.realpath(__file__)[:-20]


class Giocatore:
	def __init__(self):
		self.numero_giocatore = -1

		self.x = 0
		self.y = 0

		self.HEIGHT = 92
		self.WIDTH = 64

		self.immagini = []
		for i in range(0, 12):
			if i < 10:
				percorso_frame = PERCORSO + "/Gioco/Immagini/w_p1/Wraith_01_Moving Forward_00" + str(i) + ".png"
			else:
				percorso_frame = PERCORSO + "/Gioco/Immagini/w_p1/Wraith_01_Moving Forward_0" + str(i) + ".png"
			self.immagini.append(pygame.image.load(percorso_frame))
			self.immagini[i] = pygame.transform.scale(self.immagini[i], (self.WIDTH, self.HEIGHT))
		self.rettangolo_collisione = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

		self.rivolto_destra = False
		self.velocita = 10
		self.ancora_vivo = True
		self.pronto = False
		self.index_animation = 0
		self.punti = 0

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
	def __init__(self, finestra, connessione, altezza_schermo, larghezza_schermo, numero_giocatore):
		self.FINESTRA = finestra
		self.NET = connessione
		self.SCREEN_HEIGHT = altezza_schermo
		self.SCREEN_WIDTH = larghezza_schermo

		self.giocatori = [Giocatore(), Giocatore(), Giocatore(), Giocatore()]
		self.numero_giocatore = int(numero_giocatore)

		self.esecuzione_in_corso = True

		self.info = {
			"minigioco": None,
			"vincitore": None
		}

	def player_to_dictionary(self, giocatore):
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

	def scarica_dati_da_server(self):
		ping = time.perf_counter_ns()
		dati_server = self.NET.send(encode_pos({"giocatore": self.player_to_dictionary(self.giocatori[int(self.numero_giocatore)]), "info": self.info}))	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
		ping = time.perf_counter_ns() - ping	#	latenza espressa in nano secondi

		if dati_server:
			dati_server = decode_pos(dati_server)
		else:
			dati_server = None

		return dati_server

	def aggiorna_giocatori(self):
		dati = self.scarica_dati_da_server()
		self.numero_giocatore = dati["info"]["numero_giocatore"]
		self.info["vincitore"] = dati["info"]["vincitore"]
		for i, giocatori in enumerate(dati["giocatori"]):
			self.giocatori[i].numero_giocatore = int(giocatori["numero_giocatore"])
			if giocatori["numero_giocatore"] != dati["info"]["numero_giocatore"]:
				self.giocatori[i].x = giocatori["coordinata_x"]
				self.giocatori[i].y = giocatori["coordinata_y"]
				self.giocatori[i].rivolto_destra = giocatori["rivolto_a_destra"]
				self.giocatori[i].ancora_vivo = giocatori["ancora_vivo"]
				self.giocatori[i].pronto = giocatori["pronto"]
				self.giocatori[i].punti = giocatori["punti"]

	def high_latency_warning(self, ping):
		if ping // 1000000 > 60:
			self.count_high_ping += 1
		else:
			self.count_high_ping = 0

		if self.count_high_ping > 60:
			self.FINESTRA.blit(self.IMMAGINE_LATENZA_ELEVATA, (1700, 100))
			self.FINESTRA.blit(self.LABEL_LATENZA_ELEVATA, (1630, 250))

	def tutti_pronti(self):
		pronti = True
		for giocatore in self.giocatori:
			if not giocatore.pronto: pronti = False
		return pronti

	def num_ancora_vivi(self):
		numero = 0
		for giocatore in self.giocatori:
			if giocatore.ancora_vivo: numero += 1
		return numero

class SpintoniSuPiattaforma(MiniGioco):
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore):
		super().__init__(finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore)
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Mappa1.jpg")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		self.giocatori[self.numero_giocatore].x = 650 + (self.numero_giocatore % 2) * 550
		self.giocatori[self.numero_giocatore].y = 250 + (self.numero_giocatore // 2) * 500

		for giocatore in self.giocatori:
			giocatore.rettangolo_collisione = pygame.Rect(giocatore.x, giocatore.y, giocatore.WIDTH, giocatore.HEIGHT)

		self.giocatori[self.numero_giocatore].ancora_vivo = True

		self.info = {
			"minigioco": "Spintoni",
			"vincitore": None
		}

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))
			self.aggiorna_giocatori()

			##############################################################################
			#   Listener per spegnere il gioco 
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.esecuzione_in_corso = False

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzione_in_corso = False
			if keys[pygame.K_SPACE] and not self.giocatori[self.numero_giocatore].pronto: 
				self.giocatori[self.numero_giocatore].pronto = True

			##############################################################################
			#	Muovere il giocatore locale
			##############################################################################

			if self.giocatori[self.numero_giocatore].ancora_vivo and self.tutti_pronti():
				self.giocatori[self.numero_giocatore].muovi(keys, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)

			#	verificare che il giocatore sia all'interno del cerchio (piattaforma)
			if (self.giocatori[self.numero_giocatore].x - 960)**2 + (self.giocatori[self.numero_giocatore].y - 540)**2 > 425**2:
				self.giocatori[self.numero_giocatore].ancora_vivo = False

			##############################################################################
			#	Controllare collisioni
			##############################################################################

			for giocatore in self.giocatori:
				if giocatore.numero_giocatore != self.numero_giocatore:
					self.giocatori[self.numero_giocatore].collisione(giocatore)

			##############################################################################
			#	Disegnare i giocatori sul campo
			##############################################################################

			for giocatore in self.giocatori:
				if giocatore.numero_giocatore != -1 and giocatore.ancora_vivo:
					giocatore.disegna(self.FINESTRA)

			##############################################################################
			#	Uscire dal minigioco e restituire il vincitore
			##############################################################################

			if self.info["vincitore"]:
				self.esecuzione_in_corso = False
				return self.numero_giocatore

			if self.tutti_pronti() and self.num_ancora_vivi() < 2:
				self.info = {
					"minigioco": "Spintoni",
					"vincitore": self.numero_giocatore
				}

			pygame.display.update()


class GiocatoreGara(Giocatore):
	def __init__(self):
		super().__init__()
		self.ultimo_tasto = None
		self.rivolto_destra = True

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
		super().__init__(finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore)
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Sfondo Beta Pygame.png")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		self.giocatori = [GiocatoreGara(), GiocatoreGara(), GiocatoreGara(), GiocatoreGara()]
		self.giocatori[self.numero_giocatore].x = 150
		self.giocatori[self.numero_giocatore].y = 200 + 200 * (self.numero_giocatore % 4)

		self.TRAGUARDO = 1300

		self.info = {
			"minigioco": "Gara",
			"vincitore": None
		}

	def tutti_ancora_in_gara(self):
		for giocatore in self.giocatori:
			if giocatore.x >= self.TRAGUARDO:
				return False
		return True

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))
			self.aggiorna_giocatori()

			##############################################################################
			#   Listener per spegnere il gioco 
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.esecuzione_in_corso = False

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzione_in_corso = False
			if keys[pygame.K_SPACE] and not self.giocatori[self.numero_giocatore].pronto: 
				self.giocatori[self.numero_giocatore].pronto = True

			##############################################################################
			#	Muovere il giocatore locale
			##############################################################################

			if self.tutti_pronti():
				self.giocatori[self.numero_giocatore].muovi(keys)

			##############################################################################
			#	Disegnare i giocatori sul campo
			##############################################################################

			for giocatore in self.giocatori:
				if giocatore.numero_giocatore != -1:
					giocatore.disegna(self.FINESTRA)

			##############################################################################
			#	Uscire dal minigioco e restituire il vincitore
			##############################################################################

			if self.info["vincitore"]:
				self.esecuzione_in_corso = False
				return self.numero_giocatore

			if self.tutti_pronti() and not self.tutti_ancora_in_gara():
				self.info = {
					"minigioco": "Gara",
					"vincitore": self.numero_giocatore
				}

			pygame.display.update()


class Paracadutismo(MiniGioco):
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore):
		super().__init__(finestra, connessione, schermo_altezza, schermo_larghezza, numero_giocatore)
		self.y_sfondo = 0
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Nuvole/Nuvole.jpg")
		self.IMMAGINE_PARTE_BASSA = pygame.image.load(PERCORSO + "/Gioco/Immagini/Nuvole/Base_Nuvole.png")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, self.y_sfondo))

		self.giocatori = [Giocatore(), Giocatore(), Giocatore(), Giocatore()]
		self.giocatori[self.numero_giocatore].x = 200 + 400 * (self.numero_giocatore % 4)
		self.giocatori[self.numero_giocatore].y = 200
		self.giocatori[self.numero_giocatore].ancora_vivo = True

		self.PUNTEGGIO_MASSIMO = 5000
		self.distanza = 0

		self.info = {
			"minigioco": "Paracadutismo",
			"vincitore": None
		}

	def disegna_parte_bassa(self):
		self.FINESTRA.blit(self.IMMAGINE_PARTE_BASSA, (0, self.PUNTEGGIO_MASSIMO - self.distanza))

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, self.y_sfondo))
			self.disegna_parte_bassa()

			if self.tutti_pronti() and self.distanza < self.PUNTEGGIO_MASSIMO:
				self.distanza += 10
				if self.y_sfondo > -1000:
					self.y_sfondo -= 10
				else:
					self.y_sfondo = 0

				if self.giocatori[self.numero_giocatore].ancora_vivo: 
					self.giocatori[self.numero_giocatore].punti = self.distanza

			self.aggiorna_giocatori()

			##############################################################################
			#   Listener per spegnere il gioco 
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.esecuzione_in_corso = False

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzione_in_corso = False
			if keys[pygame.K_SPACE] and not self.giocatori[self.numero_giocatore].pronto: 
				self.giocatori[self.numero_giocatore].pronto = True
			if keys[pygame.K_RETURN]: 
				self.giocatori[self.numero_giocatore].ancora_vivo = False

			##############################################################################
			#	Muovere il giocatore locale
			##############################################################################

			if not self.giocatori[self.numero_giocatore].ancora_vivo:
				self.giocatori[self.numero_giocatore].y -= 10

			if self.giocatori[self.numero_giocatore].punti > self.PUNTEGGIO_MASSIMO:
				self.giocatori[self.numero_giocatore].ancora_vivo = False
				self.giocatori[self.numero_giocatore].punti = -1

			##############################################################################
			#	Disegnare i giocatori sul campo
			##############################################################################

			for giocatore in self.giocatori:
				if giocatore.numero_giocatore != -1:
					giocatore.disegna(self.FINESTRA)

			##############################################################################
			#	Uscire dal minigioco e restituire il vincitore
			##############################################################################

			if self.info["vincitore"] is not None:
				self.esecuzione_in_corso = False
				return self.numero_giocatore

			pygame.display.update()


class PallinaPong:
	def __init__(self):
		self.x = 1920 // 2
		self.y = 1080 // 2

		self.HEIGHT = 20
		self.WIDTH = 20

		self.IMMAGINE = pygame.image.load(PERCORSO + "/Gioco/Immagini/Palla.png")
		self.IMMAGINE = pygame.transform.scale(self.IMMAGINE, (self.WIDTH, self.HEIGHT))

	def disegna(self, finestra, x, y):
		finestra.blit(self.IMMAGINE, (x, y))

class Pong(MiniGioco):
	def __init__(self, finestra, connessione, altezza_schermo, larghezza_schermo, numero_giocatore):
		super().__init__(finestra, connessione, altezza_schermo, larghezza_schermo, numero_giocatore)
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Mappa_Pong.jpg")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		self.giocatori = [Giocatore(), Giocatore(), Giocatore(), Giocatore()]
		self.pallina = PallinaPong()
		self.giocatori[self.numero_giocatore].x = 650 + (self.numero_giocatore % 2) * 550
		self.giocatori[self.numero_giocatore].y = 250 + (self.numero_giocatore // 2) * 500

		for giocatore in self.giocatori:
			giocatore.rettangolo_collisione = pygame.Rect(giocatore.x, giocatore.y, giocatore.WIDTH, giocatore.HEIGHT)

		self.giocatori[self.numero_giocatore].ancora_vivo = True

		self.info = {
			"minigioco": "Pong",
			"x": 1920 // 2,
			"y": 1080 // 2,
			"vincitore": None
		}

	def aggiorna_giocatori(self):
		dati = self.scarica_dati_da_server()
		self.numero_giocatore = dati["info"]["numero_giocatore"]
		self.info["vincitore"] = dati["info"]["vincitore"]

		try:
			self.info["x"] = dati["info"]["x"]
			self.info["y"] = dati["info"]["y"]
		except:
			self.info["x"] = 0
			self.info["y"] = 0

		for i, giocatori in enumerate(dati["giocatori"]):
			self.giocatori[i].numero_giocatore = int(giocatori["numero_giocatore"])
			if giocatori["numero_giocatore"] != dati["info"]["numero_giocatore"]:
				self.giocatori[i].x = giocatori["coordinata_x"]
				self.giocatori[i].y = giocatori["coordinata_y"]
				self.giocatori[i].rivolto_destra = giocatori["rivolto_a_destra"]
				self.giocatori[i].ancora_vivo = giocatori["ancora_vivo"]
				self.giocatori[i].pronto = giocatori["pronto"]
				self.giocatori[i].punti = giocatori["punti"]

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))
			self.aggiorna_giocatori()

			##############################################################################
			#   Listener per spegnere il gioco 
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.esecuzione_in_corso = False

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzione_in_corso = False
			if keys[pygame.K_SPACE] and not self.giocatori[self.numero_giocatore].pronto: 
				self.giocatori[self.numero_giocatore].pronto = True

			##############################################################################
			#	Muovere il giocatore locale
			##############################################################################

			if self.giocatori[self.numero_giocatore].ancora_vivo:
				self.giocatori[self.numero_giocatore].muovi(keys, self.SCREEN_HEIGHT, self.SCREEN_WIDTH)

			##############################################################################
			#	Controllare collisioni
			##############################################################################

			for giocatore in self.giocatori:
				if giocatore.numero_giocatore != self.numero_giocatore:
					self.giocatori[self.numero_giocatore].collisione(giocatore)

			##############################################################################
			#	Disegnare i giocatori sul campo
			##############################################################################

			for giocatore in self.giocatori:
				if giocatore.numero_giocatore != -1 and giocatore.ancora_vivo:
					giocatore.disegna(self.FINESTRA)

			self.pallina.disegna(self.FINESTRA, self.info["x"], self.info["y"])

			##############################################################################
			#	Uscire dal minigioco e restituire il vincitore
			##############################################################################

			if self.info["vincitore"]:
				self.esecuzione_in_corso = False
				return self.numero_giocatore

			pygame.display.update()
