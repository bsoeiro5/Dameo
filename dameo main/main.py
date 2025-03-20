import pygame
from dameo_sub.constants import LARGURA, ALTURA
from dameo_sub.tabuleiro import Tabuleiro

WIN = pygame.display.set_mode((LARGURA,ALTURA))   #medidas da janela incial
pygame.display.set_caption('Dameo')


def main():             #função para correr o jogo
    run = True 
    clock = pygame.time.Clock()
    tabuleiro = Tabuleiro()

    while run:
        clock.tick(60)  #60 FPS
        
        for event in pygame.event.get():        #para fechar a janela
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass    
    
        tabuleiro.desenhar(WIN)
        pygame.display.update()

    pygame.quit()

main()
