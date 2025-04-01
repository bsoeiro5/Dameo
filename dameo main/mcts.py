import math
import random
from dameo_sub.game import Game
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.peças import Peças
from dameo_sub.constants import VERDE, LARANJA

class Node:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = self._copy_game_state(game_state)
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self._get_untried_moves()

    def _copy_game_state(self, game):
        new_game = type(game)(game.win)
        new_game.selected = game.selected
        new_game.turn = game.turn
        new_game.valid_moves = game.valid_moves.copy()
        new_game.tabuleiro = self._copy_tabuleiro(game.tabuleiro)
        return new_game

    def _copy_tabuleiro(self, tabuleiro):
        new_tabuleiro = Tabuleiro()
        new_tabuleiro.board = [[self._copy_peca(peca) for peca in row] for row in tabuleiro.board]
        new_tabuleiro.verdes_left = tabuleiro.verdes_left
        new_tabuleiro.laranjas_left = tabuleiro.laranjas_left
        new_tabuleiro.verdes_kings = tabuleiro.verdes_kings
        new_tabuleiro.laranjas_kings = tabuleiro.laranjas_kings
        return new_tabuleiro

    def _copy_peca(self, peca):
        if peca == 0:
            return 0
        new_peca = Peças(peca.linha, peca.coluna, peca.cor)
        new_peca.king = peca.king
        return new_peca

    def _get_untried_moves(self):
        moves = []
        cor = VERDE if self.game_state.turn == VERDE else LARANJA
        for piece in self.game_state.tabuleiro.get_all_peças(cor):
            valid_moves = self.game_state.tabuleiro.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                # Armazena a peça real, não apenas sua cor
                moves.append((piece, move, skip))
        return moves

    def add_child(self, move, game_state):
        child = Node(game_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def UCT_select_child(self):
        if not self.children:
            return None
        
        c = math.sqrt(2)
        return max(self.children, 
                  key=lambda child: (child.wins / child.visits) + 
                  c * math.sqrt(math.log(self.visits) / child.visits) 
                  if child.visits > 0 else float('inf'))

    def update(self, result):
        self.visits += 1
        self.wins += result

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        return self.game_state.tabuleiro.winner() is not None

    def get_best_child(self):
        return max(self.children, key=lambda c: c.visits) if self.children else None

import math
import random
from copy import deepcopy
from dameo_sub.constants import VERDE, LARANJA

class Node:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = self._copy_game_state(game_state)
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self._get_untried_moves()

    def _copy_game_state(self, game):
        new_game = type(game)(game.win)
        new_game.turn = game.turn
        new_game.selected = None
        new_game.valid_moves = {}
        new_game.tabuleiro = self._copy_tabuleiro(game.tabuleiro)
        return new_game

    def _copy_tabuleiro(self, tabuleiro):
        new_tabuleiro = Tabuleiro()
        new_tabuleiro.board = [[self._copy_peca(peca) for peca in row] for row in tabuleiro.board]
        new_tabuleiro.verdes_left = tabuleiro.verdes_left
        new_tabuleiro.laranjas_left = tabuleiro.laranjas_left
        new_tabuleiro.verdes_kings = tabuleiro.verdes_kings
        new_tabuleiro.laranjas_kings = tabuleiro.laranjas_kings
        return new_tabuleiro

    def _copy_peca(self, peca):
        if peca == 0:
            return 0
        new_peca = Peças(peca.linha, peca.coluna, peca.cor)
        new_peca.king = peca.king
        return new_peca

    def _get_untried_moves(self):
        moves = []
        for piece in self.game_state.tabuleiro.get_all_peças(self.game_state.turn):
            valid_moves = self.game_state.tabuleiro.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                moves.append((piece, move, skip))
        return moves

    def UCT_select_child(self):
        if not self.children:
            return None
        
        c = math.sqrt(2)
        return max(self.children, 
                  key=lambda child: (child.wins / child.visits if child.visits > 0 else 0) + 
                  c * math.sqrt(math.log(self.visits) / child.visits) if child.visits > 0 else float('inf'))

    def add_child(self, move, game_state):
        child = Node(game_state, parent=self, move=move)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result):
        self.visits += 1
        self.wins += result

    def is_terminal(self):
        return self.game_state.tabuleiro.winner() is not None

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

class MCTS:
    def __init__(self, iterations=1000):
        self.iterations = iterations

    def get_move(self, game):
        root = Node(game)
        
        for _ in range(self.iterations):
            node = self._select(root)
            if not node.is_terminal() and not node.is_fully_expanded():
                node = self._expand(node)
            reward = self._simulate(node)
            self._backpropagate(node, reward)

        if root.children:
            best_child = max(root.children, 
                           key=lambda c: (c.wins / c.visits if c.visits > 0 else 0) + 
                           math.sqrt(2 * math.log(root.visits) / c.visits) if c.visits > 0 else float('inf'))
            return best_child.move
        return None

    def _select(self, node):
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return node
            node = node.UCT_select_child()
            if node is None:
                break
        return node

    def _expand(self, node):
        if not node.untried_moves:
            return node
        
        move = random.choice(node.untried_moves)
        new_state = self._copy_game_state(node.game_state)
        
        piece, pos, skip = move
        new_state.tabuleiro.movimento(piece, pos[0], pos[1])
        if skip:
            new_state.tabuleiro.remove(skip)
        new_state.turn = VERDE if new_state.turn == LARANJA else LARANJA
        
        return node.add_child(move, new_state)

    def _simulate(self, node):
        state = self._copy_game_state(node.game_state)
        depth = 0
        max_depth = 50
        
        while not state.tabuleiro.winner() and depth < max_depth:
            moves = self._get_all_possible_moves(state)
            if not moves:
                break
            
            move = random.choice(moves)
            piece, pos, skip = move
            state.tabuleiro.movimento(piece, pos[0], pos[1])
            if skip:
                state.tabuleiro.remove(skip)
            state.turn = VERDE if state.turn == LARANJA else LARANJA
            depth += 1
        
        return self._evaluate_position(state, node.game_state.turn)

    def _backpropagate(self, node, reward):
        while node:
            node.update(reward)
            node = node.parent

    def _get_all_possible_moves(self, game_state):
        moves = []
        for piece in game_state.tabuleiro.get_all_peças(game_state.turn):
            valid_moves = game_state.tabuleiro.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                moves.append((piece, move, skip))
        return moves

    def _evaluate_position(self, state, original_turn):
        score = 0
        
        # Valor base das peças
        if original_turn == LARANJA:
            score = state.tabuleiro.laranjas_left - state.tabuleiro.verdes_left
            score += (state.tabuleiro.laranjas_kings * 1.5 - state.tabuleiro.verdes_kings * 1.5)
        else:
            score = state.tabuleiro.verdes_left - state.tabuleiro.laranjas_left
            score += (state.tabuleiro.verdes_kings * 1.5 - state.tabuleiro.laranjas_kings * 1.5)

        # Bônus para peças avançadas
        for peca in state.tabuleiro.get_all_peças(original_turn):
            if original_turn == LARANJA:
                score += (7 - peca.linha) * 0.3  # Aumentado o peso do avanço
            else:
                score += peca.linha * 0.3

        # Bônus para peças protegidas e centralizadas
        for peca in state.tabuleiro.get_all_peças(original_turn):
            # Bônus para posição central
            col_distance_from_center = abs(3.5 - peca.coluna)
            score += (4 - col_distance_from_center) * 0.1

            # Bônus para peças protegidas
            if self._is_protected(state.tabuleiro, peca):
                score += 0.5

        return (score + 10) / 20  # Normalizar para [0,1]

    def _copy_game_state(self, game):
        new_game = type(game)(game.win)
        new_game.turn = game.turn
        new_game.selected = None
        new_game.valid_moves = {}
        new_game.tabuleiro = self._copy_tabuleiro(game.tabuleiro)
        return new_game

    def _copy_tabuleiro(self, tabuleiro):
        new_tabuleiro = Tabuleiro()
        new_tabuleiro.board = [[self._copy_peca(peca) for peca in row] for row in tabuleiro.board]
        new_tabuleiro.verdes_left = tabuleiro.verdes_left
        new_tabuleiro.laranjas_left = tabuleiro.laranjas_left
        new_tabuleiro.verdes_kings = tabuleiro.verdes_kings
        new_tabuleiro.laranjas_kings = tabuleiro.laranjas_kings
        return new_tabuleiro

    def _copy_peca(self, peca):
        if peca == 0:
            return 0
        new_peca = Peças(peca.linha, peca.coluna, peca.cor)
        new_peca.king = peca.king
        return new_peca
