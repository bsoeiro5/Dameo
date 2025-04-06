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
    if not all(key in configuracoes for key in ["modo", "tamanho"]):
        print("Erro: Configurações incompletas")
        return
    
    # Configurar parâmetros baseado na dificuldade e algoritmo
    dificuldade = configuracoes.get("dificuldade")
    algoritmo = configuracoes.get("algoritmo")
    
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
    
    depth = 0
    if algoritmo in ["minimax", "alphabeta"]:
        from minimax.algoritmo import minimax, alfa_beta
        if dificuldade == "facil":
            depth = 2
        elif dificuldade == "medio":
            depth = 4
        else:  # difícil
            depth = 6
            
        print(f"{algoritmo.upper()} configurado: {dificuldade} - profundidade {depth}")
    
    # Random AI não precisa de configuração adicional
    if algoritmo == "random":
        print("IA Random configurada")

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        
        if game.verificar_fim_do_jogo():
            pygame.time.delay(3000)
            run = False
            break

        # Turno da IA
        if ((configuracoes["modo"] == "pvc" and game.turn == LARANJA) or 
            (configuracoes["modo"] == "cvc")) and not ai_thinking:
            ai_thinking = True
            print(f"IA pensando... (algoritmo: {algoritmo}, dificuldade: {dificuldade})")
            
            if algoritmo == "mcts":
                move, is_capture = ai.get_move(game)
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
          

            elif algoritmo == "random":
                # Implementação do algoritmo Random com prioridade para capturas
                moves = get_valid_moves(game)
                if moves:
                    # Separar movimentos com e sem captura
                    capture_moves = [move for move in moves if move[2]]  # move[2] é o parâmetro 'skip' que indica captura
                    
                    if capture_moves:
                        # Se existem capturas, escolhe aleatoriamente entre elas
                        peca, novo_pos, skip = random.choice(capture_moves)
                        print("Random AI fez um movimento de captura")
                    else:
                        # Se não existem capturas, escolhe aleatoriamente entre os movimentos normais
                        peca, novo_pos, skip = random.choice(moves)
                        print("Random AI fez um movimento normal (sem captura)")
                    
                    # Executa o movimento escolhido
                    game.tabuleiro.movimento(peca, novo_pos[0], novo_pos[1])
                    if skip:
                        game.tabuleiro.remove(skip)
                        new_piece = game.tabuleiro.get_peça(novo_pos[0], novo_pos[1])
                        # Verificar se há mais capturas possíveis
                        more_captures = any(skip for _, skip in game.tabuleiro.get_valid_moves(new_piece).items())
                        if not more_captures:
                            game.change_turn()
                    else:
                        game.change_turn()
                else:
                    game.change_turn()
                    print("Random AI não encontrou movimentos válidos")
            else:
                # Usar minimax ou alpha-beta
                try:
                    print(f"\nIniciando {algoritmo}...")
                    print(f"Estado atual do tabuleiro antes da IA:")
                    print(f"Peças verdes: {game.tabuleiro.verdes_left}")
                    print(f"Peças laranjas: {game.tabuleiro.laranjas_left}")
                    
                    if algoritmo == "minimax":
                        score, best_board = minimax(game.tabuleiro, depth, False, game)
                        print(f"Minimax retornou score: {score}")
                    
                        if best_board:
                            print("Tabuleiro válido retornado, aplicando movimento...")
                            # Verificar estado antes do movimento
                            old_orange = game.tabuleiro.laranjas_left
                            game.ai_move(best_board)
                            # Verificar estado após o movimento
                            new_orange = game.tabuleiro.laranjas_left
                            print(f"Peças laranjas antes: {old_orange}, depois: {new_orange}")
                        else:
                            print("IA não encontrou movimentos válidos!")
                            game.change_turn()
                    elif algoritmo == "alphabeta":
                        score, best_board = alfa_beta(game.tabuleiro, depth, float('-inf'), float('inf'), False, game)
                        print(f"Alpha-beta retornou score: {score}")
                    
                        if best_board:
                            print("Tabuleiro válido retornado, aplicando movimento...")
                            # Verificar estado antes do movimento
                            old_orange = game.tabuleiro.laranjas_left
                            game.ai_move(best_board)
                            # Verificar estado após o movimento
                            new_orange = game.tabuleiro.laranjas_left
                            print(f"Peças laranjas antes: {old_orange}, depois: {new_orange}")
                        else:
                            print("IA não encontrou movimentos válidos!")
                            game.change_turn()
                except Exception as e:
                    print(f"Erro ao executar {algoritmo}: {e}")
                    import traceback
                    traceback.print_exc()
                    game.change_turn()
            
            ai_thinking = False
            continue

        # Processar eventos do jogador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Retornar ao menu principal e iniciar novo jogo com novas configurações
                    new_config = menu_principal()
                    if new_config:
                        pygame.quit()
                        return new_config  # Retorna as novas configurações
                    else:
                        pygame.quit()
                        return None

            if event.type == pygame.MOUSEBUTTONDOWN and \
               (configuracoes["modo"] == "pvp" or (configuracoes["modo"] == "pvc" and game.turn == VERDE)):
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // TAMANHO_QUADRADO, pos[0] // TAMANHO_QUADRADO
                game.select(row, col)

        game.update(WIN)

    return menu_principal()  # Quando o jogo termina, retorna ao menu principal

if __name__ == "__main__":
    configuracoes = menu_principal()
    while configuracoes:  # Loop principal que permite reiniciar o jogo
        configuracoes = jogo_principal(configuracoes)
    pygame.quit()
