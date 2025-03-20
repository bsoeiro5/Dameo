from .constants import LARANJA, VERDE, TAMANHO_QUADRADO, LARANJA_ESCURO
import pygame

class Peças:
    ESPAÇO = 10
    BORDA = 2

    def __init__(self, linha, coluna, cor):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor
        self.king = False

        if self.cor == LARANJA:
            self.direções = -1
        else:
            self.direções = 1

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):     #calcular a posição da peça
        self.x = TAMANHO_QUADRADO * self.coluna + TAMANHO_QUADRADO // 2
        self.y = TAMANHO_QUADRADO * self.linha + TAMANHO_QUADRADO // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        raio = TAMANHO_QUADRADO // 2 - self.ESPAÇO
        pygame.draw.circle(win, LARANJA_ESCURO, (self.x, self.y), raio + self.BORDA)
        pygame.draw.circle(win, self.cor, (self.x, self.y), raio)

    def __repr__(self):
        return str(self.cor)
