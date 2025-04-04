import pygame
import random
from dameo_sub.constants import LARGURA, ALTURA, TAMANHO_QUADRADO, LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.game import Game
from mcts import MCTS
from interface import menu_principal

def get_valid_moves(game):
    moves = []
    for peca in game.tabuleiro.get_all_peças(game.turn):
        valid_moves = game.tabuleiro.get_valid_moves(peca)
        for move, skip in valid_moves.items():
            moves.append((peca, move, skip))
    print(f"Movimentos válidos encontrados: {len(moves)}")
    return moves

def jogo_principal(configuracoes):
    """Função principal do jogo que recebe as configurações do menu"""
    WIN = pygame.display.set_mode((LARGURA, ALTURA))
    game = Game(WIN)
    run = True
    ai_thinking = False
    
    # Verificar se as configurações necessárias existem
    if not all(key in configuracoes for key in ["modo", "tamanho", "algoritmo", "dificuldade"]):
        print("Erro: Configurações incompletas")
        return
    
    # Configurar MCTS com parâmetros de dificuldade
    dificuldade = configuracoes["dificuldade"]
    if dificuldade == "facil":
        iterations = 200
        simulation_depth = 5
        exploration_constant = 0.5
    elif dificuldade == "medio":
        iterations = 800
        simulation_depth = 15
        exploration_constant = 1.4
    else:  # difícil
        iterations = 1500
        simulation_depth = 25
        exploration_constant = 2.0
    
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
        if (configuracoes["modo"] == "pvc" and game.turn == LARANJA and not ai_thinking) or \
           (configuracoes["modo"] == "cvc" and not ai_thinking):
            
            ai_thinking = True
            print(f"IA pensando... (cor: {game.turn}, dificuldade: {dificuldade})")
            
            while True:  # Loop para permitir múltiplas capturas
                move, is_capture = mcts.get_move(game)
                
                if not move:
                    print("IA não encontrou movimentos válidos!")
                    game.change_turn()
                    break
                    
                peca, novo_pos, skip = move
                print(f"IA escolheu mover de ({peca.linha}, {peca.coluna}) para ({novo_pos[0]}, {novo_pos[1]})")
                
                # Executar o movimento
                game.tabuleiro.movimento(peca, novo_pos[0], novo_pos[1])
                if skip:
                    game.tabuleiro.remove(skip)
                    print(f"IA capturou peças: {len(skip)}")
                    
                    # Verificar se há mais capturas disponíveis com a mesma peça
                    new_piece = game.tabuleiro.get_peça(novo_pos[0], novo_pos[1])
                    more_captures = False
                    valid_moves = game.tabuleiro.get_valid_moves(new_piece)
                    
                    for next_move, next_skip in valid_moves.items():
                        if next_skip:  # Há mais capturas disponíveis
                            more_captures = True
                            break
                    
                    if not more_captures:  # Se não há mais capturas, termina o turno
                        game.change_turn()
                        break
                else:  # Se não foi uma captura, termina o turno
                    game.change_turn()
                    break
                
                game.update(WIN)
                pygame.time.delay(500)  # Delay para visualizar o movimento
            
            ai_thinking = False
            continue

        # Processar eventos do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN and \
               (configuracoes["modo"] == "pvp" or (configuracoes["modo"] == "pvc" and game.turn == VERDE)):
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // TAMANHO_QUADRADO, pos[0] // TAMANHO_QUADRADO
                game.select(row, col)

        game.update(WIN)

    pygame.quit()

if __name__ == "__main__":
    # Iniciar o menu e obter configurações
    configuracoes = menu_principal()
    if configuracoes:
        jogo_principal(configuracoes)
    pygame.quit()
