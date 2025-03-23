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

        if linha == LINHAS - 1 or linha == 0:
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

    def remove(self,peças):
        for peça in peças:
            self.board[peça.linha][peça.coluna] = 0
            if peça != 0:
                if peça.cor == LARANJA:
                    self.laranjas_left -= 1
                else:
                    self.verdes_left -= 1
    def winner(self):
        if self.laranjas_left <= 0:
            return VERDE
        elif self.verdes_left <= 0:
            return LARANJA
        return None
    
    def get_valid_moves(self, peça):
        movimentos = {}
        esquerda = peça.coluna - 1
        direita = peça.coluna + 1
        linha = peça.linha

        if peça.cor == LARANJA or peça.king:
            movimentos.update(self._traverse_left(linha -1, max(linha-3, -1), -1, peça.cor, esquerda))
            movimentos.update(self._traverse_right(linha -1, max(linha-3, -1), -1, peça.cor, direita))
            movimentos.update(self._traverse_vertical(linha - 1, max(linha-3, -1), -1, peça.cor, peça.coluna))

        if peça.cor == VERDE or peça.king:
            movimentos.update(self._traverse_left(linha +1, min(linha+3, LINHAS), 1, peça.cor, esquerda))
            movimentos.update(self._traverse_right(linha +1, min(linha+3, LINHAS), 1, peça.cor, direita))
            movimentos.update(self._traverse_vertical(linha + 1, min(linha+3, LINHAS), 1, peça.cor, peça.coluna))

        return movimentos

    def _traverse_left(self, start, stop, step, cor, left, skipped=[]):
        movimentos = {}
        last = []

        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    movimentos[(r, left)] = last + skipped
                else:
                    movimentos[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 1, 0)
                    else:
                        row = min(r + 1, LINHAS)
                    movimentos.update(self._traverse_left(r + step, row, step, cor, left - 1, skipped=last))
                    movimentos.update(self._traverse_right(r + step, row, step, cor, left + 1, skipped=last))
                break
            elif current.cor == cor:
                last = [current]
            else:
                break

            left -= 1
        return movimentos

    def _traverse_right(self, start, stop, step, cor, right, skipped=[]):
        movimentos = {}
        last = []

        for r in range(start, stop, step):
            if right >= COLUNAS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    movimentos[(r, right)] = last + skipped
                else:
                    movimentos[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 1, 0)
                    else:
                        row = min(r + 1, LINHAS)
                    movimentos.update(self._traverse_left(r + step, row, step, cor, right - 1, skipped=last))
                    movimentos.update(self._traverse_right(r + step, row, step, cor, right + 1, skipped=last))
                break
            elif current.cor == cor:
                last = [current]
            else:
                break

            right += 1
        return movimentos

    def _traverse_vertical(self, start, stop, step, cor, coluna, skipped=[]):
        movimentos = {}
        last = []  # Lista de peças que foram saltadas

        for r in range(start, stop, step):
            current = self.board[r][coluna]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    movimentos[(r, coluna)] = last + skipped
                else:
                    movimentos[(r, coluna)] = last
                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3,LINHAS)
                    movimentos.update(self._traverse_left(r+step, row, step, cor, coluna-1, skipped=last))
                    movimentos.update(self._traverse_right(r+step, row, step, cor, coluna+1, skipped=last))
                break
            elif current.cor == cor:
                    last = []
            else:
                last = [current]
        return movimentos
