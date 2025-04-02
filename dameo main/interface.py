import pygame
import sys
from dameo_sub.constants import LARGURA, ALTURA, BRANCO, AZUL_CLARO, CASTANHO, PRETO, set_board_size, get_board_size
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
fonte_subtitulo = pygame.font.Font(None, 40)

def desenhar_botao(win, texto, cor, x, y, largura, altura):
    """Desenha um botão na tela com texto centralizado."""
    pygame.draw.rect(win, PRETO, (x-2, y-2, largura+4, altura+4))  # Desenha o botão
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
    global FUNDO  # Declare FUNDO as global to modify the global variable
    run = True
    board_size = "8x8"  # Default board size

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
        botao_regras = (x_centro, 600, largura_botao, altura_botao)

        # Board size buttons
        largura_botao_tabuleiro = 150
        altura_botao_tabuleiro = 50
        x_tabuleiro = (LARGURA - (3 * largura_botao_tabuleiro + 2 * espacamento)) // 2
        y_tabuleiro = 180

        botao_6x6 = (x_tabuleiro, y_tabuleiro, largura_botao_tabuleiro, altura_botao_tabuleiro)
        botao_8x8 = (x_tabuleiro + largura_botao_tabuleiro + espacamento, y_tabuleiro, largura_botao_tabuleiro, altura_botao_tabuleiro)
        botao_12x12 = (x_tabuleiro + 2 * (largura_botao_tabuleiro + espacamento), y_tabuleiro, largura_botao_tabuleiro, altura_botao_tabuleiro)

        # Highlight selected board size
        cor_6x6 = AZUL_CLARO if board_size == "6x6" else CASTANHO
        cor_8x8 = AZUL_CLARO if board_size == "8x8" else CASTANHO
        cor_12x12 = AZUL_CLARO if board_size == "12x12" else CASTANHO

        desenhar_botao(WIN, "6x6", cor_6x6, *botao_6x6)
        desenhar_botao(WIN, "8x8", cor_8x8, *botao_8x8)
        desenhar_botao(WIN, "12x12", cor_12x12, *botao_12x12)

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

                # Check board size buttons
                if botao_6x6[0] <= x <= botao_6x6[0] + botao_6x6[2] and botao_6x6[1] <= y <= botao_6x6[1] + botao_6x6[3]:
                    FUNDO = pygame.image.load("assets/background_6x6.png")
                    FUNDO = pygame.transform.scale(FUNDO, (LARGURA, ALTURA))
                    board_size = "6x6"
                elif botao_8x8[0] <= x <= botao_8x8[0] + botao_8x8[2] and botao_8x8[1] <= y <= botao_8x8[1] + botao_8x8[3]:
                    FUNDO = pygame.image.load("assets/background.png")
                    FUNDO = pygame.transform.scale(FUNDO, (LARGURA, ALTURA))
                    board_size = "8x8"
                elif botao_12x12[0] <= x <= botao_12x12[0] + botao_12x12[2] and botao_12x12[1] <= y <= botao_12x12[1] + botao_12x12[3]:
                    FUNDO = pygame.image.load("assets/background_12x12.png")
                    FUNDO = pygame.transform.scale(FUNDO, (LARGURA, ALTURA))
                    board_size = "12x12"

                # Check game mode buttons
                if x_centro-175 <= x <= x_centro-175 + largura_botao:
                    if 270 <= y <= 270 + altura_botao:
                        return "pvp", board_size
                    elif 270 + altura_botao + espacamento <= y <= 270 + 2 * altura_botao + espacamento:
                        return selecionar_dificuldade("pvc"), board_size
                    elif 270 + 2 * (altura_botao + espacamento) <= y <= 270 + 3 * altura_botao + 2 * espacamento:
                        return selecionar_dificuldade("cvc"), board_size
                if x_centro <= x <= x_centro + largura_botao:
                    if 600 <= y <= 600 + altura_botao:
                        regras(WIN)
    return None, board_size

def selecionar_dificuldade(modo):
    """Exibe a tela de seleção de dificuldade."""
    run = True
    dificuldade_selecionada = None
    
    while run:
        WIN.blit(FUNDO, (0, 0))  # Desenha a imagem de fundo
        
        # Título
        titulo = fonte.render("Selecione a Dificuldade", True, BRANCO)
        WIN.blit(titulo, ((LARGURA - titulo.get_width()) // 2, 50))
        
        # Subtítulo - mostra o modo selecionado
        modo_texto = "Jogador vs Computador" if modo == "pvc" else "Computador vs Computador"
        subtitulo = fonte_subtitulo.render(f"Modo: {modo_texto}", True, BRANCO)
        WIN.blit(subtitulo, ((LARGURA - subtitulo.get_width()) // 2, 120))
        
        # Botões
        largura_botao = 300
        altura_botao = 60
        espacamento = 40  # Espaçamento entre os botões
        
        # Calcula a posição central para o eixo X dos botões
        x_centro = (LARGURA - largura_botao) // 2
        
        botao_facil = (x_centro-175, 270, largura_botao, altura_botao)
        botao_medio = (x_centro-175, 270 + altura_botao + espacamento, largura_botao, altura_botao)
        botao_dificil = (x_centro-175, 270 + 2 * (altura_botao + espacamento), largura_botao, altura_botao)
        botao_voltar = (x_centro,  600, largura_botao, altura_botao)
        
        desenhar_botao(WIN, "Fácil", CASTANHO, *botao_facil)
        desenhar_botao(WIN, "Médio", CASTANHO, *botao_medio)
        desenhar_botao(WIN, "Difícil", CASTANHO, *botao_dificil)
        desenhar_botao(WIN, "Voltar", CASTANHO, *botao_voltar)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(f"Mouse clicked at: x={x}, y={y}")  # Debugging mouse position
                print(f"x_centro: {x_centro}, largura_botao: {largura_botao}")  # Debugging button position

                if x_centro-175 <= x <= x_centro-175 + largura_botao:
                    if 270 <= y <= 270 + altura_botao:
                        dificuldade_selecionada = "facil"
                        run = False
                    elif 270 + altura_botao + espacamento <= y <= 270 + 2 * altura_botao + espacamento:
                        dificuldade_selecionada = "medio"
                        run = False
                    elif 270 + 2 * (altura_botao + espacamento) <= y <= 270 + 3 * altura_botao + 2 * espacamento:
                        dificuldade_selecionada = "dificil"
                        run = False
                elif x_centro <= x <= x_centro + largura_botao:  # Check "Voltar" button
                    if 600 <= y <= 600 + altura_botao:
                        print("Voltar button clicked!")  # Debugging button click
                        return menu()  # Volta para o menu principal
    
    if dificuldade_selecionada:
        return f"{modo}_{dificuldade_selecionada}"  # Retorna o modo e a dificuldade concatenados
    return None

def iniciar_jogo(modo_completo, board_size):
    """Chama o loop do jogo baseado no modo e dificuldade selecionados."""
    if modo_completo is None:
        return
    
    # Verifica se o modo inclui uma dificuldade
    if "_" in modo_completo:
        modo, dificuldade = modo_completo.split("_")
    else:
        modo = modo_completo
        dificuldade = "medio"  # Dificuldade padrão

    # Update board size globally
    if board_size == "6x6":
        set_board_size(6, 6)
    elif board_size == "8x8":
        set_board_size(8, 8)
    elif board_size == "12x12":
        set_board_size(12, 12)

    print(f"Iniciando jogo no modo {modo} com dificuldade {dificuldade} e tamanho do tabuleiro {board_size}...")

    if modo == "pvp":
        jogo_principal(modo="pvp", dificuldade=dificuldade)
    elif modo == "pvc":
        jogo_principal(modo="pvc", dificuldade=dificuldade)
    elif modo == "cvc":
        jogo_principal(modo="cvc", dificuldade=dificuldade)

if __name__ == "__main__":
    modo_completo, board_size = menu()  # Mostra o menu inicial e captura o modo+dificuldade selecionados
    if modo_completo:
        iniciar_jogo(modo_completo, board_size)  # Inicia o jogo com o modo, dificuldade e tamanho do tabuleiro selecionados
    pygame.quit()
