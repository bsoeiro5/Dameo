import pygame
import sys
from dameo_sub.constants import LARGURA, ALTURA, BRANCO, CASTANHO, PRETO
from regras import regras

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
fonte_subtitulo = pygame.font.Font(None, 40)

def desenhar_botao(win, texto, cor, x, y, largura, altura, selecionado=False):
    """Desenha um botão na tela com texto centralizado."""
    # Desenha borda mais grossa se selecionado
    borda = 4 if selecionado else 2
    pygame.draw.rect(win, PRETO, (x-borda, y-borda, largura+2*borda, altura+2*borda))
    pygame.draw.rect(win, cor, (x, y, largura, altura))
    texto_render = fonte.render(texto, True, BRANCO)
    win.blit(
        texto_render,
        (
            x + (largura - texto_render.get_width()) // 2,
            y + (altura - texto_render.get_height()) // 2,
        ),
    )

def desenhar_botao_voltar(win, x, y, largura, altura):
    """Desenha o botão voltar."""
    pygame.draw.rect(win, PRETO, (x-2, y-2, largura+4, altura+4))
    pygame.draw.rect(win, CASTANHO, (x, y, largura, altura))
    texto_voltar = fonte_subtitulo.render("Voltar", True, BRANCO)
    win.blit(
        texto_voltar,
        (
            x + (largura - texto_voltar.get_width()) // 2,
            y + (altura - texto_voltar.get_height()) // 2,
        ),
    )

def menu_principal():
    """Menu principal com opções Jogar e Regras."""
    run = True
    while run:
        WIN.blit(FUNDO, (0, 0))
        
        titulo = fonte.render("Bem-vindo ao Dameo!", True, BRANCO)
        WIN.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))
        
        largura_botao = 300
        altura_botao = 60
        x_centro = 100  # Changed from centered to left side
        
        desenhar_botao(WIN, "Jogar", CASTANHO, x_centro, 300, largura_botao, altura_botao)
        desenhar_botao(WIN, "Regras", CASTANHO, x_centro, 400, largura_botao, altura_botao)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x_centro <= x <= x_centro + largura_botao:
                    if 300 <= y <= 300 + altura_botao:
                        return menu_tamanho_tabuleiro()
                    elif 400 <= y <= 400 + altura_botao:
                        regras(WIN)

def menu_tamanho_tabuleiro():
    """Menu de seleção do tamanho do tabuleiro."""
    run = True
    selecionado = None
    voltar_largura = 120
    voltar_altura = 50
    voltar_x = (LARGURA - voltar_largura) // 2  # Centered horizontally
    voltar_y = ALTURA - voltar_altura - 20  # 20 pixels from bottom
    
    while run:
        WIN.blit(FUNDO, (0, 0))
        
        # Desenha o botão voltar
        desenhar_botao_voltar(WIN, voltar_x, voltar_y, voltar_largura, voltar_altura)
        
        titulo = fonte.render("Selecione o Tamanho do Tabuleiro", True, BRANCO)
        WIN.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))
        
        largura_botao = 300
        altura_botao = 60
        x_centro = 100  # Changed from centered to left side
        
        desenhar_botao(WIN, "6x6", CASTANHO, x_centro, 200, largura_botao, altura_botao, selecionado == "6x6")
        desenhar_botao(WIN, "8x8", CASTANHO, x_centro, 300, largura_botao, altura_botao, selecionado == "8x8")
        desenhar_botao(WIN, "12x12", CASTANHO, x_centro, 400, largura_botao, altura_botao, selecionado == "12x12")
        
        if selecionado:  # Só mostra o botão continuar se houver seleção
            desenhar_botao(WIN, "Continuar", CASTANHO, x_centro, 500, largura_botao, altura_botao)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return menu_principal()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Verifica se clicou no botão "Voltar"
                if voltar_x <= x <= voltar_x + voltar_largura and voltar_y <= y <= voltar_y + voltar_altura:
                    return menu_principal()
                if x_centro <= x <= x_centro + largura_botao:
                    if 200 <= y <= 200 + altura_botao:
                        selecionado = "6x6"
                    elif 300 <= y <= 300 + altura_botao:
                        selecionado = "8x8"
                    elif 400 <= y <= 400 + altura_botao:
                        selecionado = "12x12"
                    elif 500 <= y <= 500 + altura_botao and selecionado:
                        return menu_algoritmo(selecionado)

def menu_algoritmo(tamanho):
    """Menu de seleção do algoritmo."""
    run = True
    selecionado = None
    voltar_largura = 120
    voltar_altura = 50
    voltar_x = (LARGURA - voltar_largura) // 2  # Centered horizontally
    voltar_y = ALTURA - voltar_altura - 20  # 20 pixels from bottom
    
    while run:
        WIN.blit(FUNDO, (0, 0))
        
        # Desenha o botão voltar
        desenhar_botao_voltar(WIN, voltar_x, voltar_y, voltar_largura, voltar_altura)
        
        titulo = fonte.render("Selecione o Algoritmo", True, BRANCO)
        WIN.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))
        
        largura_botao = 300  # Changed from 400 to 300 to match other buttons
        altura_botao = 60
        x_centro = 100  # Changed from 35 to 100 to align with other buttons
        
        # Desenha os botões com destaque para o selecionado
        desenhar_botao(WIN, "MCTS", CASTANHO, x_centro, 200, largura_botao, altura_botao, selecionado == "mcts")
        desenhar_botao(WIN, "Minimax", CASTANHO, x_centro, 300, largura_botao, altura_botao, selecionado == "minimax")
        desenhar_botao(WIN, "Alpha-Beta", CASTANHO, x_centro, 400, largura_botao, altura_botao, selecionado == "alphabeta")
        
        if selecionado:  # Só mostra o botão continuar se houver seleção
            desenhar_botao(WIN, "Continuar", CASTANHO, x_centro, 500, largura_botao, altura_botao)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return menu_tamanho_tabuleiro()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Verifica se clicou no botão "Voltar"
                if voltar_x <= x <= voltar_x + voltar_largura and voltar_y <= y <= voltar_y + voltar_altura:
                    return menu_tamanho_tabuleiro()
                if x_centro <= x <= x_centro + largura_botao:
                    if 200 <= y <= 200 + altura_botao:
                        selecionado = "mcts"
                    elif 300 <= y <= 300 + altura_botao:
                        selecionado = "minimax"
                    elif 400 <= y <= 400 + altura_botao:
                        selecionado = "alphabeta"
                    elif 500 <= y <= 500 + altura_botao and selecionado:
                        return menu_dificuldade(tamanho, selecionado)

def menu_dificuldade(tamanho, algoritmo):
    """Menu de seleção da dificuldade."""
    run = True
    selecionado = None
    voltar_largura = 120
    voltar_altura = 50
    voltar_x = (LARGURA - voltar_largura) // 2  # Centered horizontally
    voltar_y = ALTURA - voltar_altura - 20  # 20 pixels from bottom
    
    while run:
        WIN.blit(FUNDO, (0, 0))
        
        # Desenha o botão voltar
        desenhar_botao_voltar(WIN, voltar_x, voltar_y, voltar_largura, voltar_altura)
        
        titulo = fonte.render("Selecione a Dificuldade", True, BRANCO)
        WIN.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))
        
        largura_botao = 300
        altura_botao = 60
        x_centro = 100
        
        # Desenha os botões com destaque para o selecionado
        desenhar_botao(WIN, "Fácil", CASTANHO, x_centro, 200, largura_botao, altura_botao, selecionado == "facil")
        desenhar_botao(WIN, "Médio", CASTANHO, x_centro, 300, largura_botao, altura_botao, selecionado == "medio")
        desenhar_botao(WIN, "Difícil", CASTANHO, x_centro, 400, largura_botao, altura_botao, selecionado == "dificil")
        
        if selecionado:  # Só mostra o botão continuar se houver seleção
            desenhar_botao(WIN, "Continuar", CASTANHO, x_centro, 500, largura_botao, altura_botao)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return menu_algoritmo(tamanho)
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Verifica se clicou no botão "Voltar"
                if voltar_x <= x <= voltar_x + voltar_largura and voltar_y <= y <= voltar_y + voltar_altura:
                    return menu_algoritmo(tamanho)
                if x_centro <= x <= x_centro + largura_botao:
                    if 200 <= y <= 200 + altura_botao:
                        selecionado = "facil"
                    elif 300 <= y <= 300 + altura_botao:
                        selecionado = "medio"
                    elif 400 <= y <= 400 + altura_botao:
                        selecionado = "dificil"
                    elif 500 <= y <= 500 + altura_botao and selecionado:
                        return iniciar_jogo(tamanho, algoritmo, selecionado)

def iniciar_jogo(tamanho, algoritmo, dificuldade):
    """Retorna as configurações selecionadas."""
    print(f"Configurações selecionadas: Tamanho {tamanho}, Algoritmo {algoritmo}, Dificuldade {dificuldade}")
    return {
        "tamanho": tamanho, 
        "algoritmo": algoritmo, 
        "dificuldade": dificuldade,
        "modo": "pvc"  # Player vs Computer mode
    }

if __name__ == "__main__":
    print("Please run the game through main.py")
