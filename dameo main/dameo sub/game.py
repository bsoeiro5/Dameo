import pygame
from .constants import VERDE, LARANJA

class Game:
    def __init__(self,win):
        self.selected = None
        self.tabuleiro = Tabuleiro()
        self.turn = VERDE
        self.valid_moves = {}
        self.win = win
