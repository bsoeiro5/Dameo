import math
import random
from dameo_sub.game import Game
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.peças import Peças
from dameo_sub.constants import VERDE, LARANJA
from copy import deepcopy


class Node:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self._get_untried_moves()

    def UCT_select_child(self, exploration_constant):
        if not self.children:
            return None
        
        # Fórmula UCT: exploitation (wins/visits) + exploration (sqrt(log(parent_visits)/child_visits))
        return max(self.children,
                  key=lambda c: (c.wins / c.visits if c.visits > 0 else 0) +
                               exploration_constant * math.sqrt(math.log(self.visits) / c.visits) if c.visits > 0 else float('inf'))

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

    def _get_untried_moves(self):
        # CORREÇÃO: Verificar se há movimentos de captura obrigatórios primeiro
        moves = []
        capture_moves = []
        
        for piece in self.game_state.tabuleiro.get_all_peças(self.game_state.turn):
            valid_moves = self.game_state.tabuleiro.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                if skip:  # Este é um movimento de captura
                    capture_moves.append((piece, move, skip))
                else:
                    moves.append((piece, move, skip))
        
        # Se houver movimentos de captura, apenas eles são válidos
        if capture_moves:
            return capture_moves
        return moves
    
class MCTS:
    def __init__(self, iterations=1000, simulation_depth=20, exploration_constant=1.4):
        self.iterations = iterations
        self.simulation_depth = simulation_depth
        self.exploration_constant = exploration_constant
        print(f"MCTS inicializado: {iterations} iterações, {simulation_depth} profundidade, {exploration_constant} const. exploração")

    def get_move(self, game):
        # Verificar se há movimentos de captura obrigatórios primeiro
        capture_moves = self._get_capture_moves(game)
        
        # Se houver capturas obrigatórias, aplicar MCTS apenas a elas
        if capture_moves:
            print(f"IA: Encontrei {len(capture_moves)} movimentos de captura obrigatórios")
            root = Node(game)
            # Substituir os movimentos normais por apenas movimentos de captura
            root.untried_moves = capture_moves
        else:
            root = Node(game)

        for i in range(self.iterations):
            if i % 100 == 0:  # Log a cada 100 iterações para feedback
                print(f"MCTS: iteração {i}/{self.iterations}")
                
            node = self._select(root)
            if not node.is_terminal():
                node = self._expand(node)
                reward = self._simulate(node)
                self._backpropagate(node, reward)

        if not root.children:
            print("MCTS: Nenhum movimento disponível")
            return None

        # Escolher o melhor movimento baseado nas visitas
        best_child = max(root.children, key=lambda c: c.visits)
        print(f"MCTS: Movimento escolhido com {best_child.visits} visitas e {best_child.wins} vitórias")
        return best_child.move

    def _get_capture_moves(self, game):
        """Retorna todos os movimentos de captura disponíveis"""
        capture_moves = []
        for piece in game.tabuleiro.get_all_peças(game.turn):
            valid_moves = game.tabuleiro.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                if skip:  # Este é um movimento de captura
                    capture_moves.append((piece, move, skip))
        return capture_moves

    def _select(self, node):
        while not node.is_terminal() and node.is_fully_expanded():
            child = node.UCT_select_child(self.exploration_constant)
            if child is None:
                break
            node = child
        return node

    def _expand(self, node):
        if node.untried_moves:
            move = random.choice(node.untried_moves)
            new_state = self._copy_game_state(node.game_state)
            
            # Aplicar o movimento no novo estado
            peca, novo_pos, skip = move
            
            # Obter a peça correspondente no novo tabuleiro
            new_peca = new_state.tabuleiro.get_peça(peca.linha, peca.coluna)
            
            # Realizar o movimento
            new_state.tabuleiro.movimento(new_peca, novo_pos[0], novo_pos[1])
            
            # Remover peças capturadas
            if skip:
                # Converter os objetos de peça para peças no novo tabuleiro
                new_skips = []
                for s in skip:
                    new_skips.append(new_state.tabuleiro.get_peça(s.linha, s.coluna))
                new_state.tabuleiro.remove(new_skips)
            
            new_state.change_turn()
            
            child = node.add_child(move, new_state)
            return child
        return node

    def _simulate(self, node):
        state = self._copy_game_state(node.game_state)
        depth = 0
        original_turn = state.turn
        
        while depth < self.simulation_depth:
            winner = state.tabuleiro.winner()
            if winner:
                # Retornar 1 se o vencedor é o jogador original, 0 caso contrário
                if (winner == 'VERDE' and original_turn == VERDE) or \
                (winner == 'LARANJA' and original_turn == LARANJA):
                    return 1.0
                else:
                    return 0.0
            
            # Verificar se há uma peça que está em sequência de captura
            capturing_piece = None
            for piece in state.tabuleiro.get_all_peças(state.turn):
                # Verificar se a peça tem capturas disponíveis
                valid_moves = state.tabuleiro.get_valid_moves(piece)
                captures = {move: skip for move, skip in valid_moves.items() if skip}
                if captures:
                    capturing_piece = piece
                    move = random.choice(list(captures.items()))
                    # Formato: ((linha, coluna), [peças_capturadas])
                    novo_pos, skip = move
                    
                    # Aplicar movimento
                    state.tabuleiro.movimento(capturing_piece, novo_pos[0], novo_pos[1])
                    if skip:
                        state.tabuleiro.remove(skip)
                    
                    # Verificar se mesma peça pode continuar capturando
                    valid_moves = state.tabuleiro.get_valid_moves(capturing_piece)
                    captures = {move: skip for move, skip in valid_moves.items() if skip}
                    
                    if captures:  # Se pode continuar capturando, não muda o turno
                        continue
                    
                    break  # Se não pode continuar capturando, sai do loop
            
            # Se não encontrou peça capturando, escolha um movimento normal
            if not capturing_piece:
                # Escolher movimento aleatório
                valid_moves = self._get_valid_moves(state)
                if not valid_moves:
                    break
                move = random.choice(valid_moves)
                
                # Aplicar movimento
                peca, novo_pos, skip = move
                state.tabuleiro.movimento(peca, novo_pos[0], novo_pos[1])
                if skip:
                    state.tabuleiro.remove(skip)
            
            # Mudar o turno apenas quando terminar a sequência de capturas
            state.change_turn()
            depth += 1
        
        # Se chegou ao limite de profundidade, avaliar o estado
        return self._evaluate_state(state, original_turn)

    def _evaluate_state(self, state, original_turn):
        # Usar a heurística implementada no tabuleiro
        score = state.tabuleiro.heuristica()
        
        # Ajustar o score baseado no turno original
        if original_turn == LARANJA:
            score = -score
            
        # Normalizar entre 0 e 1 usando sigmoid
        return 1 / (1 + math.exp(-score/10))

    def _backpropagate(self, node, reward):
        while node:
            node.update(reward)
            node = node.parent
            # Inverter a recompensa para o próximo nível
            reward = 1 - reward

    def _get_valid_moves(self, game):
        moves = []
        for peca in game.tabuleiro.get_all_peças(game.turn):
            valid_moves = game.tabuleiro.get_valid_moves(peca)
            for move, skip in valid_moves.items():
                moves.append((peca, move, skip))
        return moves

    def _copy_game_state(self, game):
        new_game = type(game)(game.win)
        new_game.turn = game.turn
        new_game.selected = None
        new_game.valid_moves = {}
        
        # Copiar tabuleiro
        new_game.tabuleiro = Tabuleiro()
        new_game.tabuleiro.board = [[self._copy_peca(peca) for peca in row] for row in game.tabuleiro.board]
        new_game.tabuleiro.verdes_left = game.tabuleiro.verdes_left
        new_game.tabuleiro.laranjas_left = game.tabuleiro.laranjas_left
        new_game.tabuleiro.verdes_kings = game.tabuleiro.verdes_kings
        new_game.tabuleiro.laranjas_kings = game.tabuleiro.laranjas_kings
        
        return new_game

    def _copy_peca(self, peca):
        if peca == 0:
            return 0
        new_peca = Peças(peca.linha, peca.coluna, peca.cor)
        new_peca.king = peca.king
        return new_peca
