import time
import csv
import os
from datetime import datetime

class GameMetrics:
    def __init__(self):
        self.reset()
        self.metrics_file = f"dameo_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self._initialize_file()
        
    def reset(self):
        # Métricas gerais
        self.game_id = 0
        self.algorithm = ""
        self.difficulty = ""
        self.execution_time = 0
        self.start_time = 0
        self.nodes_expanded = 0
        self.simulations_run = 0  # Específico para MCTS
        self.evaluation_score = 0
        self.moves_considered = 0
        self.depth = 0
        
        # Contadores de peças
        self.green_pieces_start = 0
        self.orange_pieces_start = 0
        self.green_pieces_end = 0
        self.orange_pieces_end = 0
        
    def _initialize_file(self):
        # Cria o arquivo CSV se ele não existir
        header = [
            "game_id", "algorithm", "difficulty", "move_number", 
            "execution_time_ms", "nodes_expanded", "simulations_run",
            "evaluation_score", "moves_considered", "depth",
            "green_pieces", "orange_pieces", "total_game_time"
        ]
        
        if not os.path.exists(self.metrics_file):
            with open(self.metrics_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                
    def start_move_timer(self):
        self.start_time = time.time()
        
    def stop_move_timer(self):
        self.execution_time = (time.time() - self.start_time) * 1000  # Convert to milliseconds
        
    def record_move_metrics(self, move_number, total_game_time=0):
        with open(self.metrics_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.game_id,
                self.algorithm,
                self.difficulty,
                move_number,
                round(self.execution_time, 2),
                self.nodes_expanded,
                self.simulations_run,
                self.evaluation_score,
                self.moves_considered,
                self.depth,
                self.green_pieces_end,
                self.orange_pieces_end,
                round(total_game_time, 2)
            ])
            
    def set_algorithm_info(self, algorithm, difficulty, depth=0):
        self.algorithm = algorithm
        self.difficulty = difficulty
        self.depth = depth
        
    def update_piece_count(self, green_pieces, orange_pieces):
        self.green_pieces_end = green_pieces
        self.orange_pieces_end = orange_pieces
        
    def print_move_summary(self, move_number):
        print(f"\n--- Métricas do Movimento {move_number} ---")
        print(f"Algoritmo: {self.algorithm} (Dificuldade: {self.difficulty})")
        print(f"Tempo de execução: {self.execution_time:.2f} ms")
        print(f"Nós expandidos: {self.nodes_expanded}")
        if self.algorithm.lower() == "mcts":
            print(f"Simulações executadas: {self.simulations_run}")
        print(f"Avaliação final: {self.evaluation_score}")
        print(f"Peças verdes: {self.green_pieces_end}")
        print(f"Peças laranjas: {self.orange_pieces_end}")
        print("--------------------------------\n")

# Instância global para uso em todo o jogo
metrics = GameMetrics()
