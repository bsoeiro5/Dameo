import pygame
from .constants import VERDE, LARANJA, TAMANHO_QUADRADO, ALTURA, AZUL, LINHAS, COLUNAS
from .tabuleiro import Tabuleiro

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def _init(self):
        self.selected = None
        self.tabuleiro = Tabuleiro()
        self.turn = VERDE
        self.valid_moves = {}
        self.must_capture = False
        self.capturing_piece = None  # Armazena a peça que está capturando

    def winner(self):
        return self.tabuleiro.winner()
    
    def update(self):
        self.tabuleiro.desenhar(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, linha, coluna):
        # Se há uma peça em processo de captura múltipla
        if self.capturing_piece:
            # Verifica se o clique foi em um movimento válido
            if (linha, coluna) in self.valid_moves:
                return self._process_move(linha, coluna)
            else:
                # Se clicou em outro lugar, cancela a captura múltipla e reseta
                self._end_turn()
                return False
        
        peça = self.tabuleiro.get_peça(linha, coluna)
        
        # Verifica se há capturas obrigatórias
        self._check_capture_requirements()
        
        # Seleciona uma peça do jogador atual
        if peça != 0 and peça.cor == self.turn:
            # Se há capturas obrigatórias, só permite selecionar peças que podem capturar
            if self.must_capture:
                self.valid_moves = self.tabuleiro.get_valid_moves(peça)
                self.valid_moves = {move: skipped for move, skipped in self.valid_moves.items() if skipped}
                
                if self.valid_moves:  # Se esta peça pode capturar
                    self.selected = peça
                    return True
                return False
            else:
                # Sem capturas obrigatórias, seleciona normalmente
                self.selected = peça
                self.valid_moves = self.tabuleiro.get_valid_moves(peça)
                return True
        
        # Se já tem uma peça selecionada, tenta mover
        if self.selected:
            result = self._process_move(linha, coluna)
            if not result and peça != 0 and peça.cor != self.turn:
                # Se clicou em uma peça adversária sem ser um movimento válido, reseta
                self._end_turn()
            return result
        
        return False

    def _process_move(self, linha, coluna):
        peça = self.tabuleiro.get_peça(linha, coluna)
        
        if peça == 0 and (linha, coluna) in self.valid_moves:
            # Faz o movimento
            self.tabuleiro.movimento(self.selected, linha, coluna)
            skipped = self.valid_moves[(linha, coluna)]
            
            if skipped:  # Se houve captura
                self.tabuleiro.remove(skipped)
                
                # Verifica se há mais capturas disponíveis
                current_piece = self.tabuleiro.get_peça(linha, coluna)
                self.valid_moves = self.tabuleiro.get_valid_moves(current_piece)
                # Filtra apenas capturas
                self.valid_moves = {move: skipped for move, skipped in self.valid_moves.items() if skipped}
                
                if self.valid_moves:  # Se pode continuar capturando
                    self.capturing_piece = current_piece
                    self.selected = current_piece
                    self.must_capture = True
                    return True
                else:  # Não há mais capturas
                    self._end_turn()
                    return True
            else:  # Movimento sem captura
                if self.must_capture:
                    return False  # Não deveria acontecer
                self._end_turn()
                return True
        
        return False

    def _check_capture_requirements(self):
        self.must_capture = False
        # Verifica se há capturas obrigatórias
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peça = self.tabuleiro.get_peça(linha, coluna)
                if peça != 0 and peça.cor == self.turn:
                    moves = self.tabuleiro.get_valid_moves(peça)
                    if any(skipped for skipped in moves.values() if skipped):
                        self.must_capture = True
                        return

    def _end_turn(self):
        self.selected = None
        self.capturing_piece = None
        self.valid_moves = {}
        self.must_capture = False
        
        # Muda o turno
        self.turn = LARANJA if self.turn == VERDE else VERDE
        
        # Verifica capturas obrigatórias para o próximo jogador
        self._check_capture_requirements()

    def draw_valid_moves(self, movimentos):
        for movimento in movimentos:
            linha, coluna = movimento
            pygame.draw.circle(self.win, AZUL, (coluna * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2, linha * TAMANHO_QUADRADO + TAMANHO_QUADRADO//2), 15)
