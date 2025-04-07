import pygame
import random
import time
from dameo_sub.constants import LARGURA, ALTURA, TAMANHO_QUADRADO, LARANJA, VERDE
from dameo_sub.tabuleiro import Tabuleiro
from dameo_sub.game import Game
from mcts import MCTS
from interface import menu_principal
from metricas import metrics

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
    
    # Inicializar contadores de métricas
    move_number = 0
    game_start_time = time.time()
    metrics.game_id += 1
    metrics.reset()
    
    # Verificar se as configurações necessárias existem
    if not all(key in configuracoes for key in ["modo", "tamanho", "algoritmo", "dificuldade"]):
        print("Erro: Configurações incompletas")
        return
    
    # Configurar parâmetros baseado na dificuldade e algoritmo
    dificuldade = configuracoes["dificuldade"]
    algoritmo = configuracoes["algoritmo"]
    
    # Configurar MCTS
    if algoritmo == "mcts":
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
        
        ai = MCTS(
            iterations=iterations,
            simulation_depth=simulation_depth,
            exploration_constant=exploration_constant
        )
        print(f"MCTS configurado: {dificuldade} - {iterations} iterações, {simulation_depth} profundidade")
        metrics.set_algorithm_info("MCTS", dificuldade, simulation_depth)
    
    # Configurar Minimax/AlphaBeta
    depth = 0
    if algoritmo in ["minimax", "alphabeta"]:
        from minimax.algoritmo import minimax, alfa_beta
        # Resetar contadores globais
        from minimax.algoritmo import nos_expandidos_minimax, nos_expandidos_alphabeta
        nos_expandidos_minimax = 0
        nos_expandidos_alphabeta = 0
        
        # Ajustar profundidade para melhor qualidade das jogadas
        if dificuldade == "facil":
            depth = 2
        elif dificuldade == "medio":
            depth = 3
        else:  # difícil
            depth = 7  
            
        print(f"{algoritmo.upper()} configurado: {dificuldade} - profundidade {depth}")
        metrics.set_algorithm_info(algoritmo.upper(), dificuldade, depth)

    # Registar estado inicial do tabuleiro
    metrics.update_piece_count(game.tabuleiro.verdes_left, game.tabuleiro.laranjas_left)
    
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        if game.verificar_fim_do_jogo():
            # Registar métricas finais do jogo
            total_game_time = time.time() - game_start_time
            metrics.update_piece_count(game.tabuleiro.verdes_left, game.tabuleiro.laranjas_left)
            metrics.record_move_metrics(move_number, total_game_time)
            print(f"Jogo finalizado! Tempo total: {total_game_time:.2f} segundos")
            pygame.time.delay(3000)
            run = False
            break

        # Turno da IA
        if (configuracoes["modo"] == "pvc" and game.turn == LARANJA and not ai_thinking):
            ai_thinking = True
            move_number += 1
            print(f"\n--- Turno {move_number} da IA ---")
            print(f"IA pensando... (algoritmo: {algoritmo}, dificuldade: {dificuldade})")
            
            # Iniciar timer
            metrics.start_move_timer()
            metrics.reset()
            metrics.set_algorithm_info(algoritmo, dificuldade, depth)
            
            if algoritmo == "mcts":
                # Antes do movimento da IA
                old_green = game.tabuleiro.verdes_left
                old_orange = game.tabuleiro.laranjas_left
                
                move, is_capture = ai.get_move(game)
                
                # Registrar métricas do MCTS
                metrics.nodes_expanded = ai.nodes_expanded
                metrics.simulations_run = ai.simulations_run
                metrics.moves_considered = len(ai._get_valid_moves(game))
                metrics.evaluation_score = game.tabuleiro.heuristica()
                
                # Resetar contadores do MCTS para o próximo movimento
                ai.nodes_expanded = 0
                ai.simulations_run = 0
                
                # Processar movimento do MCTS
                if move:
                    peca, novo_pos, skip = move
                    game.tabuleiro.movimento(peca, novo_pos[0], novo_pos[1])
                    if skip:
                        game.tabuleiro.remove(skip)
                        new_piece = game.tabuleiro.get_peça(novo_pos[0], novo_pos[1])
                        more_captures = any(skip for _, skip in game.tabuleiro.get_valid_moves(new_piece).items())
                        if not more_captures:
                            game.change_turn()
                    else:
                        game.change_turn()
                else:
                    game.change_turn()
            else:
                # Usar minimax ou alpha-beta
                try:
                    print(f"\nIniciando {algoritmo}...")
                    print(f"Estado atual do tabuleiro antes da IA:")
                    print(f"Peças verdes: {game.tabuleiro.verdes_left}")
                    print(f"Peças laranjas: {game.tabuleiro.laranjas_left}")
                    
                    # Antes do movimento da IA
                    old_green = game.tabuleiro.verdes_left
                    old_orange = game.tabuleiro.laranjas_left
                    
                    # Verifica se há capturas obrigatórias primeiro
                    capturas_obrigatorias = []
                    for piece in game.tabuleiro.get_all_peças(LARANJA):
                        valid_moves = game.tabuleiro.get_valid_moves(piece)
                        for move, skip in valid_moves.items():
                            if skip:
                                capturas_obrigatorias.append((piece, move, skip))
                    
                    if capturas_obrigatorias:
                        print(f"Encontradas {len(capturas_obrigatorias)} capturas obrigatórias")
                        # Escolher a melhor captura (poderia ser mais sofisticado)
                        peca, move, skip = capturas_obrigatorias[0]
                        game.tabuleiro.movimento(peca, move[0], move[1])
                        game.tabuleiro.remove(skip)
                        
                        # Verificar capturas em sequência
                        new_piece = game.tabuleiro.get_peça(move[0], move[1])
                        more_captures = any(skip for _, skip in game.tabuleiro.get_valid_moves(new_piece).items())
                        if not more_captures:
                            game.change_turn()
                    else:
                        if algoritmo == "minimax":
                            # Resetar contador global
                            from minimax.algoritmo import nos_expandidos_minimax
                            nos_expandidos_minimax = 0
                            
                            # Adicionar tempo de início para limitar o tempo de processamento
                            from minimax.algoritmo import minimax
                            minimax.start_time = time.time()
                            
                            score, best_board = minimax(game.tabuleiro, depth, False, game)
                            print(f"Minimax retornou score: {score}")
                            
                            # Registar métricas
                            from minimax.algoritmo import nos_expandidos_minimax
                            metrics.nodes_expanded = nos_expandidos_minimax
                            metrics.evaluation_score = score
                                
                            if best_board:
                                print("Tabuleiro válido retornado, aplicando movimento...")
                                game.ai_move(best_board)
                            else:
                                print("IA não encontrou movimentos válidos!")
                                game.change_turn()
                        else:  # alphabeta
                            # Resetar contador global
                            from minimax.algoritmo import nos_expandidos_alphabeta
                            nos_expandidos_alphabeta = 0
                            
                            # Adicionar tempo de início para limitar o tempo de processamento
                            from minimax.algoritmo import alfa_beta
                            alfa_beta.start_time = time.time()
                            
                            score, best_board = alfa_beta(game.tabuleiro, depth, float('-inf'), float('inf'), False, game)
                            print(f"Alpha-beta retornou score: {score}")
                            
                            # Registar métricas
                            from minimax.algoritmo import nos_expandidos_alphabeta
                            metrics.nodes_expanded = nos_expandidos_alphabeta
                            metrics.evaluation_score = score
                            from minimax.algoritmo import nos_podados_alphabeta
                            metrics.nodes_pruned = nos_podados_alphabeta
                            
                            if best_board:
                                print("Tabuleiro válido retornado, aplicando movimento...")
                                game.ai_move(best_board)
                            else:
                                print("IA não encontrou movimentos válidos!")
                                game.change_turn()
                except Exception as e:
                    print(f"Erro ao executar {algoritmo}: {e}")
                    import traceback
                    traceback.print_exc()
                    game.change_turn()
            
            # Parar timer e registar métricas
            metrics.stop_move_timer()
            metrics.update_piece_count(game.tabuleiro.verdes_left, game.tabuleiro.laranjas_left)
            metrics.print_move_summary(move_number)
            metrics.record_move_metrics(move_number)
            
            # Mostrar diferença no tabuleiro após o movimento
            print(f"Peças capturadas: Verde: {old_green - game.tabuleiro.verdes_left}, Laranja: {old_orange - game.tabuleiro.laranjas_left}")
            
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
                selected = game.select(row, col)
                
                # Se um movimento foi feito, registe
                if selected and game.turn == LARANJA:  # O turno mudou depois do movimento
                    move_number += 1
                    print(f"\n--- Turno {move_number} do Jogador ---")
                    metrics.update_piece_count(game.tabuleiro.verdes_left, game.tabuleiro.laranjas_left)

        game.update(WIN)

    pygame.quit()

if __name__ == "__main__":
    # Iniciar o menu e obter configurações
    configuracoes = menu_principal()
    if configuracoes:
        jogo_principal(configuracoes)
    pygame.quit()
