import pygame
import random
import math
from Grid import Grid, clock

'''
Blue is the start.
Rigth click to set the goal.
Left click to change walls and tiles.

'''
WIDTH = 60
HEIGHT = 60
SCREEN_SIZE = 800

class Maze(Grid):

    def __init__(self, width, height, screen_size):
        super().__init__(width, height, screen_size)
        self.generate_maze_prim()

    def generate_maze_prim(self):
        start_row = random.randrange(0, self.board_height, 2)
        start_col = random.randrange(0, self.board_width, 2)
        self.cells[start_row][start_col] = 1
        self.start=(start_row,start_col)

        frontier = []
        def add_frontier(r, c):
            #2 steps away to skip wall cell
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.board_height and 0 <= nc < self.board_width:
                    if self.cells[nr][nc] == 0:
                        frontier.append((nr, nc, r, c))

        add_frontier(start_row, start_col)

        while frontier:
            idx = random.randrange(len(frontier))
            nr, nc, pr, pc = frontier.pop(idx)

            if self.cells[nr][nc] == 0:
                self.cells[nr][nc] = 1

                wall_r = (pr + nr) // 2
                wall_c = (pc + nc) // 2
                self.cells[wall_r][wall_c] = 1
                add_frontier(nr, nc)

                if(not self.board_width+self.board_height>120):
                    self.update(200)

        
        #Delete some walls to spice things ups
        for row in range(self.board_height):
            for col in range(self.board_width):
                if self.cells[row][col] == 0:
                    wall_count = 0
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < self.board_height and 0 <= nc < self.board_width:
                            if self.cells[nr][nc] == 0:
                                wall_count += 1

                    if wall_count == 2:
                        if random.random() < 0.025:
                            self.cells[row][col] = 1

        self.update(100)
        clock.tick(24)

    def nextPosibles(self, x,y):
        l=[]
        for i,j in [(0,-1),(-1,0),(0,1),(1,0)]:
            if(0<=y+j<self.board_height and 0<=x+i<self.board_width and self.cells[y+j][x+i]==1):
                l.append((x+i,y+j,x,y))
        return l

    def orderBasedDistance(self, visit, distances, toadd):
        goalx, goaly = self.goal
        for pos in toadd:
            x, y, a, b= pos
            dist = math.sqrt((x - goalx)**2 + (y - goaly)**2)
            low, high= 0, len(distances)
            while low < high:
                mid= (low + high) // 2
                if distances[mid] < dist:
                    low= mid + 1
                else:
                    high= mid

            distances.insert(low, dist)
            visit.insert(low, pos)
        return visit, distances

    def BFS(self):
        while(self.goal== (-1,-1)):
            self.events(True)
            continue

        x,y=self.start
        visit= []
        visit.extend(self.nextPosibles(x,y))
        mappedPrev= {}
        while visit:
            x,y,prevx,prevy= visit.pop(0)
            mappedPrev[(x,y)]=(prevx,prevy)
            if(self.goal == (x,y)):
                break
            self.cells[y][x]=2
            visit.extend(self.nextPosibles(x,y))

            self.update(200)
        
        while True:
            x,y= mappedPrev[x,y]
            if (x,y)== self.start:
                break
            self.cells[y][x]=3
            self.update(40)
        
        while self.events(True):
            continue
        
    def DFS(self):
        while(self.goal== (-1,-1)):
            self.events(True)
            continue

        x,y=self.start
        visit= []
        visit.extend(self.nextPosibles(x,y))
        mappedPrev= {}
        while visit:
            x,y,prevx,prevy= visit.pop()
            mappedPrev[(x,y)]=(prevx,prevy)
            if(self.goal == (x,y)):
                break
            self.cells[y][x]=2
            visit.extend(self.nextPosibles(x,y))

            self.update(200)
        
        while True:
            x,y= mappedPrev[x,y]
            if (x,y)== self.start:
                break
            self.cells[y][x]=3
            self.update(40)
        
        while self.events(True):
            continue

    def Astar(self):
        while(self.goal== (-1,-1)):
            self.events(True)
            continue
        
        x,y=self.start
        self.cells[y][x]=2
        visit,distances= self.orderBasedDistance([],[],self.nextPosibles(x,y))
        mappedPrev={}
        while visit:
            x,y,prevx,prevy= visit.pop(0)
            distances.pop(0)
            mappedPrev[(x,y)]=(prevx,prevy)
            if(self.goal == (x,y)):
                break
            self.cells[y][x]=2
            l= self.nextPosibles(x,y)
            visit,distances= self.orderBasedDistance(visit, distances,l)

            self.update(200)
            
        while True:
            x,y= mappedPrev[x,y]
            if (x,y)== self.start:
                break
            self.cells[y][x]=3
            self.update(40)
        
        while self.events(True):
            continue

    def events(self, paused):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                paused = not paused
                print("Paused" if paused else "Running")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                x = int(mouse_pos[0] / self.cell_size)
                y = int(mouse_pos[1] / self.cell_size)
                if(self.goal == (x,y)): 
                    self.goal= (-1,-1)
                elif (0 <= x < self.board_width) and (0 <= y < self.board_height) and not self.cells[y][x]==0:
                    self.goal = (x, y)
                pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                clock.tick(12)
                mouse_pos = pygame.mouse.get_pos()
                x= int(mouse_pos[0] / self.cell_size)
                y= int(mouse_pos[1] / self.cell_size)
                if (0 <= x < self.board_width) and (0 <= y < self.board_height):
                    self.cells[y][x] = (self.cells[y][x] +1) % 2
                pygame.display.update()
        return paused


board = Maze(WIDTH, HEIGHT, SCREEN_SIZE)
board.BFS()
board.clearGrid()
board.DFS()
board.clearGrid()
board.Astar()
