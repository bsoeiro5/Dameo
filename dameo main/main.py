import pygame
import time
from dameo_sub.constants import LARGURA, ALTURA, TAMANHO_QUADRADO, LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.game import Game
from minimax.algoritmo import minimax

# Configuração inicial da janela
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Dameo')

def jogo_principal(modo, dificuldade="medio"):
    WIN = pygame.display.set_mode((LARGURA, ALTURA))
    game = Game(WIN)
    run = True
    ai_thinking = False
    last_move_time = 0
    
    # Configuração da profundidade do minimax baseada na dificuldade
    if dificuldade == "facil":
        depth = 1
        delay_between_moves = 500  # Mais rápido para o nível fácil
    elif dificuldade == "medio":
        depth = 3
        delay_between_moves = 1000  # Velocidade média
    else:  # dificil
        depth = 5
        delay_between_moves = 1500  # Mais lento para que a IA "pense" mais

    print(f"Jogo iniciado no modo {modo} com dificuldade {dificuldade} (profundidade {depth})")

    while run:
        # Verificar se o jogo terminou
        if game.verificar_fim_do_jogo():
            pygame.time.delay(3000)
            run = False
            break

        current_time = pygame.time.get_ticks()
        
        # Modo CVC - ambos os jogadores são controlados pelo computador
        if modo == "cvc" and not ai_thinking and current_time - last_move_time > delay_between_moves:
            ai_thinking = True
            
            # Definir o jogador maximizador com base no turno atual
            is_max_player = game.turn == VERDE
            
            # Executar o algoritmo minimax
            value, new_board = minimax(game.get_tabuleiro(), depth, float('-inf'), float('inf'), is_max_player, game)
            
            if new_board:
                game.ai_move(new_board)
                last_move_time = current_time
                
                # Atualiza a tela após cada movimento
                game.update(WIN)
                
            ai_thinking = False
            continue
        
        # Turno da IA no modo PVC
        elif modo == "pvc" and game.turn == LARANJA and not ai_thinking:
            ai_thinking = True
            value, new_board = minimax(game.get_tabuleiro(), depth, float('-inf'), float('inf'), False, game)
            if new_board:
                game.ai_move(new_board)
                last_move_time = current_time
            ai_thinking = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            # Processar cliques apenas para modos que envolvem jogador humano
            if modo != "cvc" and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // TAMANHO_QUADRADO, pos[0] // TAMANHO_QUADRADO
                
                if modo == "pvp":
                    game.select(row, col)
                elif modo == "pvc" and game.turn == VERDE:
                    game.select(row, col)

        # Atualizar a tela
        game.update(WIN)
        
        # Pequeno atraso para reduzir o uso de CPU
        pygame.time.delay(50)

    pygame.quit()
