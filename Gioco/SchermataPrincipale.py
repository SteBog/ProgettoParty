import pygame
import os
from minigiochi import *


PERCORSO = os.path.realpath(__file__)[:-29]

class Schermata_Principale:
	def __init__(self, finestra, connessione, schermo_altezza, schermo_larghezza):
		self.NET = connessione

		self.FINESTRA = finestra
		self.IMMAGINE_SFONDO = pygame.image.load(PERCORSO + "/Gioco/Immagini/Campo_Final_Spikes.jpg")
		self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

		self.SCREEN_HEIGHT = schermo_altezza
		self.SCREEN_WIDTH = schermo_larghezza

		self.esecuzione_in_corso = True
		self.numero_giocatore = None

		self.posizione_local = 0
		self.numero_minigioco = 0
		self.posizioni = [(10, 925), (90, 600), (240, 275), (380, 550), (616, 746), (850, 602), (724, 458), (561, 314), (814, 170), (1030, 350), (1030, 656), (1264, 818), (1498, 404)]

		self.giocatori = [Giocatore(), Giocatore(), Giocatore(), Giocatore()]
		self.numero_giocatore = -1

		#	Giocatore w: 64, h: 92 
		#	Posizione 1: 10, 925 (418)
		#	Posizione 2: 90, 600
		#	Posizione 3: 240, 275
		#	Posizione 4: 380, 550
		#	Posizione 5: 616, 746
		#	Posizione 6: 850, 602
		#	Posizione 7: 724, 458
		#	Posizione 8: 561, 314
		#	Posizione 9: 814, 170
		#	Posizione10: 1030, 350
		#	Posizione11: 1030, 656
		#	Posizione12: 1264, 818
		#	Posizione13: 1498, 404

	def scarica_dati_da_server(self):
		ping = time.perf_counter_ns()
		dati_server = self.NET.send('{"giocatore": {"numero_giocatore": -1, "coordinata_x": 0, "coordinata_y": 0, "rivolto_a_destra": 0, "ancora_vivo": 1, "pronto": 0, "punti": 0}, "info": {"minigioco": "Home", "vincitore": null}}')	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
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

	def main(self):
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			self.aggiorna_giocatori()

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

			self.giocatori[self.numero_giocatore].x = self.posizioni[self.numero_minigioco][0]
			self.giocatori[self.numero_giocatore].y = self.posizioni[self.numero_minigioco][1]

			if self.numero_minigioco % 4 == 0:
				minigioco = SpintoniSuPiattaforma(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
			if self.numero_minigioco % 4 == 1:
				minigioco = Pong(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
			if self.numero_minigioco % 4 == 2:
				minigioco = Gara(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
			if self.numero_minigioco % 4 == 3:
				minigioco = Paracadutismo(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)

			vincitori = minigioco.main()

			for vincitore in vincitori:
				if vincitore == self.numero_giocatore:
					self.numero_minigioco += 1

			##############################################################################
			#   Listener per spegnere il gioco quando clicchi sulla
			#   x rossa
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

			##############################################################################
			#
			##############################################################################

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzione_in_corso = False

			for giocatore in self.giocatori:
				if giocatore.ancora_vivo:
					giocatore.disegna(self.FINESTRA)

			pygame.display.update()
