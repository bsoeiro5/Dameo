import pygame
from constants import CINZA, LINHAS, BRANCO

class Tabuleiro:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.verdes_left = self.laranjas_left = 18
        self.verdes_kings = self.laranjas_kings = 0

    def draw_quadrados(self,win):
        win.fill(CINZA)
        for  LINHA in range(LINHAS):
            for COLUNA in range(LINHAS):
                if LINHA % 2 == 0 and COLUNA % 2 != 0:
                    pygame.draw.rect(win, BRANCO, (LINHA*100, COLUNA*100, 100, 100))
                elif LINHA % 2 != 0 and COLUNA % 2 == 0:
                    pygame.draw.rect(win, BRANCO, (LINHA*100, COLUNA*100, 100, 100))
