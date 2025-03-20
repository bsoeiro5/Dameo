import pygame

class DameoBoard:
    def __init__(self, size=6, cell_size=80):
        pygame.init()
        self.size = size
        self.cell_size = cell_size
        self.width = self.height = size * cell_size + 40  # Adicionando bordas
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dameo Board")
        self.colors = [(200, 200, 200), (100, 100, 100)]  # Cores alternadas
        self.running = True
    
    def draw_board(self):
        self.screen.fill((50, 50, 50))  # Fundo escuro
        for row in range(self.size):
            for col in range(self.size):
                x = col * self.cell_size + 20  # Ajuste para borda
                y = row * self.cell_size + 20
                color = self.colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (0, 0, 0), (x, y, self.cell_size, self.cell_size), 2)  # Bordas das células
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.draw_board()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = DameoBoard()
    game.run()

