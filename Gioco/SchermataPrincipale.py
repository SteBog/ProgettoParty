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

		self.local_player = Giocatore()

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

		self.index_posizione = 0
		self.spostare = False
	def spostamento_1_2(self):
		if self.local_player.y > 418:
			self.local_player.y -= 10
		else:
			self.spostare = False

	def main(self):
		click = False
		while self.esecuzione_in_corso:
			pygame.time.delay(20)
			remotePos = self.NET.send('{"giocatore": {"numero_giocatore": 0, "coordinata_x": 0, "coordinata_y": 0, "rivolto_a_destra": 0, "ancora_vivo": 1, "pronto": 0, "punti": 0}, "info": {"minigioco": "Home", "vincitore": null}}')	#	Invio posizione giocatore locale e ricezione posizione altri giocatori
			if remotePos:
				remotePos = decode_pos(remotePos)
				self.numero_giocatore = remotePos["info"]["numero_giocatore"]

			self.FINESTRA.blit(self.IMMAGINE_SFONDO, (0, 0))
			mouse_x, mouse_y = pygame.mouse.get_pos()
			pulsante_minigioco_1 = pygame.Rect(100, 100, 100, 30)
			pulsante_minigioco_2 = pygame.Rect(300, 100, 100, 30)
			pulsante_minigioco_3 = pygame.Rect(500, 100, 100, 30)
			pulsante_minigioco_4 = pygame.Rect(700, 100, 100, 30)

			if pulsante_minigioco_1.collidepoint((mouse_x, mouse_y)):
				if click:
					minigioco = SpintoniSuPiattaforma(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
					vincitore = minigioco.main()
			if pulsante_minigioco_2.collidepoint((mouse_x, mouse_y)):
				if click:
					minigioco = Pong(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
					minigioco.main()
			if pulsante_minigioco_3.collidepoint((mouse_x, mouse_y)):
				if click:
					minigioco = Gara(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
					minigioco.main()
			if pulsante_minigioco_4.collidepoint((mouse_x, mouse_y)):
				if click:
					minigioco = Paracadutismo(self.FINESTRA, self.NET, self.SCREEN_HEIGHT, self.SCREEN_WIDTH, self.numero_giocatore)
					minigioco.main()

			click = False

			pygame.draw.rect(self.FINESTRA, (0, 0, 0), pulsante_minigioco_1)
			pygame.draw.rect(self.FINESTRA, (0, 0, 0), pulsante_minigioco_2)
			pygame.draw.rect(self.FINESTRA, (0, 0, 0), pulsante_minigioco_3)
			pygame.draw.rect(self.FINESTRA, (0, 0, 0), pulsante_minigioco_4)

			##############################################################################
			#   Listener per spegnere il gioco quando clicchi sulla
			#   x rossa
			##############################################################################

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						click = True

			##############################################################################
			#
			##############################################################################

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]: self.esecuzione_in_corso = False
			if keys[pygame.K_SPACE]:
				self.spostare = True
			
			if self.spostare: self.spostamento_1_2()

			self.local_player.disegna(self.FINESTRA)

			pygame.display.update()
