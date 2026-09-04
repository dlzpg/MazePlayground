import pygame
from Grid import Grid, clock

WIDTH = 50
HEIGHT = 50
SCREEN_SIZE = 800

LINE_COLOR = (0, 0, 0)
ON_COLOR = (255, 255, 255)
OFF_COLOR = (30, 30, 30)


class GameOfLife(Grid):

    def draw(self):
        for r in range(self.board_width):
            for c in range(self.board_height):
                color = ON_COLOR if self.cells[c][r] else OFF_COLOR
                rect = pygame.Rect(r * self.cell_size, c * self.cell_size, self.cell_size, self.cell_size)
                outline_width = round(max(1, self.cell_size * 0.05))
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, LINE_COLOR, rect, outline_width)

    def count_neighbors_alive(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_x = (x + j) % self.board_width
                neighbor_y = (y + i) % self.board_height
                count += self.cells[neighbor_y][neighbor_x]
        return count
    
    def next_gen(self):
        new_cells = [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        for r in range(self.board_width):
            for c in range(self.board_height):
                alive_neighbors = self.count_neighbors_alive(r, c)
                if self.cells[c][r] == 1:
                    if alive_neighbors < 2:
                        new_cells[c][r] = 0
                    elif 2 <= alive_neighbors <= 3:
                        new_cells[c][r] = self.cells[c][r]
                    elif alive_neighbors > 3:
                        new_cells[c][r] = 0
                elif self.cells[c][r] == 0:
                    if alive_neighbors == 3:
                        new_cells[c][r] = 1
        self.cells = new_cells

board = GameOfLife(WIDTH, HEIGHT, SCREEN_SIZE)
running = True
paused = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused
            print("Paused" if paused else "Running")
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            x= int(mouse_pos[0] / board.cell_size)
            y= int(mouse_pos[1] / board.cell_size)
            if (0 <= x < board.board_width) and (0 <= y < board.board_height):
                board.cells[y][x] = (board.cells[y][x] +1) % 2
            pygame.display.update()

    if not paused:
        board.next_gen()
    board.update(20)
pygame.quit()
