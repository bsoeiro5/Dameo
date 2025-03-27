import pygame
from .constants import VERDE, LARANJA, TAMANHO_QUADRADO, ALTURA, AZUL
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

    def winner(self):
        return self.tabuleiro.winner() 
    
    def update(self):
        self.tabuleiro.desenhar(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, linha, coluna):  
        if self.selected:
            result = self._move(linha, coluna)
            if not result:
                self.selected = None
                self.select(linha, coluna)
        
        peça = self.tabuleiro.get_peça(linha, coluna)
        
        if peça != 0 and peça.cor == self.turn:
            self.selected = peça
            self.valid_moves = self.tabuleiro.get_valid_moves(peça)

            # Verifica se existem movimentos de captura
            capture_moves = {move: self.valid_moves[move] for move in self.valid_moves if self.valid_moves[move]}
            
            if capture_moves:
                # Se houver movimentos de captura, deve-se forçar o jogador a realizá-los
                self.valid_moves = capture_moves
                return True
            else:
                # Se não houver movimentos de captura, permite o jogador fazer um movimento normal
                return True
        
        return False

    def _move(self, linha, coluna):
        peça = self.tabuleiro.get_peça(linha, coluna)
        if self.selected and peça == 0 and (linha, coluna) in self.valid_moves:
            self.tabuleiro.movimento(self.selected, linha, coluna)
            skipped = self.valid_moves[(linha, coluna)]
            if skipped:
                self.tabuleiro.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, movimentos):
        for movimento in movimentos:
            linha, coluna = movimento
            pygame.draw.circle(self.win, AZUL, (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == VERDE:
            self.turn = LARANJA
        else:
            self.turn = VERDE
