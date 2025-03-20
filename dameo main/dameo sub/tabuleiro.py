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
            self.board.append([])  # Cria uma linha (lista vazia)
            for COLUNA in range(COLUNAS):
                # Primeira linha: todas as colunas preenchidas
                if LINHA == 0:
                    self.board[LINHA].append(Peças(LINHA, COLUNA, VERDE))
                # Segunda linha: n-1 peças
                elif LINHA == 1 and 0 < COLUNA < COLUNAS - 1:
                    self.board[LINHA].append(Peças(LINHA, COLUNA, VERDE))
                # Terceira linha: n-2 peças
                elif LINHA == 2 and 1 < COLUNA < COLUNAS - 2:
                    self.board[LINHA].append(Peças(LINHA, COLUNA, VERDE))
                # Antepenúltima linha: n-2 peças
                elif LINHA == LINHAS - 3 and 1 < COLUNA < COLUNAS - 2:
                    self.board[LINHA].append(Peças(LINHA, COLUNA, LARANJA))
                # Penúltima linha: n-1 peças
                elif LINHA == LINHAS - 2 and 0 < COLUNA < COLUNAS - 1:
                    self.board[LINHA].append(Peças(LINHA, COLUNA, LARANJA))
                # Última linha: todas as colunas preenchidas
                elif LINHA == LINHAS - 1:
                    self.board[LINHA].append(Peças(LINHA, COLUNA, LARANJA))
                else:
                    self.board[LINHA].append(0)  # Espaço vazio


    def desenhar(self,win): 
        self.draw_quadrados(win)
        for LINHA in range(LINHAS):
            for COLUNA in range(COLUNAS):
                peças = self.board[LINHA][COLUNA]
                if peças != 0:
                    peças.draw(win)
