import pygame




class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[' '] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 20

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                x = self.left + i * self.cell_size
                y = self.top + j * self.cell_size
                if self.board[j][i] != '#':
                    pygame.draw.rect(screen, 'black', (x, y, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(screen, 'white', (x, y, self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top) // self.cell_size
        if (x < 0 or x > self.width - 1) or (y < 0 or y > self.height - 1):
            return None
        else:
            return (x, y)

    def on_click(self, cell_coords, bt):
        if cell_coords:
            a = self.board[cell_coords[1]][cell_coords[0]]
            if a == ' ' and bt == 1:
                self.board[cell_coords[1]][cell_coords[0]] = '#'
            elif a == '#' and bt == 3:
                self.board[cell_coords[1]][cell_coords[0]] = ' '


    def get_click(self, mouse_pos, bt):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, bt)


    def table(self):
        file = open("map_add.txt", "w")
        for i in self.board:
            file.write(''.join(i) + '\n')


press = False
# Столб строка
col, row = 19, 22
board = Board(col, row)

pygame.init()
pygame.display.set_caption('Реакция на события от мыши')
screen = pygame.display.set_mode((20 + col * 20, 20 + row * 20))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            board.table()
            running = False
        press = False
        if pygame.mouse.get_pressed()[0]:
            press = True
            board.get_click(pygame.mouse.get_pos(), 1)
        if pygame.mouse.get_pressed()[2]:
            press = True
            board.get_click(pygame.mouse.get_pos(), 3)



    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()
pygame.display.flip()
pygame.quit()