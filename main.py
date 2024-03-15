import pygame 
import random
class SandBox:
    def __init__(self):
        self.width = 800
        self.height = 1000
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.sand = 5
        self.fps = 60
        self.row = self.height // self.sand
        self.col = self.width // self.sand
        self.grid = {}
        self.gravity = 3
        self.partical_size = 8
    
    def withinRow(self, value):
        return 0 <= value < self.row

    def withinCol(self, value):
        return 0 <= value < self.col
    
    def color(self):
        return (random.choice(range(255)), random.choice(range(255)), random.choice(range(255)))

    def pos(self, col, row):
        return f"{col};{row}"

    def update(self, clear):
        nextGrid = {}

        for col in range(self.col):
            for row in range(self.row): 
                if self.pos(col, row) in self.grid:
                    #continue
                    below_left = self.pos(col-1, row+1) not in self.grid and self.withinCol(col-1) and self.withinRow(row+1)
                    below_right = self.pos(col+1, row+1) not in self.grid and self.withinCol(col+1) and self.withinRow(row+1)
                    
                    if clear:
                        nextGrid[self.pos(col, row)] = self.grid[self.pos(col, row)]

                    elif self.pos(col, row+self.gravity) not in self.grid and self.withinCol(col) and self.withinRow(row+self.gravity):
                        nextGrid[self.pos(col, row+self.gravity)] = self.grid[self.pos(col, row)]

                    elif self.pos(col, row+1) not in self.grid and self.withinCol(col) and self.withinRow(row+1):
                        nextGrid[self.pos(col, row+1)] = self.grid[self.pos(col, row)]

                    elif below_left and below_right:
                        side = random.choice([1, -1])
                        nextGrid[self.pos(col+side, row+1)] = self.grid[self.pos(col, row)]

                    elif below_left:
                        nextGrid[self.pos(col-1, row+1)] = self.grid[self.pos(col, row)]

                    elif below_right:
                        nextGrid[self.pos(col+1, row+1)] = self.grid[self.pos(col, row)]

                    else:
                        nextGrid[self.pos(col, row)] = self.grid[self.pos(col, row)]

        self.grid = nextGrid

    def particals(self, x, y, color):
        bounding_box = self.partical_size // 2
        for col in range(-bounding_box, bounding_box+1):
            for row in range(-bounding_box, bounding_box+1):
                    if self.withinCol(x+col) and self.withinRow(y+row):
                        if color:
                            self.grid[self.pos(x+col, y+row)] = color

                        elif self.pos(x+col, y+row) in self.grid: 
                            del self.grid[self.pos(x+col, y+row)]

    def render(self):
        for key, value in self.grid.items():
            pos = tuple(map(int, key.split(";")))
            pygame.draw.rect(self.screen, value, (pos[0]*self.sand, pos[1]*self.sand, self.sand, self.sand), 0)
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()

        hover = False
        clear = False
        color = (0, 0, 0)

        while True:
            self.screen.fill((0, 0, 0))
            self.render()
            self.update(clear)
            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                buttons = pygame.mouse.get_pressed()
                if hover:
                    x, y = pygame.mouse.get_pos()
                    self.particals(x//self.sand, y//self.sand, color)

                if clear:
                    x, y = pygame.mouse.get_pos()
                    self.particals(x//self.sand, y//self.sand, None)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons[0]:
                        color = self.color()
                        hover = True
                        
                    if buttons[2]:
                        clear = True
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    hover = False
                    clear = False
            clock.tick(self.fps)


if __name__ == "__main__":
    SandBox().run()
