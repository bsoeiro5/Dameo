import pygame
import random
from dameo_sub.constants import LARGURA, ALTURA, TAMANHO_QUADRADO, LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.game import Game
from mcts import MCTS

# Configuração inicial da janela
WIN = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Dameo')

def get_valid_moves(game):
    """Retorna todos os movimentos válidos, priorizando capturas."""
    moves = []
    capturas = []
    
    for peca in game.tabuleiro.get_all_peças(game.turn):
        valid_moves = game.tabuleiro.get_valid_moves(peca)
        for move, skip in valid_moves.items():
            if skip:
                capturas.append((peca, move, skip))
            else:
                moves.append((peca, move, skip))
    
    return capturas if capturas else moves

def jogo_principal(modo, dificuldade="medio"):
    WIN = pygame.display.set_mode((LARGURA, ALTURA))
    game = Game(WIN)
    run = True
    ai_thinking = False
    
    # Configurar MCTS
    if dificuldade == "facil":
        iterations = 500
    elif dificuldade == "medio":
        iterations = 1000
    else:  # difícil
        iterations = 2000
        
    mcts = MCTS(iterations=iterations)

    while run:
        if game.verificar_fim_do_jogo():
            pygame.time.delay(3000)
            run = False
            break

        # Turno da IA
        if (modo == "pvc" and game.turn == LARANJA and not ai_thinking) or \
           (modo == "cvc" and not ai_thinking):
            
            ai_thinking = True
            
            # Obter movimentos válidos
            valid_moves = get_valid_moves(game)
            
            if valid_moves:
                # Escolher um movimento
                peca, novo_pos, skip = random.choice(valid_moves)
                
                # Executar o movimento
                game.tabuleiro.movimento(peca, novo_pos[0], novo_pos[1])
                if skip:
                    game.tabuleiro.remove(skip)
                game.change_turn()
                
                # Atualizar a tela e fazer uma pausa
                game.update(WIN)
                pygame.time.delay(500)
            
            ai_thinking = False
            continue

        # Processar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and \
               (modo == "pvp" or (modo == "pvc" and game.turn == VERDE)):
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // TAMANHO_QUADRADO, pos[0] // TAMANHO_QUADRADO
                game.select(row, col)

        # Atualizar a tela
        game.update(WIN)
        pygame.time.delay(50)

    pygame.quit()

def iniciar_jogo(modo_completo):
    if modo_completo is None:
        return
    
    if "_" in modo_completo:
        modo, dificuldade = modo_completo.split("_")
    else:
        modo = modo_completo
        dificuldade = "medio"
    
    print(f"Iniciando jogo no modo {modo} com dificuldade {dificuldade}...")
    jogo_principal(modo=modo, dificuldade=dificuldade)

if __name__ == "__main__":
    from interface import menu
    modo_completo = menu()
    if modo_completo:
        iniciar_jogo(modo_completo)
    pygame.quit()
