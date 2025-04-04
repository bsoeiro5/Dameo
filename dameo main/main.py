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
    moves = []
    for peca in game.tabuleiro.get_all_peças(game.turn):
        valid_moves = game.tabuleiro.get_valid_moves(peca)
        for move, skip in valid_moves.items():
            moves.append((peca, move, skip))
    print(f"Movimentos válidos encontrados: {len(moves)}")
    return moves

def jogo_principal(modo, dificuldade="medio"):
    WIN = pygame.display.set_mode((LARGURA, ALTURA))
    game = Game(WIN)
    run = True
    ai_thinking = False
    
    # Configurar MCTS com parâmetros de dificuldade mais significativos
    if dificuldade == "facil":
        iterations = 200  # Reduzido para decisões mais rápidas e menos precisas
        simulation_depth = 5  # Profundidade de simulação menor = visão mais limitada
        exploration_constant = 0.5  # Menor exploração, mais foco em movimentos já conhecidos
    elif dificuldade == "medio":
        iterations = 800
        simulation_depth = 15
        exploration_constant = 1.4
    else:  # difícil
        iterations = 1500  # Mais iterações = decisões mais refinadas
        simulation_depth = 25  # Olha mais longe no futuro
        exploration_constant = 2.0  # Mais exploração para encontrar movimentos menos óbvios
    
    print(f"Configuração da IA: {dificuldade} - {iterations} iterações, {simulation_depth} profundidade")
    
    mcts = MCTS(
        iterations=iterations,
        simulation_depth=simulation_depth,
        exploration_constant=exploration_constant
    )

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)  # Limitar a 60 FPS para não sobrecarregar o CPU
        
        if game.verificar_fim_do_jogo():
            pygame.time.delay(3000)
            run = False
            break

        # Turno da IA
        if (modo == "pvc" and game.turn == LARANJA and not ai_thinking) or \
           (modo == "cvc" and not ai_thinking):
            
            ai_thinking = True
            print(f"IA pensando... (cor: {game.turn}, dificuldade: {dificuldade})")
            
            # CORREÇÃO: Verificar primeiro se há capturas obrigatórias
            capture_moves = []
            for peca in game.tabuleiro.get_all_peças(game.turn):
                valid_moves = game.tabuleiro.get_valid_moves(peca)
                for move, skip in valid_moves.items():
                    if skip:  # Este é um movimento de captura
                        capture_moves.append((peca, move, skip))
            
            if capture_moves:
                print(f"IA: Encontradas {len(capture_moves)} capturas obrigatórias")
                # Usar MCTS para escolher entre os movimentos de captura
                move = mcts.get_move(game)
            else:
                # Sem capturas obrigatórias, usar MCTS normalmente
                move = mcts.get_move(game)
            
            if move:
                peca, novo_pos, skip = move
                print(f"IA escolheu mover de ({peca.linha}, {peca.coluna}) para ({novo_pos[0]}, {novo_pos[1]})")
                
                # Verificar se é um movimento válido
                valid_moves = game.tabuleiro.get_valid_moves(peca)
                if (novo_pos[0], novo_pos[1]) in valid_moves:
                    # Executar o movimento
                    game.tabuleiro.movimento(peca, novo_pos[0], novo_pos[1])
                    if skip:
                        game.tabuleiro.remove(skip)
                        print(f"IA capturou peças: {len(skip)}")
                    game.change_turn()
                else:
                    print("ERRO: Movimento inválido escolhido pela IA!")
                
                game.update(WIN)
                pygame.time.delay(500)  # Pequeno delay para visualizar o movimento da IA
            else:
                print("IA não encontrou movimentos válidos!")
                game.change_turn()
            
            ai_thinking = False
            continue

        # Processar eventos do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and \
               (modo == "pvp" or (modo == "pvc" and game.turn == VERDE)):
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // TAMANHO_QUADRADO, pos[0] // TAMANHO_QUADRADO
                game.select(row, col)

        game.update(WIN)

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
