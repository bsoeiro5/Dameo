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
FUNDO = pygame.image.load("assets/background.png.jpeg")
FUNDO = pygame.transform.scale(FUNDO, (LARGURA, ALTURA))

# Definir fontes
fonte = pygame.font.Font(None, 50)
fonte_subtitulo = pygame.font.Font(None, 40)

def desenhar_botao(win, texto, cor, x, y, largura, altura):
    """Desenha um botão na tela com texto centralizado e contorno preto."""
    pygame.draw.rect(win, PRETO, (x-2, y-2, largura+4, altura+4))  # contorno preto
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
        WIN.blit(FUNDO, (0, 0))
        
        # Título
        titulo = fonte.render("Bem-vindo ao Dameo!", True, BRANCO)
        WIN.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))
        
        # Botões
        largura_botao = 400
        altura_botao = 60
        espacamento = 40  # Espaçamento entre botões

        x_centro = (LARGURA - largura_botao) // 2

        botao_pvp = (x_centro - 175, 270, largura_botao, altura_botao)
        botao_pvc = (x_centro - 175, 270 + altura_botao + espacamento, largura_botao, altura_botao)
        botao_cvc = (x_centro - 175, 270 + 2 * (altura_botao + espacamento), largura_botao, altura_botao)
        botao_regras = (x_centro, 600, largura_botao, altura_botao)
        
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
                if x_centro - 175 <= x <= x_centro - 175 + largura_botao:
                    if 270 <= y <= 270 + altura_botao:
                        return "pvp"
                    elif 270 + altura_botao + espacamento <= y <= 270 + 2 * altura_botao + espacamento:
                        return selecionar_dificuldade("pvc")
                    elif 270 + 2*(altura_botao + espacamento) <= x <= 270 + 3*altura_botao + 2*espacamento:
                        return selecionar_dificuldade("cvc")
                if x_centro <= x <= x_centro + largura_botao:
                    if 600 <= y <= 600 + altura_botao:
                        regras(WIN)  # Exibe as regras
    return None

def selecionar_dificuldade(modo):
    """Exibe a tela de seleção de dificuldade com botão 'Voltar' no canto superior esquerdo."""
    run = True
    dificuldade_selecionada = None

    # Parâmetros do botão "Voltar" (canto superior esquerdo)
    voltar_x = 20
    voltar_y = 20
    voltar_largura = 120
    voltar_altura = 50
    
    while run:
        WIN.blit(FUNDO, (0, 0))
        
        # Título
        titulo = fonte.render("Selecione a Dificuldade", True, BRANCO)
        WIN.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))
        
        # Subtítulo - mostra o modo selecionado
        modo_texto = "Jogador vs Computador" if modo == "pvc" else "Computador vs Computador"
        subtitulo = fonte_subtitulo.render(f"Modo: {modo_texto}", True, BRANCO)
        WIN.blit(subtitulo, ((LARGURA - subtitulo.get_width()) // 2, 120))
        
        # Botões de dificuldade
        largura_botao = 300
        altura_botao = 60
        espacamento = 40

        x_centro = (LARGURA - largura_botao) // 2

        botao_facil = (x_centro - 175, 270, largura_botao, altura_botao)
        botao_medio = (x_centro - 175, 270 + altura_botao + espacamento, largura_botao, altura_botao)
        botao_dificil = (x_centro - 175, 270 + 2*(altura_botao + espacamento), largura_botao, altura_botao)
        
        desenhar_botao(WIN, "Fácil", CASTANHO, *botao_facil)
        desenhar_botao(WIN, "Médio", CASTANHO, *botao_medio)
        desenhar_botao(WIN, "Difícil", CASTANHO, *botao_dificil)
        
        # Botão "Voltar" no canto superior esquerdo
        desenhar_botao(WIN, "Voltar", CASTANHO, voltar_x, voltar_y, voltar_largura, voltar_altura)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Verifica se clicou no botão "Voltar"
                if voltar_x <= x <= voltar_x + voltar_largura and voltar_y <= y <= voltar_y + voltar_altura:
                    return menu()
                
                # Verifica os botões de dificuldade (na área central)
                if x_centro - 175 <= x <= x_centro - 175 + largura_botao:
                    if 270 <= y <= 270 + altura_botao:
                        dificuldade_selecionada = "facil"
                        run = False
                    elif 270 + altura_botao + espacamento <= y <= 270 + 2 * altura_botao + espacamento:
                        dificuldade_selecionada = "medio"
                        run = False
                    elif 270 + 2*(altura_botao+espacamento) <= y <= 270 + 3*altura_botao + 2*espacamento:
                        dificuldade_selecionada = "dificil"
                        run = False
    if dificuldade_selecionada:
        return f"{modo}_{dificuldade_selecionada}"
    return None

def iniciar_jogo(modo_completo):
    """Chama o loop do jogo baseado no modo e dificuldade selecionados."""
    if modo_completo is None:
        return
    
    if "_" in modo_completo:
        modo, dificuldade = modo_completo.split("_")
    else:
        modo = modo_completo
        dificuldade = "medio"
    
    print(f"Iniciando jogo no modo {modo} com dificuldade {dificuldade}...")
    
    if modo == "pvp":
        jogo_principal(modo="pvp")
    elif modo == "pvc":
        jogo_principal(modo="pvc", dificuldade=dificuldade)
    elif modo == "cvc":
        jogo_principal(modo="cvc", dificuldade=dificuldade)

if __name__ == "__main__":
    modo_completo = menu()
    if modo_completo:
        iniciar_jogo(modo_completo)
    pygame.quit()
    sys.exit()
# Código finalizado com sucesso.
