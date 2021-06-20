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

		self.info = {
			"minigioco": "home",
			"vincitore": None,
			"vincitore_partita": None,
			"ID_Utente": 1
		}

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
		dati_server = ""
		dati_server = self.NET.send(encode_pos({"giocatore": self.player_to_dictionary(self.giocatori[int(self.numero_giocatore)]), "info": self.info}))	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
		ping = time.perf_counter_ns() - ping	#	latenza espressa in nano secondi

		if dati_server:
			dati_server = decode_pos(dati_server)

		return dati_server

	def aggiorna_giocatori(self):
		dati = self.scarica_dati_da_server()
		if dati is None or dati == "" or dati["info"]["vincitore_partita"]:
			self.esecuzione_in_corso = False
			return 0

		self.numero_giocatore = dati["info"]["numero_giocatore"]
		self.numero_minigioco = dati["info"]["minigioco"]

		for i, giocatori in enumerate(dati["giocatori"]):
			self.giocatori[i].numero_giocatore = int(giocatori["numero_giocatore"])
			self.giocatori[i].personaggio = giocatori["personaggio"]
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
			if self.aggiorna_giocatori() == 0: break

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))

			if self.giocatori[self.numero_giocatore].pronto:
				self.giocatori[self.numero_giocatore].disegna_pronto(self.FINESTRA)

			if self.numero_minigioco is not None:
				minigioco_di_coppia = False
				if self.numero_minigioco % 4 == 0:
					minigioco = SpintoniSuPiattaforma(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
				if self.numero_minigioco % 4 == 1:
					minigioco = Pong(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
					minigioco_di_coppia = True
				if self.numero_minigioco % 4 == 2:
					minigioco = Gara(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
				if self.numero_minigioco % 4 == 3:
					minigioco = Paracadutismo(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)

				vincitori = minigioco.main()

				if vincitori is not None:
					self.giocatori[self.numero_giocatore].pronto = False
					if vincitori[0] == self.numero_giocatore:
						self.posizione_local += 1
						self.giocatori[self.numero_giocatore].x = self.posizioni[self.posizione_local][0]
						self.giocatori[self.numero_giocatore].y = self.posizioni[self.posizione_local][1]

					if minigioco_di_coppia and vincitori[1] == self.numero_giocatore:
						self.posizione_local += 1
						self.giocatori[self.numero_giocatore].x = self.posizioni[self.posizione_local][0]
						self.giocatori[self.numero_giocatore].y = self.posizioni[self.posizione_local][1]

					vincitori = None
					self.info["vincitore"] = None

					if self.posizione_local == 12: self.info["vincitore_partita"] = self.numero_giocatore

				print(f"Numero: {self.numero_giocatore} - posizione: {self.posizione_local}")

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
			if keys[pygame.K_SPACE] and not self.giocatori[self.numero_giocatore].pronto: 
				self.giocatori[self.numero_giocatore].pronto = True

			for giocatore in self.giocatori:
				if len(giocatore.immagini) == 0 and giocatore.personaggio is not None:
					giocatore.carica_immagini(giocatore.personaggio)

			for giocatore in self.giocatori:
				if giocatore.ancora_vivo and giocatore.numero_giocatore != -1:
					giocatore.disegna(self.FINESTRA)

			pygame.display.update()

