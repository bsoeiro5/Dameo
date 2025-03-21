import pygame
from dameo_sub.constants import LARGURA, ALTURA, TAMANHO_QUADRADO
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.game import Game

WIN = pygame.display.set_mode((LARGURA,ALTURA))   #medidas da janela incial
pygame.display.set_caption('Dameo')


def get_row_col_from_mouse(pos):
    x, y = pos
    linha = y // TAMANHO_QUADRADO
    coluna = x // TAMANHO_QUADRADO
    return linha, coluna

def main():             #função para correr o jogo
    run = True 
    clock = pygame.time.Clock()
    game = Game(WIN)
    

    while run:
        clock.tick(60)  #60 FPS
        
        for event in pygame.event.get():        #para fechar a janela
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                pos = pygame.mouse.get_pos()
                linha, coluna = get_row_col_from_mouse(pos)
                
        game.update()

    pygame.quit()

main()
