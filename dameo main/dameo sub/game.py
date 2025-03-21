import pygame
from .constants import VERDE, LARANJA
from .tabuleiro import Tabuleiro


class Game:
    def __init__(self,win):
        self.selected = None
        self.tabuleiro = Tabuleiro()
        self.turn = VERDE
        self.valid_moves = {}
        self.win = win
def update(self):
    self.tabuleiro.desenhar(self.win)
    pygame.display.update()
