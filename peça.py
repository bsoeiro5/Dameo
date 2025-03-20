import pygame

# Inicializa o pygame
pygame.init()

# Definições de tela (com fundo transparente)
LARGURA, ALTURA = 400, 400
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.SRCALPHA)  # Habilita transparência

# Cores
PRETO = (0, 0, 0)
VERMELHO = (200, 0, 0)
BRANCO = (255, 255, 255, 0)  # Transparente

def desenhar_peca_3d(surface, x, y, cor):
    raio = 30
    sombra = (cor[0] // 2, cor[1] // 2, cor[2] // 2)  # Cor escura para sombra

    # Desenha sombra inferior (para efeito 3D)
    pygame.draw.circle(surface, sombra, (x, y + 3), raio + 1)

    # Desenha a peça principal
    pygame.draw.circle(surface, cor, (x, y), raio)

    # Contorno para acabamento
    pygame.draw.circle(surface, (255, 255, 255), (x, y), raio, 1)

# Criando uma superfície transparente para desenhar as peças
peca_surface = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)

# Desenha peças na superfície transparente
desenhar_peca_3d(peca_surface, 200, 200, PRETO)

# Loop principal
rodando = True
while rodando:
    TELA.fill((0, 0, 0, 0))  # Mantém a tela transparente

    # Blita a superfície das peças na tela principal
    TELA.blit(peca_surface, (0, 0))

    # Eventos para fechar a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    pygame.display.update()

pygame.quit()
