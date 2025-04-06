import pygame
import time
from copy import deepcopy
from dameo_sub.constants import LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro

nos_expandidos_minimax = 0
nos_expandidos_alphabeta = 0

import time
from copy import deepcopy
from dameo_sub.constants import LARANJA, VERDE

nos_expandidos_alphabeta = 0

def alfa_beta(tabuleiro, depth, alpha, beta, max_player, game):
    global nos_expandidos_alphabeta
    nos_expandidos_alphabeta += 1
    
    # Restrição de tempo mais generosa para permitir análise mais profunda
    current_time = time.time()
    if hasattr(alfa_beta, 'start_time') and current_time - alfa_beta.start_time > 10:  # 10 segundos em vez de 5
        return tabuleiro.heuristica(), tabuleiro

    # Caso base
    if depth == 0 or tabuleiro.winner() is not None:
        return tabuleiro.heuristica(), tabuleiro

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(tabuleiro, VERDE, game)
        
        if not moves:
            return maxEval, tabuleiro
            
        # Ordenação mais estratégica de movimentos
        for move in moves:
            evaluation = alfa_beta(move, depth - 1, alpha, beta, False, game)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        moves = get_all_moves(tabuleiro, LARANJA, game)
        
        if not moves:
            return minEval, tabuleiro
            
        for move in moves:
            evaluation = alfa_beta(move, depth - 1, alpha, beta, True, game)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval, best_move

def get_all_moves(tabuleiro, cor, game):
    moves = []
    capture_moves = []
    
    # Priorizar capturas - isso é essencial para a qualidade do jogo
    for piece in tabuleiro.get_all_peças(cor):
        valid_moves = tabuleiro.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if skip:  # Movimentos de captura
                temp_board = deepcopy(tabuleiro)
                temp_piece = temp_board.get_peça(piece.linha, piece.coluna)
                new_board = simular_movimento(temp_piece, move, temp_board, game, skip)
                if new_board:
                    # Verificar se este movimento de captura leva a múltiplas capturas
                    nova_peça = new_board.get_peça(move[0], move[1])
                    if nova_peça:
                        mais_capturas = False
                        for _, novo_skip in new_board.get_valid_moves(nova_peça).items():
                            if novo_skip:
                                mais_capturas = True
                                break
                        # Priorizar capturas múltiplas adicionando ao início da lista
                        if mais_capturas:
                            capture_moves.insert(0, new_board)
                        else:
                            capture_moves.append(new_board)
                    else:
                        capture_moves.append(new_board)

    if capture_moves:
        return capture_moves

    # Se não há capturas, considerar movimentos estratégicos
    # Verificar movimentos que podem promover peças a posições mais avançadas
    for piece in tabuleiro.get_all_peças(cor):
        valid_moves = tabuleiro.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if not skip:
                temp_board = deepcopy(tabuleiro)
                temp_piece = temp_board.get_peça(piece.linha, piece.coluna)
                new_board = simular_movimento(temp_piece, move, temp_board, game, skip)
                if new_board:
                    moves.append(new_board)

    return moves

def simular_movimento(peça, movimento, tabuleiro, game, skip):
    if peça and movimento:
        try:
            tabuleiro.movimento(peça, movimento[0], movimento[1])
            if skip:
                tabuleiro.remove(skip)
                
                # Verifica capturas adicionais
                nova_peça = tabuleiro.get_peça(movimento[0], movimento[1])
                if nova_peça:
                    novos_movimentos = tabuleiro.get_valid_moves(nova_peça)
                    capturas_adicionais = {move: skipped for move, skipped in novos_movimentos.items() if skipped}
                    
                    if capturas_adicionais:
                        # Implementa uma análise mais profunda para escolher a melhor captura
                        best_move = None
                        best_skipped = None
                        best_score = -float('inf') if peça.cor == VERDE else float('inf')
                        
                        for move, skipped in capturas_adicionais.items():
                            # Cria uma cópia do tabuleiro para avaliação
                            temp_board = deepcopy(tabuleiro)
                            temp_piece = temp_board.get_peça(nova_peça.linha, nova_peça.coluna)
                            
                            # Simula o movimento
                            temp_board.movimento(temp_piece, move[0], move[1])
                            temp_board.remove(skipped)
                            
                            # Verifica se este movimento pode levar a mais capturas
                            temp_nova_peça = temp_board.get_peça(move[0], move[1])
                            mais_capturas = False
                            if temp_nova_peça:
                                for _, novo_skip in temp_board.get_valid_moves(temp_nova_peça).items():
                                    if novo_skip:
                                        mais_capturas = True
                                        break
                            
                            # Avalia este movimento
                            score = temp_board.heuristica()
                            if mais_capturas:
                                # Prioriza capturas múltiplas
                                if peça.cor == VERDE:
                                    score += 100  # Bônus para capturas adicionais
                                else:
                                    score -= 100
                            
                            if (peça.cor == VERDE and score > best_score) or \
                               (peça.cor == LARANJA and score < best_score):
                                best_score = score
                                best_move = move
                                best_skipped = skipped
                        
                        if best_move:
                            return simular_movimento(nova_peça, best_move, tabuleiro, game, best_skipped)
            
            return tabuleiro
        except Exception as e:
            print(f"Erro ao simular movimento: {e}")
            return None
    return None
        
def minimax(tabuleiro, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
    global nos_expandidos_minimax
    nos_expandidos_minimax += 1

    # Adiciona restrição de tempo mais generosa
    current_time = time.time()
    if hasattr(minimax, 'start_time') and current_time - minimax.start_time > 10:  # 10 segundos
        return tabuleiro.heuristica(), tabuleiro

    if depth == 0 or tabuleiro.winner() is not None:
        return tabuleiro.heuristica(), tabuleiro

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(tabuleiro, VERDE, game)
        
        if not moves:
            return maxEval, tabuleiro

        for move in moves:
            evaluation = minimax(move, depth - 1, False, game, alpha, beta)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:  # Add pruning to regular minimax
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        moves = get_all_moves(tabuleiro, LARANJA, game)
        
        if not moves:
            return minEval, tabuleiro

        for move in moves:
            evaluation = minimax(move, depth - 1, True, game, alpha, beta)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:  # Add pruning to regular minimax
                break
        return minEval, best_move
