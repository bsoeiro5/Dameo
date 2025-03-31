import pygame
from dameo_sub.constants import LARGURA, ALTURA, TAMANHO_QUADRADO, LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.game import Game
from minimax.algoritmo import minimax

# Configuração inicial da janela
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Dameo')

def jogo_principal(modo):
    WIN = pygame.display.set_mode((LARGURA, ALTURA))
    game = Game(WIN)
    run = True
    ai_thinking = False

    while run:
        if game.verificar_fim_do_jogo():
            pygame.time.delay(3000)
            run = False
            break

        # Turno da IA no modo PVC
        if modo == "pvc" and game.turn == LARANJA and not ai_thinking:
            ai_thinking = True
            value, new_board = minimax(game.get_tabuleiro(), 2, float('-inf'), float('inf'), False, game)
            if new_board:
                game.ai_move(new_board)
            ai_thinking = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // TAMANHO_QUADRADO, pos[0] // TAMANHO_QUADRADO
                
                if modo == "pvp":
                    game.select(row, col)
                elif modo == "pvc" and game.turn == VERDE:
                    game.select(row, col)

        game.update(WIN)
        pygame.time.delay(50)

    pygame.quit()
