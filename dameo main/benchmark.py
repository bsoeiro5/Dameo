import pygame
import time
import csv
from datetime import datetime
from dameo_sub.constants import VERDE, LARANJA
from dameo_sub.game import Game
from mcts import MCTS
from metricas import metrics

def run_benchmark_game(algoritmo, dificuldade, num_movimentos=30, max_time_per_move=5):
    """Executa um jogo de benchmark para coleta de métricas"""
    print(f"\n=== INICIANDO BENCHMARK: {algoritmo.upper()} - {dificuldade.upper()} ===")
    move_times = []
    
    # Configurações iniciais
    WIN = pygame.display.set_mode((800, 800))
    pygame.display.set_caption(f"Dameo - Benchmark {algoritmo}")
    game = Game(WIN)
    
    # Configurar o algoritmo específico
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
        depth = simulation_depth
    else:  # minimax ou alphabeta
        from minimax.algoritmo import minimax, alfa_beta
        
        if dificuldade == "facil":
            depth = 2
        elif dificuldade == "medio":
            depth = 3
        else:  # difícil
            depth = 4
    
    # Inicializar métricas
    metrics.game_id += 1
    metrics.reset()
    metrics.set_algorithm_info(algoritmo, dificuldade, depth)
    
    # Dados para o relatório
    benchmark_data = {
        "algoritmo": algoritmo,
        "dificuldade": dificuldade,
        "total_nodes": 0,
        "total_time": 0,
        "moves_completed": 0,
        "avg_time_per_move": 0,
        "avg_nodes_per_move": 0,
        "individual_move_times": []  # Nova lista para tempos individuais
    }
    
    # Loop principal do benchmark
    move_number = 0
    game_start_time = time.perf_counter()  # Usar perf_counter para maior precisão
    
    while move_number < num_movimentos:
        if game.verificar_fim_do_jogo():
            print(f"Jogo terminou após {move_number} movimentos.")
            break
        
        # Turno da IA
        if game.turn == LARANJA:
            move_number += 1
            print(f"\nBenchmark - Movimento {move_number}/{num_movimentos}")
            
            try:
                start_time = time.perf_counter()  # Início da medição
                
                if algoritmo == "mcts":
                    move, is_capture = ai.get_move(game)
                    
                    if move:
                        peca, novo_pos, skip = move
                        game.tabuleiro.movimento(peca, novo_pos[0], novo_pos[1])
                        if skip:
                            game.tabuleiro.remove(skip)
                    
                    nodes_expanded = ai.nodes_expanded
                    ai.nodes_expanded = 0  # Reset contador
                    
                elif algoritmo == "minimax":
                    from minimax.algoritmo import nos_expandidos_minimax
                    nos_expandidos_minimax = 0
                    best_score = float('-inf')
                    best_move = None
                    
                    # Começar da profundidade máxima e ir diminuindo
                    for current_depth in range(depth, 0, -1):
                        current_time = time.perf_counter() - start_time
                        if current_time > max_time_per_move:
                            print(f"Tempo limite ({max_time_per_move}s) atingido na profundidade {current_depth}")
                            break
                            
                        try:
                            print(f"Tentando profundidade {current_depth}...")
                            score, board = minimax(game.tabuleiro, current_depth, False, game)
                            if board:
                                best_score = score
                                best_move = board
                                print(f"Movimento encontrado na profundidade {current_depth}")
                        except Exception as e:
                            print(f"Erro na profundidade {current_depth}: {e}")
                            break

                    nodes_expanded = nos_expandidos_minimax
                    print(f"Nós expandidos: {nodes_expanded}")
                    
                    if best_move:
                        game.ai_move(best_move)
                    else:
                        print("Nenhum movimento válido encontrado!")

                else:  # alphabeta
                    from minimax.algoritmo import nos_expandidos_alphabeta
                    nos_expandidos_alphabeta = 0
                    best_score = float('-inf')
                    best_move = None
                    
                    # Começar da profundidade máxima e ir diminuindo
                    for current_depth in range(depth, 0, -1):
                        current_time = time.perf_counter() - start_time
                        if current_time > max_time_per_move:
                            print(f"Tempo limite ({max_time_per_move}s) atingido na profundidade {current_depth}")
                            break
                            
                        try:
                            print(f"Tentando profundidade {current_depth}...")
                            score, board = alfa_beta(game.tabuleiro, current_depth, float('-inf'), float('inf'), False, game)
                            if board:
                                best_score = score
                                best_move = board
                                print(f"Movimento encontrado na profundidade {current_depth}")
                        except Exception as e:
                            print(f"Erro na profundidade {current_depth}: {e}")
                            break

                    nodes_expanded = nos_expandidos_alphabeta
                    print(f"Nós expandidos: {nodes_expanded}")
                    
                    if best_move:
                        game.ai_move(best_move)
                    else:
                        print("Nenhum movimento válido encontrado!")
                
                end_time = time.perf_counter()  # Fim da medição
                move_time = (end_time - start_time) * 1000  # Converter para milissegundos
                
                # Registrar tempo e métricas
                move_times.append(move_time)
                benchmark_data["individual_move_times"].append(move_time)
                benchmark_data["total_nodes"] += nodes_expanded
                print(f"Tempo do movimento {move_number}: {move_time:.2f}ms")
                
                # Atualizar dados do benchmark
                benchmark_data["moves_completed"] = move_number
                
            except Exception as e:
                print(f"Erro durante o benchmark: {e}")
                import traceback
                traceback.print_exc()
                break
            
            # Atualizar tela para visualização
            game.update(WIN)
            pygame.time.delay(500)
            
        else:  # Turno do jogador (movimento aleatório)
            valid_moves = []
            for peca in game.tabuleiro.get_all_peças(VERDE):
                moves = game.tabuleiro.get_valid_moves(peca)
                for move, skip in moves.items():
                    valid_moves.append((peca, move, skip))
            
            if valid_moves:
                import random
                peca, move, skip = random.choice(valid_moves)
                game.tabuleiro.movimento(peca, move[0], move[1])
                if skip:
                    game.tabuleiro.remove(skip)
                game.change_turn()
                
                game.update(WIN)
                pygame.time.delay(300)
            else:
                print("Jogador não tem movimentos válidos. Jogo termina.")
                break
    
    # Calcular médias finais
    if move_times:
        benchmark_data["total_time"] = sum(move_times)
        benchmark_data["avg_time_per_move"] = sum(move_times) / len(move_times)
    
    if benchmark_data["moves_completed"] > 0:
        benchmark_data["avg_nodes_per_move"] = benchmark_data["total_nodes"] / benchmark_data["moves_completed"]
    
    # Tempo total do jogo
    total_game_time = time.perf_counter() - game_start_time
    
    # Exibir resultados detalhados
    print("\n=== RESULTADOS DO BENCHMARK ===")
    print(f"Algoritmo: {algoritmo.upper()}")
    print(f"Dificuldade: {dificuldade.upper()}")
    print(f"Movimentos completados: {benchmark_data['moves_completed']}/{num_movimentos}")
    print("\nTempos individuais dos movimentos:")
    for i, t in enumerate(move_times, 1):
        print(f"Movimento {i}: {t:.2f}ms")
    print(f"\nTempo total de processamento: {benchmark_data['total_time']:.2f}ms")
    print(f"Tempo médio por movimento: {benchmark_data['avg_time_per_move']:.2f}ms")
    print(f"Total de nós expandidos: {benchmark_data['total_nodes']}")
    print(f"Média de nós por movimento: {benchmark_data['avg_nodes_per_move']:.2f}")
    print(f"Tempo total do jogo: {total_game_time:.2f} segundos")
    print("================================\n")
    
    # Salvar resultados em CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"benchmark_{algoritmo}_{dificuldade}_{timestamp}.csv"
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Métrica", "Valor"])
        for key, value in benchmark_data.items():
            if key != "individual_move_times":
                writer.writerow([key, value])
        writer.writerow(["tempo_total_jogo_segundos", total_game_time])
        writer.writerow([])
        writer.writerow(["Movimento", "Tempo (ms)"])
        for i, t in enumerate(move_times, 1):
            writer.writerow([f"Movimento {i}", f"{t:.2f}"])
    
    print(f"Resultados salvos em {filename}")
    return benchmark_data

# O resto do código (run_all_benchmarks e main) permanece o mesmo

def run_all_benchmarks(num_movimentos=30):
    """Executa benchmarks para todas as combinações de algoritmos e dificuldades"""
    algoritmos = ["mcts", "minimax", "alphabeta"]
    dificuldades = ["facil", "medio", "dificil"]
    
    resultados = []
    
    for algoritmo in algoritmos:
        for dificuldade in dificuldades:
            print(f"\n\nExecutando benchmark para {algoritmo.upper()} - {dificuldade.upper()}")
            resultado = run_benchmark_game(algoritmo, dificuldade, num_movimentos)
            resultados.append({
                "algoritmo": algoritmo,
                "dificuldade": dificuldade,
                **resultado
            })
            
            # Pequeno delay entre benchmarks
            time.sleep(2)
    
    # Salvar resultados comparativos
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"comparacao_benchmarks_{timestamp}.csv"
    
    with open(filename, 'w', newline='') as f:
        campos = ["algoritmo", "dificuldade", "total_nodes", "total_time", 
                 "moves_completed", "avg_time_per_move", "avg_nodes_per_move"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for resultado in resultados:
            writer.writerow({campo: resultado.get(campo, "") for campo in campos})
    
    print(f"\nComparação de todos os benchmarks salva em {filename}")
    
    return resultados

if __name__ == "__main__":
    print("Ferramenta de Benchmark do Dameo")
    print("1. Executar benchmark individual")
    print("2. Executar todos os benchmarks")
    
    opcao = input("Escolha uma opção (1-2): ")
    
    if opcao == "1":
        algoritmos = {"1": "mcts", "2": "minimax", "3": "alphabeta"}
        dificuldades = {"1": "facil", "2": "medio", "3": "dificil"}
        
        print("\nEscolha o algoritmo:")
        print("1. MCTS")
        print("2. Minimax")
        print("3. Alpha-Beta")
        alg_opcao = input("Opção (1-3): ")
        
        print("\nEscolha a dificuldade:")
        print("1. Fácil")
        print("2. Médio")
        print("3. Difícil")
        dif_opcao = input("Opção (1-3): ")
        
        num_movimentos = int(input("\nNúmero de movimentos para o benchmark (recomendado: 30): "))
        
        algoritmo = algoritmos.get(alg_opcao, "mcts")
        dificuldade = dificuldades.get(dif_opcao, "medio")
        
        run_benchmark_game(algoritmo, dificuldade, num_movimentos)
        
    elif opcao == "2":
        num_movimentos = int(input("\nNúmero de movimentos para cada benchmark (recomendado: 30): "))
        run_all_benchmarks(num_movimentos)
        
    else:
        print("Opção inválida!")

   
