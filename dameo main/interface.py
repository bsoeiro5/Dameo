import pygame
import sys
from dameo_sub.constants import LARGURA, ALTURA, BRANCO, AZUL_CLARO, CASTANHO, PRETO
from main import jogo_principal  # Importa o loop do jogo de main.py
from regras import regras  # Importa a função de regras de regras.py

# Inicializar o Pygame
pygame.init()

# Criar a janela
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Dameo - Menu Inicial")

# Carregar imagem de fundo
FUNDO = pygame.image.load("assets/background.png")
FUNDO = pygame.transform.scale(FUNDO, (LARGURA, ALTURA))

# Definir fontes
fonte = pygame.font.Font(None, 50)

def desenhar_botao(win, texto, cor, x, y, largura, altura):
    """Desenha um botão na tela com texto centralizado."""
    pygame.draw.rect(win,PRETO, (x-2, y-2, largura+4, altura+4))  # Desenha o botão
    pygame.draw.rect(win, cor, (x, y, largura, altura))
    texto_render = fonte.render(texto, True, BRANCO)
    win.blit(
        texto_render,
        (
            x + (largura - texto_render.get_width()) // 2,
            y + (altura - texto_render.get_height()) // 2,
        ),
    )

def menu():
    """Exibe o menu inicial."""
    run = True
    while run:
        WIN.blit(FUNDO, (0, 0))  # Desenha a imagem de fundo
        
        # Título
        titulo = fonte.render("Bem-vindo ao Dameo!", True, BRANCO)
        WIN.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))
        
        # Botões
        largura_botao = 400
        altura_botao = 60
        espacamento = 40  # Espaçamento entre os botões

        # Calcula a posição central para o eixo X dos botões
        x_centro = (LARGURA - largura_botao) // 2

        botao_pvp = (x_centro-175, 270, largura_botao, altura_botao)
        botao_pvc = (x_centro-175, 270 + altura_botao + espacamento, largura_botao, altura_botao)
        botao_cvc = (x_centro-175, 270 + 2 * (altura_botao + espacamento), largura_botao, altura_botao)
        botao_regras = (x_centro,600, largura_botao, altura_botao)
        
        desenhar_botao(WIN, "Player vs Player", CASTANHO, *botao_pvp)
        desenhar_botao(WIN, "Player vs Computer", CASTANHO, *botao_pvc)
        desenhar_botao(WIN, "Computer vs Computer", CASTANHO, *botao_cvc)
        desenhar_botao(WIN, "Regras", CASTANHO, *botao_regras)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x_centro-175 <= x <= x_centro + largura_botao:
                    if 270 <= y <= 270 + altura_botao:
                        return "pvp"
                    elif 270 + altura_botao + espacamento <= y <= 270 + 2 * (altura_botao + espacamento):
                        return "pvc"
                    elif 270 + 2 * (altura_botao + espacamento) <= y <= 270 + 3 * (altura_botao + espacamento):
                        return "cvc"
                if x_centro <= x <= x_centro + largura_botao:
                    if 600 <= y <= 600 + altura_botao:
                        regras(WIN)
    return None

def iniciar_jogo(modo):
    """Chama o loop do jogo baseado no modo selecionado."""
    if modo == "pvp":
        print("Iniciando jogo Player vs Player...")
        jogo_principal(modo="pvp")  # Chama o jogo principal no modo PVP
    elif modo == "pvc":
        print("Iniciando jogo Player vs Computer...")
        jogo_principal(modo="pvc")  # Placeholder para PVC (a lógica ainda deve ser implementada)
    elif modo == "cvc":
        print("Iniciando jogo Computer vs Computer...")
        jogo_principal(modo="cvc")  # Placeholder para CVC (a lógica ainda deve ser implementada)

if __name__ == "__main__":
    modo = menu()  # Mostra o menu inicial e captura o modo selecionado
    if modo:
        iniciar_jogo(modo)  # Inicia o jogo com o modo selecionado
    pygame.quit()
