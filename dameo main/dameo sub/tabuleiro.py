import pygame
from .constants import CINZA, LINHAS, BRANCO ,TAMANHO_QUADRADO, COLUNAS, LARANJA, VERDE
from .peças import Peças

class Tabuleiro:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.verdes_left = self.laranjas_left = 18
        self.verdes_kings = self.laranjas_kings = 0
        self.create_tabuleiro()

    def draw_quadrados(self,win):
        win.fill(CINZA)
        for  LINHA in range(LINHAS):
            for COLUNA in range(LINHA%2, COLUNAS, 2):
                pygame.draw.rect(win, BRANCO, (LINHA*TAMANHO_QUADRADO, COLUNA*TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

    def create_tabuleiro(self):
        for LINHA in range(LINHAS):
            self.board.append([]) #cria uma linha a cada iteraçao (lista vazia)
            for COLUNA in range(COLUNAS):
                if LINHA < 3:
                    if (LINHA == 0) or (LINHA == 1 and 1 <= COLUNA <= TAMANHO_QUADRADO-1) or (LINHA == 2 and 2 <= COLUNA <= TAMANHO_QUADRADO-2):
                        self.board[LINHA].append(Peças(LINHA,COLUNA,VERDE))  # V for Verdes
                    else:
                        self.board[LINHA].append(0)
                elif LINHA > 4:
                    if (LINHA == TAMANHO_QUADRADO-1) or (LINHA == TAMANHO_QUADRADO-2 and 1 <= COLUNA <= TAMANHO_QUADRADO-2) or (LINHA == TAMANHO_QUADRADO-3 and 2 <= COLUNA <= TAMANHO_QUADRADO-3):
                        self.board[LINHA].append(Peças(LINHA,COLUNA,LARANJA))  # L for Laranjas
                    else:
                        self.board[LINHA].append(0)
                else:
                    self.board[LINHA].append(0)
    
    def desenhar(self,win): 
        self.draw_quadrados(win)
        for LINHA in range(LINHAS):
            for COLUNA in range(COLUNAS):
                peças = self.board[LINHA][COLUNA]
                if peças != 0:
                    peças.draw(win)
