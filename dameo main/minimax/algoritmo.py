import pygame
from copy import deepcopy
from dameo_sub.constants import LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro

def get_all_moves(tabuleiro, cor, game):
    moves = []
    capture_moves = []  # Lista separada para movimentos de captura
    
    # Primeiro, verifica se existem capturas disponíveis
    for piece in tabuleiro.get_all_peças(cor):
        valid_moves = tabuleiro.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if skip:  # Se é um movimento de captura
                temp_board = deepcopy(tabuleiro)
                temp_piece = temp_board.get_peça(piece.linha, piece.coluna)
                new_board = simular_movimento(temp_piece, move, temp_board, game, skip)
                if new_board:
                    capture_moves.append(new_board)

    # Se houver capturas disponíveis, retorna apenas elas
    if capture_moves:
        return capture_moves

    # Se não houver capturas, retorna movimentos normais
    for piece in tabuleiro.get_all_peças(cor):
        valid_moves = tabuleiro.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            if not skip:  # Apenas movimentos sem captura
                temp_board = deepcopy(tabuleiro)
                temp_piece = temp_board.get_peça(piece.linha, piece.coluna)
                new_board = simular_movimento(temp_piece, move, temp_board, game, skip)
                if new_board:
                    moves.append(new_board)

    return moves

def minimax(tabuleiro, depth, alpha, beta, max_player, game):
    if depth == 0 or tabuleiro.winner() is not None:
        return tabuleiro.heuristica(), tabuleiro

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(tabuleiro, VERDE, game)
        
        if not moves:  # Se não houver movimentos possíveis
            return maxEval, tabuleiro
            
        for move in moves:
            evaluation = minimax(move, depth - 1, alpha, beta, False, game)[0]
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
        
        if not moves:  # Se não houver movimentos possíveis
            return minEval, tabuleiro
            
        for move in moves:
            evaluation = minimax(move, depth - 1, alpha, beta, True, game)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval, best_move

def simular_movimento(peça, movimento, tabuleiro, game, skip):
    if peça and movimento:
        try:
            tabuleiro.movimento(peça, movimento[0], movimento[1])
            if skip:
                tabuleiro.remove(skip)
                
                # Verifica se há mais capturas disponíveis após a primeira
                nova_peça = tabuleiro.get_peça(movimento[0], movimento[1])
                if nova_peça:
                    novos_movimentos = tabuleiro.get_valid_moves(nova_peça)
                    capturas_adicionais = {move: skipped for move, skipped in novos_movimentos.items() if skipped}
                    if capturas_adicionais:
                        # Se houver mais capturas disponíveis, escolhe uma aleatoriamente
                        # ou implementa uma lógica para escolher a melhor
                        move, skipped = list(capturas_adicionais.items())[0]
                        return simular_movimento(nova_peça, move, tabuleiro, game, skipped)
            
            return tabuleiro
        except Exception as e:
            print(f"Erro ao simular movimento: {e}")
            return None
    return None
