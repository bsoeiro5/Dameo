import pygame
from dameo_sub.constants import LARGURA, ALTURA, TAMANHO_QUADRADO, LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.game import Game
from minimax.algoritmo import minimax

# Configuração inicial da janela
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Dameo')

def get_row_col_from_mouse(pos):
    """Converte a posição do mouse em coordenadas do tabuleiro."""
    x, y = pos
    linha = y // TAMANHO_QUADRADO
    coluna = x // TAMANHO_QUADRADO
    return linha, coluna

def jogo_principal(modo="pvp"):
    """
    Loop principal do jogo Dameo. Recebe o modo de jogo:
    - "pvp": Player vs Player
    - "pvc": Player vs Computer
    - "cvc": Computer vs Computer
    """
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    while run:
        clock.tick(60)  # 60 FPS

        if game.turn == VERDE:
            value, new_board = minimax(game.get_tabuleiro(), 3, VERDE, game)
            game.ai_move(new_board)
        
        # Verificar se o jogo terminou
        if game.verificar_fim_do_jogo():  # Função de verificação no Game
            pygame.time.wait(4000)  # Espera para mostrar o vencedor
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Encerrar ao fechar a janela
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                linha, coluna = get_row_col_from_mouse(pos)
                
                # Lógica do modo Player vs Player
                if modo == "pvp":
                    game.select(linha, coluna)
                
                # Modo Player vs Computer
                elif modo == "pvc":
                    game.select(linha, coluna)
                    # Adicione aqui a lógica de jogada da IA
                    
                # Modo Computer vs Computer
                elif modo == "cvc":
                    # Adicione lógica para ambos os lados jogados pela IA
                    pass

        game.update()

    pygame.quit()
