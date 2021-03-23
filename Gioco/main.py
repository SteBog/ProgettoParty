import pygame
import os
from Network import Connessione
from SchermataPrincipale import *

pygame.init()

if __name__ == "__main__":
	FINESTRA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

	PERCORSO = os.path.realpath(__file__)[:-14]
	SFONDO_SCHERMATA_PRINCIPALE = pygame.image.load(PERCORSO + "/Gioco/Immagini/Home.jpg")
	FINESTRA.blit(SFONDO_SCHERMATA_PRINCIPALE, (0, 0))

	click = False
	NET = Connessione()

	while True:
		pygame.time.delay(20)
		FINESTRA.blit(SFONDO_SCHERMATA_PRINCIPALE, (0, 0))
		mouse_x, mouse_y = pygame.mouse.get_pos()
		pulsante_1 = pygame.Rect(100, 100, 100, 30)

		if pulsante_1.collidepoint((mouse_x, mouse_y)):
			if click:
				minigioco = Schermata_Principale(FINESTRA, NET, SCREEN_HEIGHT, SCREEN_WIDTH)
				minigioco.main()

		pygame.draw.rect(FINESTRA, (0, 0, 255), pulsante_1)

		click = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()

		pygame.display.update()