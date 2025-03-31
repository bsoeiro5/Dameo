import pygame
from copy import deepcopy
from dameo_sub.constants import LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro

def minimax(tabuleiro, profundidade, max_player, game):
    if profundidade == 0 or tabuleiro.winner() != None:
        return tabuleiro.evaluate(), tabuleiro

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(tabuleiro, game, VERDE):
            evaluation = minimax(move, profundidade - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(tabuleiro, game, LARANJA):
            evaluation = minimax(move, profundidade - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move
    
def simular_movimento(peça, movimento, tabuleiro, game, skip):
    tabuleiro.movimento(peça, movimento[0], movimento[1])
    if skip:
        tabuleiro.remove(skip)
    return tabuleiro

def get_all_moves(tabuleiro, cor, game):
    moves = []

    for piece in tabuleiro.get_all_peças(cor):
        valid_moves = tabuleiro.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_tabuleiro = deepcopy(tabuleiro)
            temp_peça = temp_tabuleiro.get_peça(piece.linha, piece.coluna)
            new_tabuleiro = simular_movimento(temp_peça, move, temp_tabuleiro, game, skip)
            moves.append(new_tabuleiro)

    return moves

    
