import pygame

WALL    = (30, 35, 36)      
GROUND  = (205, 206, 210)  
START   = (52, 152, 219)    
GOAL    = (231, 76, 60)     
VISITED = (46, 204, 113)    
SOL     = (255, 190, 60)    

pygame.init()
clock = pygame.time.Clock()

class Grid:
    def __init__(self, width, height, screen_size):
        self.board_width= width
        self.board_height= height
        self.cells= [[0 for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.screen_size = screen_size
        self.cell_size = self.screen_size / self.board_width
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        self.goal= (-1,-1)
        self.start= (-1,-1)

    def clearGrid(self):
        for x in range(self.board_width):
            for y in range(self.board_height):
                if self.cells[y][x]!=0:
                    self.cells[y][x]=1

    def draw(self):
        for r in range(self.board_width):
            for c in range(self.board_height):
                if self.goal== (r,c):
                    color= GOAL
                elif self.start== (r,c):
                    color=START
                elif self.cells[c][r]==0:
                    color=WALL
                elif self.cells[c][r]==1:
                    color = GROUND
                elif self.cells[c][r]==2:
                    color= VISITED
                elif self.cells[c][r]==3:
                    color= SOL
                else:
                    color= (255*self.cells[c][r],255*self.cells[c][r] ,255*self.cells[c][r])
                rect = pygame.Rect(r * self.cell_size, c * self.cell_size, self.cell_size + 1, self.cell_size + 1)
                pygame.draw.rect(self.screen, color, rect)

    def update(self, fps):
        self.draw()
        pygame.display.flip()
        clock.tick(fps)
