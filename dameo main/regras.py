import pygame
from dameo_sub.constants import LARGURA, ALTURA, BRANCO, PRETO

def regras(janela):
    """Exibe a tela com as regras do jogo."""
    
    # Carrega a imagem de fundo
    background = pygame.image.load("assets/background_regras.png")
    background = pygame.transform.scale(background, (LARGURA, ALTURA))

    fonte_titulo = pygame.font.Font(None, 50)
    fonte_texto = pygame.font.Font(None, 30)

    titulo = fonte_titulo.render("Regras do Jogo", True, PRETO)
    
    regras_texto = [
        "1. Cada jogador pode mover uma peça por turno.",
        "2. As peças movem-se diagonalmente e para a frente.",
        "3. Capturas são obrigatórias, se disponíveis.",
        "4. As peças promovem-se a rei ao alcançar o lado oposto.",
        "5. Os reis podem mover-se em todas as direções, a",
        " quantidade de casas que quiserem.",
        "6. O jogo termina quando um jogador perde todas as peças,",
        " ou não tem mais movimentos possíveis.",
        "Pressione ESC para voltar ao jogo.",
    ]

    rodando = True
    while rodando:
        janela.blit(background, (0, 0))  # Define o fundo

        # Posiciona o título
        janela.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))

        # Renderiza o texto das regras
        y_offset = 285
        for regra in regras_texto:
            texto = fonte_texto.render(regra, True, PRETO)
            janela.blit(texto, (100, y_offset))
            y_offset += 30

        pygame.display.update()

        # Loop de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
