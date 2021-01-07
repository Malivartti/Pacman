import os

import pygame

w, h = 19, 22
cell = 30
size = w * cell, h * cell
pygame.init()
pygame.display.set_caption('Pacman')

screen = pygame.display.set_mode(size)
grid = [pygame.Rect(x * cell, y * cell, cell, cell) for x in range(w) for y in range(h)]

borders = pygame.sprite.Group()
point = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
row, col = 9 * cell, 16 * cell

animCount = 0
course, course_t = 'left', None

speed = 5


def load_image(x, y, x2, y2, colorkey=-1):
    image = pygame.image.load(os.path.join('data', 'pac.png'))
    cropped = pygame.Surface((x2 - x, y2 - y))
    cropped.blit(image, (0, 0), (x, y, x2, y2))

    image = cropped.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image = pygame.transform.scale(image, (cell - 2, cell - 2))
    return image


def Enemies_walk():
    global walk_BLINKY, walk_PINKY, walk_INKY, walk_CLYDE
    x, y = 470, 0
    for _ in range(6):
        walk_BLINKY.append(load_image(x, y, x + 140, y + 140))
        x += 170
    x, y = 50, 160
    for i in range(4):
        for j in range(8):
            if i == 0 and j in [0, 1]:
                walk_BLINKY.append(load_image(x, y, x + 140, y + 140))
            elif i == 0 and j in [2, 3, 4, 5, 6, 7] or i == 1 and j in [0, 1]:
                walk_INKY.append(load_image(x, y, x + 140, y + 140))
            elif (i == 1 and j in [2, 3, 4, 5, 6, 7]) or (i == 2 and j in [0, 1]):
                walk_CLYDE.append(load_image(x, y, x + 140, y + 140))
            elif (i == 2 and j in [2, 3, 4, 5, 6, 7]) or (i == 3 and j in [0, 1]):
                walk_PINKY.append(load_image(x, y, x + 140, y + 140))
            x += 170
        x = 50
        y += 160
    walk_BLINKY = [[walk_BLINKY[0], walk_BLINKY[1]], [walk_BLINKY[2], walk_BLINKY[3]],
                   [walk_BLINKY[4], walk_BLINKY[5]], [walk_BLINKY[6], walk_BLINKY[7]]]
    walk_PINKY = [[walk_PINKY[0], walk_PINKY[1]], [walk_PINKY[2], walk_PINKY[3]],
                  [walk_PINKY[4], walk_PINKY[5]], [walk_PINKY[6], walk_PINKY[7]]]
    walk_INKY = [[walk_INKY[0], walk_INKY[1]], [walk_INKY[2], walk_INKY[3]],
                 [walk_INKY[4], walk_INKY[5]], [walk_INKY[6], walk_INKY[7]]]
    walk_CLYDE = [[walk_CLYDE[0], walk_CLYDE[1]], [walk_CLYDE[2], walk_CLYDE[3]],
                  [walk_CLYDE[4], walk_CLYDE[5]], [walk_CLYDE[6], walk_CLYDE[7]]]


walk = [load_image(30, 10, 160, 140), load_image(190, 10, 310, 140),
        load_image(330, 10, 460, 140), load_image(190, 10, 310, 140)]

walk_BLINKY = []
walk_PINKY = []
walk_INKY = []
walk_CLYDE = []
wall_charged = [[load_image(390, 640, 530, 780), load_image(560, 640, 700, 780)],
                [load_image(730, 640, 870, 780), load_image(900, 640, 1040, 780)]]
Enemies_walk()


class Border(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        x, y = x * cell, y * cell
        self.add(borders)
        self.image = pygame.Surface([cell, cell])
        self.rect = pygame.Rect(x, y, cell, cell)
        self.image.fill('blue')


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(point)
        self.image = pygame.Surface([5, 5])
        self.rect = pygame.Rect(x * cell + 12, y * cell + 12, 5, 5)
        self.image.fill('white')


def Map(filename):
    lis = []
    file = [line.rstrip() for line in open(filename)]
    for row, i in enumerate(file):
        for col, j in enumerate(i):
            if j == '#':
                Border(col, row)
                lis.append(pygame.Rect(col * cell, row * cell, cell, cell))
            if j == ' ':
                Point(col, row)
    return lis


map = Map('map.txt')


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = pygame.Surface((cell, cell))
        self.rect = pygame.Rect(x, y, cell, cell)

    def move(self, xvel, yvel):
        global course
        collideList = map
        self.rect.x += xvel
        for block in collideList:
            if self.rect.colliderect(block):
                if xvel < 0:
                    self.rect.left = block.right
                elif xvel > 0:
                    self.rect.right = block.left
                break
        ################################################
        self.rect.y += yvel
        for block in collideList:
            if self.rect.colliderect(block):
                if yvel < 0:
                    self.rect.top = block.bottom
                elif yvel > 0:
                    self.rect.bottom = block.top
                break
        # Прохож на другую сторону
        if -cell >= self.rect.x or self.rect.x >= size[0]:
            self.rect.x = abs(self.rect.x + 30 - size[0] if -cell >= self.rect.x
                              else self.rect.x - size[0]) - 30

    def update(self):
        self.animation()
        if course == 'left':
            self.move(-speed, 0)
        elif course == 'right':
            self.move(speed, 0)
        elif course == 'up':
            self.move(0, -speed)
        elif course == 'down':
            self.move(0, speed)

        if pygame.sprite.spritecollide(player, point, True):  # Точки
            print('*')

    def animation(self):
        global animCount, course
        self.image.fill('black')
        if animCount + 1 >= 20:
            animCount = 0
        if course == 'left':
            walk_L = [pygame.transform.rotate(i, 180) for i in walk]
            self.image.blit(walk_L[animCount // 5], (0, 0))
            animCount += 1
        elif course == 'right':
            self.image.blit(walk[animCount // 5], (0, 0))
            animCount += 1
        elif course == 'up':
            walk_UP = [pygame.transform.rotate(i, 90) for i in walk]
            self.image.blit(walk_UP[animCount // 5], (0, 0))
            animCount += 1
        elif course == 'down':
            walk_DOWN = [pygame.transform.rotate(i, -90) for i in walk]
            self.image.blit(walk_DOWN[animCount // 5], (0, 0))
            animCount += 1


class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y, anim):
        super().__init__(all_sprites)
        self.add(enemies)

        self.anim = anim
        self.image = pygame.Surface((cell, cell))
        self.rect = pygame.Rect(x * cell, y * cell, cell, cell)

        self.states()

    def states(self):
        self.animCount = 0
        self.course = 'down'

    def update(self):
        self.animation()

    def animation(self):
        global animCountE
        self.image.fill('black')
        if self.animCount + 1 >= 10:
            self.animCount = 0
        if self.course == 'left':
            self.image.blit(self.anim[3][self.animCount // 5], (0, 0))
            self.animCount += 1
        elif self.course == 'right':
            self.image.blit(self.anim[0][self.animCount // 5], (0, 0))
            self.animCount += 1
        elif self.course == 'up':
            self.image.blit(self.anim[2][self.animCount // 5], (0, 0))
            self.animCount += 1
        elif self.course == 'down':
            self.image.blit(self.anim[1][self.animCount // 5], (0, 0))
            self.animCount += 1


Blinky = Enemies(9, 8, walk_BLINKY)
Pinky = Enemies(8, 10, walk_PINKY)
Inky = Enemies(9, 10, walk_INKY)
Clyde = Enemies(10, 10, walk_CLYDE)
player = Player(row, col)

print(walk_CLYDE)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                course = 'left'
            elif event.key == pygame.K_RIGHT:
                course = 'right'
            elif event.key == pygame.K_UP:
                course = 'up'
            elif event.key == pygame.K_DOWN:
                course = 'down'

    # Сетка
    screen.fill(pygame.Color("black"))
    [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # Клетки
    all_sprites.draw(screen)
    all_sprites.update()

    clock.tick(30)
    pygame.display.flip()
pygame.quit()
