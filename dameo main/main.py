import pygame
from dameo_sub.constants import LARGURA, ALTURA, TAMANHO_QUADRADO, LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.game import Game

WIN = pygame.display.set_mode((LARGURA,ALTURA))   #medidas da janela incial
pygame.display.set_caption('Dameo')


def get_row_col_from_mouse(pos):
    x, y = pos
    linha = y // TAMANHO_QUADRADO
    coluna = x // TAMANHO_QUADRADO
    return linha, coluna

def main():
    run = True 
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    while run:
        clock.tick(60)  # 60 FPS
        if game.verificar_fim_do_jogo():  # Verifica se o jogo terminou
            pygame.time.wait(4000)  # Espera 4 segundos para que o jogador veja a mensagem
            run = False  # Encerra o loop do jogo
        
        for event in pygame.event.get():  # Para fechar a janela
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                linha, coluna = get_row_col_from_mouse(pos)
                game.select(linha, coluna)
        
        game.update()

    pygame.quit()

main()
