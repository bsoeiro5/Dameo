import pygame
from .constants import CINZA, LINHAS, BRANCO ,TAMANHO_QUADRADO, COLUNAS, LARANJA, VERDE, PRETO, ALTURA
from .peças import Peças

class Tabuleiro:
    def __init__(self):
        self.board = []
        self.verdes_left = self.laranjas_left = 18
        self.verdes_kings = self.laranjas_kings = 0
        self.create_tabuleiro()

    def draw_quadrados(self,win):
        win.fill(CINZA)
        for  LINHA in range(LINHAS):
            for COLUNA in range(LINHA%2, COLUNAS, 2):
                pygame.draw.rect(win, BRANCO, (LINHA*TAMANHO_QUADRADO, COLUNA*TAMANHO_QUADRADO, TAMANHO_QUADRADO, TAMANHO_QUADRADO))

    def draw_bordas(self,win):
        for LINHA in range(LINHAS):
            pygame.draw.line(win, PRETO, (0, LINHA * TAMANHO_QUADRADO), (ALTURA, LINHA * TAMANHO_QUADRADO), 2)
            for COLUNA in range(COLUNAS):
                pygame.draw.line(win, PRETO, (COLUNA * TAMANHO_QUADRADO, 0), (COLUNA * TAMANHO_QUADRADO, ALTURA), 2)
                
    def movimento(self,peça,linha,coluna):
        self.board[peça.linha][peça.coluna], self.board[linha][coluna] = self.board[linha][coluna], self.board[peça.linha][peça.coluna]
        peça.movimento(linha,coluna)

        if linha == LINHAS or linha == 0:
            peça.make_king()
            if peça.cor == VERDE:
                self.verdes_kings += 1
            else:
                self.laranjas_kings += 1

    def get_peça(self,linha,coluna):
        return self.board[linha][coluna]

    def create_tabuleiro(self):
    # Definir o número de linhas com peças baseado no tamanho do tabuleiro
        if LINHAS == 6:
            linhas_com_peças = 2
        elif LINHAS == 8:
            linhas_com_peças = 3
        elif LINHAS == 12:
            linhas_com_peças = 4
        else:
            raise ValueError("Tamanho do tabuleiro não suportado. Use 6x6, 8x8 ou 12x12.")

        for LINHA in range(LINHAS):
            self.board.append([])  # Cria uma linha (lista vazia)
            for COLUNA in range(COLUNAS):
                # Linhas do topo (peças verdes)
                if LINHA < linhas_com_peças and COLUNA >= LINHA and COLUNA < COLUNAS - LINHA:
                    self.board[LINHA].append(Peças(LINHA, COLUNA, VERDE))
                    # Linhas da base (peças laranjas)
                elif LINHA >= LINHAS - linhas_com_peças and COLUNA >= (LINHAS - 1 - LINHA) and COLUNA < COLUNAS - (LINHAS - 1 - LINHA):
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
        self.draw_bordas(win)
