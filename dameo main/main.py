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

    while run:
        
        if game.verificar_fim_do_jogo():
            pygame.time.delay(3000)  # Pequena pausa para o jogador ver o resultado
            run = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if modo == "pvp":  # Player vs Player (nenhuma IA joga)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    linha = y // 100
                    coluna = x // 100
                    game.select(linha, coluna)

            elif modo == "pvc":  # Player vs Computer
                if game.turn == VERDE:  # Jogador Verde joga manualmente
                    value, new_tabuleiro = minimax(game.tabuleiro, 3, True, game)
                    game.ai_move(new_tabuleiro)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        linha = y // 100
                        coluna = x // 100
                        game.select(linha, coluna)
                        
                else:  # IA (Laranja) joga automaticamente
                    pygame.time.delay(500)
                    game.ai_move(game.tabuleiro)

            elif modo == "cvc":  # Computer vs Computer
                pygame.time.delay(500)  # Pequena pausa para visualizar as jogadas
                game.ai_move()  # IA joga para ambos os lados

        game.update(win=WIN)

    pygame.quit()
