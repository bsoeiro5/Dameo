import pygame
from copy import deepcopy
from dameo_sub.constants import LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro

def get_all_moves(tabuleiro, cor, game):
    moves = []
    capture_moves = []
    
    for piece in tabuleiro.get_all_peças(cor):
        valid_moves = tabuleiro.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # Verifica se o movimento não é para a mesma posição
            if (move[0] != piece.linha or move[1] != piece.coluna):
                if skip:  # This is a capture move
                    temp_board = deepcopy(tabuleiro)
                    temp_piece = temp_board.get_peça(piece.linha, piece.coluna)
                    new_board = simular_movimento(temp_piece, move, temp_board, game, skip)
                    if new_board:
                        capture_moves.append((temp_piece, move, skip, new_board))
                else:  # Regular move
                    temp_board = deepcopy(tabuleiro)
                    temp_piece = temp_board.get_peça(piece.linha, piece.coluna)
                    new_board = simular_movimento(temp_piece, move, temp_board, game, None)
                    if new_board:
                        moves.append((temp_piece, move, None, new_board))
    
    # Retorna movimentos de captura se existirem, senão retorna movimentos normais
    if capture_moves:
        
        return capture_moves[:10]  # Limita para evitar explosão combinatória
    
    
    return moves[:15]  # Limita para evitar explosão combinatória

def alfa_beta(tabuleiro, depth, alpha, beta, max_player, game):
    if depth == 0 or tabuleiro.winner() is not None:
        return tabuleiro.heuristica(), tabuleiro

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(tabuleiro, VERDE, game)
        
        if not moves:  # Se não houver movimentos possíveis
            return maxEval, tabuleiro
            
        for _, _, _, move in moves:
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
        
        if not moves:  # Se não houver movimentos possíveis
            return minEval, tabuleiro
            
        for _, _, _, move in moves:
            evaluation = alfa_beta(move, depth - 1, alpha, beta, True, game)[0]
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

def minimax(tabuleiro, depth, max_player, game):
    if depth == 0 or tabuleiro.winner() is not None:
        return tabuleiro.heuristica(), tabuleiro

    if max_player:
        maxEval = float('-inf')
        best_move = None
        moves = get_all_moves(tabuleiro, VERDE, game)
        
        if not moves:  # Se não houver movimentos possíveis
            return maxEval, tabuleiro
            
        for _, _, _, move in moves:
            evaluation = minimax(move, depth - 1, False, game)[0]
            if evaluation > maxEval:
                maxEval = evaluation
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        moves = get_all_moves(tabuleiro, LARANJA, game)
        
        if not moves:  # Se não houver movimentos possíveis
            return minEval, tabuleiro
            
        for _, _, _, move in moves:
            evaluation = minimax(move, depth - 1, True, game)[0]
            if evaluation < minEval:
                minEval = evaluation
                best_move = move
        return minEval, best_move
