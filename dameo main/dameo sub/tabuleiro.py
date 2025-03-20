import pygame
from .constants import CINZA, LINHAS, BRANCO ,TAMANHO_QUADRADO

class Tabuleiro:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.verdes_left = self.laranjas_left = 18
        self.verdes_kings = self.laranjas_kings = 0

    def draw_quadrados(self,win):
        win.fill(CINZA)
        for  LINHA in range(LINHAS):
            for COLUNA in range(LINHA%2, LINHAS, 2):
                pygame.draw.rect(win, BRANCO, (LINHA*TAMANHO_QUADRADO, COLUNA*TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
