import pygame
from .constants import VERDE, LARANJA
from .tabuleiro import Tabuleiro

class Game:
    def __init__(self,win):
        self._init()
        self.win = win

    def _init(self):
        self.selected = None
        self.tabuleiro = Tabuleiro()
        self.turn = VERDE
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, linha, coluna):  #tentar selecionar uma peça e verifica os movimentos possíveis
        if self.selected:
            result = self._move(linha,coluna)
            if not result:
                self.selected = None
                self.select(linha,coluna)
        else:
            peça = self.tabuleiro.get_peça(linha,coluna)
            if peça != 0 and peça.cor == self.turn:
                self.selected = peça
                self.valid_moves = self.tabuleiro.get_valid_moves(peça)
                return True
        
        return False

    def _move(self,linha,coluna):
        peça = self.tabuleiro.get_peça(linha,coluna)
        if self.selected and peça == 0 and (linha,coluna) in self.valid_moves:
            self.tabuleiro.movimento(self.selected,linha,coluna)
            self.change_turn()
        else:
            return False

        return True
