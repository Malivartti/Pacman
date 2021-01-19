import os
import sqlite3
from random import choice
from time import sleep
import pygame


def load_image(x, y, x2, y2, file='pac.png', colorkey=-1):
    image = pygame.image.load(os.path.join('data', file))
    cropped = pygame.Surface((x2 - x, y2 - y))
    cropped.blit(image, (0, 0), (x, y, x2, y2))

    image = cropped.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    image = pygame.transform.scale(image, (CELL, CELL))
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
    x, y = 5, 445
    for i2 in range(2):
        for j2 in range(8):
            if i2 == 0 or (i2 == 1 and j2 in [0, 1, 2, 3]):
                death_pacman.append(load_image(x, y, x + 55, y + 65, 'death_pac.png'))
            x += 70
        x = 5
        y += 65

    walk_BLINKY = [[walk_BLINKY[0], walk_BLINKY[1]], [walk_BLINKY[2], walk_BLINKY[3]],
                   [walk_BLINKY[4], walk_BLINKY[5]], [walk_BLINKY[6], walk_BLINKY[7]]]
    walk_PINKY = [[walk_PINKY[0], walk_PINKY[1]], [walk_PINKY[2], walk_PINKY[3]],
                  [walk_PINKY[4], walk_PINKY[5]], [walk_PINKY[6], walk_PINKY[7]]]
    walk_INKY = [[walk_INKY[0], walk_INKY[1]], [walk_INKY[2], walk_INKY[3]],
                 [walk_INKY[4], walk_INKY[5]], [walk_INKY[6], walk_INKY[7]]]
    walk_CLYDE = [[walk_CLYDE[0], walk_CLYDE[1]], [walk_CLYDE[2], walk_CLYDE[3]],
                  [walk_CLYDE[4], walk_CLYDE[5]], [walk_CLYDE[6], walk_CLYDE[7]]]


def Board(filename):
    lis = []
    file = [line.rstrip() for line in open(filename)]
    for row, i in enumerate(file):
        for col, j in enumerate(i):
            if j == '#':
                Obstacle(col, row)
                lis.append(pygame.Rect(col * CELL, row * CELL, CELL, CELL))
            elif j == ' ':
                Point(col, row)
            elif j == '*':
                Energy_Point(col, row)
    return lis


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(borders)
        self.image = pygame.Surface([CELL, CELL])
        self.rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
        self.image.fill('blue')


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(point)
        self.image = pygame.Surface([5, 5])
        self.rect = pygame.Rect(x * CELL + 12, y * CELL + 12, 5, 5)
        self.image.fill('white')


class Energy_Point(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(energy_point)
        self.radius = 2
        self.v = 0.5
        self.image = pygame.Surface((CELL, CELL))
        self.rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)
        self.image.fill('black')

    def update(self):
        self.image.fill('black')
        self.radius += self.v
        if self.radius > 8 or self.radius < 2:
            self.v *= -1
        pygame.draw.circle(self.image, pygame.Color("white"),
                           (CELL / 2, CELL / 2), self.radius)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.add(player_g)
        self.image = pygame.Surface((CELL, CELL))
        self.rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)

        self.animCount = 0
        self.animCountdeath = 0
        self.speed = 5
        self.energy = False
        self.time_energy = 0
        self.end = False
        self.time_end = 0
        self.points = 0

    def moveX(self, xvel):
        """Движение игрока по горизонтали"""
        global course, course_t
        collideList = map
        self.rect.x += xvel
        flag = True
        for block in collideList:
            if self.rect.colliderect(block):
                if xvel < 0:
                    self.rect.left = block.right
                elif xvel > 0:
                    self.rect.right = block.left
                flag = False
                break
        if flag:
            if course_t == 'left' or course_t == 'right':
                course = course_t
                course_t = None

        if -CELL >= self.rect.x or self.rect.x >= size[0]:
            self.rect.x = abs(self.rect.x + 30 - size[0] if -CELL >= self.rect.x
                              else self.rect.x - size[0]) - 30

    def moveY(self, yvel):
        """Движение игрока по вертикали"""
        global course, course_t
        collideList = map
        self.rect.y += yvel
        flag = True
        # Запрет на вход в клетку призраков
        if self.rect.colliderect(pygame.Rect(9 * CELL, 9 * CELL, CELL, CELL)):
            self.rect.bottom = pygame.Rect(9 * CELL, 9 * CELL, CELL, CELL).top
            flag = False

        for block in collideList:
            if self.rect.colliderect(block):
                if yvel < 0:
                    self.rect.top = block.bottom
                elif yvel > 0:
                    self.rect.bottom = block.top
                flag = False
                break
        if flag:
            if course_t == 'up' and yvel < 0 or course_t == 'down' and yvel > 0:
                course = course_t
                course_t = None

    def update(self):
        global all_results, new_start
        self.animation()
        if self.energy:
            self.time_energy -= 0.1
            if self.time_energy <= 0:
                self.energy = False
        if len(point) == 0 and len(energy_point) == 0:
            all_results += self.number_of_points()
            new_start = False
            Start_game()
        if course_t == 'left' or course == 'left':
            self.moveX(-self.speed)
        if course_t == 'right' or course == 'right':
            self.moveX(self.speed)
        if course_t == 'up' or course == 'up':
            self.moveY(-self.speed)
        if course_t == 'down' or course == 'down':
            self.moveY(self.speed)

        # Взаимодействие
        if pygame.sprite.spritecollide(player, point, True):  # Точки
            self.points += 10
        if pygame.sprite.spritecollide(player, energy_point, True):  # Точки
            self.points += 50
            self.energy = True
            self.time_energy = 30
        if pygame.sprite.spritecollide(player, ghosts, False) and not self.energy:  # Пакмен пойман призраком
            self.end = True
            self.speed = 0

    def animation(self):
        global course
        self.image.fill('black')
        if self.animCount + 1 >= 20:
            self.animCount = 0
        if self.end:
            self.death_animation()
        else:
            if course == 'left':
                walk_L = [pygame.transform.rotate(i, 180) for i in walk]
                self.image.blit(walk_L[self.animCount // 5], (0, 0))
                self.animCount += 1
            elif course == 'right':
                self.image.blit(walk[self.animCount // 5], (0, 0))
                self.animCount += 1
            elif course == 'up':
                walk_UP = [pygame.transform.rotate(i, 90) for i in walk]
                self.image.blit(walk_UP[self.animCount // 5], (0, 0))
                self.animCount += 1
            elif course == 'down':
                walk_DOWN = [pygame.transform.rotate(i, -90) for i in walk]
                self.image.blit(walk_DOWN[self.animCount // 5], (0, 0))
                self.animCount += 1

    def death_animation(self):
        """Анимация смерти"""
        global lives, new_start, all_results
        anim = death_pacman
        if course == 'right':
            anim = [pygame.transform.rotate(i, 180) for i in anim]
        elif course == 'up':
            anim = [pygame.transform.rotate(i, -90) for i in anim]
        elif course == 'down':
            anim = [pygame.transform.rotate(i, 90) for i in anim]

        if self.animCountdeath + 1 >= 60:
            all_results += self.number_of_points()
            lives -= 1
            new_start = False
            Start_game()
        else:
            self.image.blit(anim[self.animCountdeath // 5], (0, 0))
            self.animCountdeath += 1


    def number_of_points(self):
        """Количество собранных частиц"""
        return self.points

    def checking_pacman_energy(self):
        """Проверка на заряд пакмена"""
        return self.energy, self.time_energy


class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, anim):
        super().__init__(all_sprites)
        self.add(ghosts)

        self.anim = anim
        self.image = pygame.Surface((CELL, CELL))
        self.rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)

        self.animCount = 0
        self.speed = 5 + level / 5
        self.course = 'left'
        self.pasive = True
        self.time_into_prison = 0
        self.darw_score_time = 0  # Длительность надписи
        self.rect_score = 0, 0  # Позиция для отображения надписи

    def update(self):
        self.animation()
        if self.time_into_prison:
            self.time_into_prison -= 0.1
            if self.time_into_prison < 1:
                self.release_from_prison(9, 10)
        if self.darw_score_time >= 0:
            self.darw_score()
        if self.course == 'left':
            self.move(-self.speed, 0)
        elif self.course == 'right':
            self.move(self.speed, 0)
        elif self.course == 'up':
            self.move(0, -self.speed)
        elif self.course == 'down':
            self.move(0, self.speed)

        if pygame.sprite.spritecollideany(self, player_g) and player.checking_pacman_energy()[0]:  # Призрак поймал
            player.points += 400
            self.rect_score = self.rect.x + 20, self.rect.y - 10
            self.darw_score_time = 3
            self.into_prison()

    def move(self, xvel, yvel):
        """Движение призрака"""
        collideList = map

        self.rect.x += xvel
        for block in collideList:
            if self.rect.colliderect(block):
                if xvel < 0:
                    self.rect.left = block.right
                    self.course = choice(['up', 'down'])
                elif xvel > 0:
                    self.rect.right = block.left
                    self.course = choice(['up', 'down'])
                break

        self.rect.y += yvel
        for block in collideList:
            if self.rect.colliderect(block):
                if yvel < 0:
                    self.rect.top = block.bottom
                    self.course = choice(['right', 'left'])
                elif yvel > 0:
                    self.rect.bottom = block.top
                    self.course = choice(['right', 'left'])
                break

    def animation(self):
        self.image.fill('black')
        if self.animCount + 1 >= 10:
            self.animCount = 0
        # Режим испуга
        if player.checking_pacman_energy()[0] and not self.pasive:
            self.speed = 3
            if player.checking_pacman_energy()[1] >= 10:
                self.image.blit(wall_charged[0][self.animCount // 5], (0, 0))
                self.animCount += 1
            else:
                if int(player.checking_pacman_energy()[1]) % 2 == 0:
                    self.image.blit(wall_charged[1][self.animCount // 5], (0, 0))
                    self.animCount += 1
                else:
                    self.image.blit(wall_charged[0][self.animCount // 5], (0, 0))
                    self.animCount += 1

        else:  # Обычный режим
            self.speed = 5 + level / 5
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

    def darw_score(self):
        """Отрисовка стоимости призрака"""
        self.darw_score_time -= 0.1
        font = pygame.font.Font("data\\fonts_i.ttf", 15)
        text = font.render('400', True, [255, 255, 255])
        screen.blit(text, (self.rect_score[0], self.rect_score[1]))

    def release_from_prison(self, x, y):
        """Выход призрака из клетки"""
        self.time_into_prison = 0
        self.pasive = False
        self.course = 'up'
        self.rect = pygame.Rect(x * CELL, y * CELL, CELL, CELL)

    def into_prison(self):
        """Нахождение призрака в клетке"""
        self.pasive = True
        self.time_into_prison = 20
        self.rect = pygame.Rect(8 * CELL, 10 * CELL, CELL, CELL)


def button(x, y, text, s):
    """Создание кнопки"""
    global intro, running
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    font = pygame.font.Font("data\\fonts_i.ttf", s)
    textq = font.render(text, True, [255, 255, 255])
    fontq2 = pygame.font.Font("data\\fonts_i.ttf", s + 10)
    textq2 = fontq2.render(text, True, [255, 255, 255])
    if x < mouse[0] < x + textq.get_rect()[2] and y < mouse[1] < y + textq.get_rect()[3]:
        screen.blit(textq2, (x - (textq2.get_rect()[2] - textq.get_rect()[2]) / 2, y))
        if click == 1:
            return True
    else:
        screen.blit(textq, (x, y))


def footer():
    """Отрисовка счета частиц, количество жизней"""
    font = pygame.font.Font("data\\fonts.ttf", 25)
    text = font.render(f"SCRORE: {player.number_of_points() + all_results}", True, [255, 255, 255])
    screen.blit(text, (10, 670))

    text2 = font.render("LIVES", True, [255, 255, 255])
    screen.blit(text2, (390, 670))
    if lives > 0:
        screen.blit(walk[1], (460, 670))
    if lives > 1:
        screen.blit(walk[1], (500, 670))
    if lives > 2:
        screen.blit(walk[1], (540, 670))
    text = font.render(f"LEVEL {level}", True, [255, 255, 255])
    screen.blit(text, (260, 670))


def Start_game():
    """Завершение при отсутсвии жизней, начальный запуск, отрисовка карты со старыми значениями
     при присутсвии жизней, перезапуск после сбора всех частиц"""
    global player, Blinky, Pinky, Inky, Clyde, map, level, \
        running, restart, course, course_t, lives, all_results, time_en

    if lives == 0:
        restart = True
        running = False

    if new_start:
        for i in all_sprites:
            i.kill()
        all_results = 0
        lives = 3
        level = 1
        map = Board('data\\map.txt')
    else:
        for i in ghosts:
            i.kill()
        player.kill()
    if not new_start and len(point) == 0:
        level += 1
        map = Board('data\\map.txt')

    time_en = 0
    course, course_t = 'left', None
    player = Player(9, 16)
    Blinky = Ghost(9, 8, walk_BLINKY)
    Blinky.pasive = False
    Pinky = Ghost(8, 10, walk_PINKY)
    Inky = Ghost(9, 10, walk_INKY)
    Clyde = Ghost(10, 10, walk_CLYDE)


def timer(number):
    """Отсчет при начале игры"""
    font = pygame.font.Font("data\\fonts_i.ttf", 50)
    text = font.render(str(number), True, [255, 48, 48])
    image = pygame.Surface((CELL, CELL * 2))
    image.fill('blue')
    image.blit(text, (0, 0))
    screen.blit(image, (CELL * 9, CELL * 6))
    pygame.display.flip()
    sleep(1)


def Add_in_table(name, score):
    """Добавление игроков в топ"""
    con = sqlite3.connect('data\list_of_results.db')
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM results""").fetchall()

    flag = False, 0
    for i in result:
        if str(name) == str(i[0]):
            flag = True, i[1]
            break
    if flag[0]:
        if int(flag[1]) < score:
            cur.execute(f"""UPDATE results
            SET SCORE = '{score}'
            WHERE PLAYER = '{str(name)}' """).fetchall()
            con.commit()
    else:
        cur.execute(f"""INSERT INTO results(PLAYER,SCORE) VALUES('{name}', {score})""").fetchall()

    con.commit()
    con.close()


def Intro():
    """Начальный экран"""
    global cycle, intro, table, new_start, running
    while intro:
        for event in pygame.event.get():
            screen.fill('black')
            if event.type == pygame.QUIT:
                cycle = False
                intro = False
            if button(210, 200, 'PLAY', 60) is True:
                new_start = True
                Start_game()
                intro = False
                running = True
            elif button(110, 280, 'HIGH SCORES', 60) is True:
                intro = False
                table = True
            screen.blit(pygame.image.load(os.path.join('data', 'intro.png')), (80, 50))
        pygame.display.flip()


def Runing():
    """Игровой цикл"""
    global cycle, running, time_en, course_t
    clock = pygame.time.Clock()
    while running:
        time_en += 1
        if time_en == 3:
            timer(3)
        elif time_en == 4:
            timer(2)
        elif time_en == 5:
            timer(1)
        else:
            screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cycle = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        course_t = 'left'
                    elif event.key == pygame.K_RIGHT:
                        course_t = 'right'
                    elif event.key == pygame.K_UP:
                        course_t = 'up'
                    elif event.key == pygame.K_DOWN:
                        course_t = 'down'
            # Выход призраков
            if time_en == 200:
                Pinky.release_from_prison(9, 10)
            if time_en == 400:
                Inky.release_from_prison(9, 10)
            if time_en == 600:
                Clyde.release_from_prison(9, 10)

            all_sprites.draw(screen)
            all_sprites.update()
            footer()

        clock.tick(30)
        pygame.display.flip()


def Restart():
    """Окно после завершения игры"""
    global restart, cycle, intro, new_start, running

    font = pygame.font.Font(None, 32)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive

    input_box = pygame.Rect(155, 250, 270, 32)
    input_text = '  CREATE NICKNAME'
    active = False
    input_button = True

    while restart:
        for event in pygame.event.get():
            screen.fill('black')
            if event.type == pygame.QUIT or button(240, 440, 'EXIT', 60) is True:
                cycle = False
                restart = False
            if button(220, 370, 'MENU', 60):
                intro = True
                restart = False
            if button(180, 300, 'RESTART', 60):
                new_start = True
                Start_game()
                restart = False
                running = True
            # Button input name
            if input_button:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            color = color_inactive
                            input_button = False
                            Add_in_table(input_text, all_results)
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            if input_text == '  CREATE NICKNAME':
                                input_text = ''
                            if len(input_text) < 18:
                                input_text += event.unicode
            text = font.render(input_text, True, color)
            screen.blit(text, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)

            screen.blit(pygame.image.load(os.path.join('data', 'intro.png')), (80, 50))
            font2 = pygame.font.Font("data\\fonts_i.ttf", 40)
            text = font2.render(f"Your SCRORE: {all_results}", True, [255, 255, 255])
            screen.blit(text, (size[0] / 2 - text.get_rect()[2] / 2, 170))
        if input_text == '  CREATE NICKNAME':
            Add_in_table('[ ]', all_results)
        pygame.display.flip()


def Table():
    """Таблица с 10 лучшими игроками"""
    global cycle, intro, table
    con = sqlite3.connect('data\\list_of_results.db')
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM results""").fetchall()
    result.sort(key=lambda x: x[1])

    result = result[::-1][:10]
    y = 100
    font = pygame.font.Font("data\\fonts_i.ttf", 30)

    while table:
        for event in pygame.event.get():
            screen.fill('black')
            if event.type == pygame.QUIT:
                cycle = False
                table = False
            elif button(250, 630, 'GO BACK', 30) is True:
                table = False
                intro = True

            text = font.render("    NICKNAME                     SCORE", True, [255, 255, 0])
            screen.blit(text, (70, 25))
            for i in result:
                text = font.render(f"{result.index(i) + 1}.   {i[0]}", True, [255, 255, 255])
                screen.blit(text, (70, y))
                a = ''
                for i, ch in enumerate(str(i[1])[::-1]):
                    if i != 0 and i % 3 == 0:
                        a += ' ,'
                    a += ch
                text = font.render(f"{a[::-1]}", True, [255, 255, 255])
                screen.blit(text, (400, y))
                y += 50
            y = 100
        pygame.display.flip()


if __name__ == '__main__':
    CELL = 30
    size = 19 * CELL, 22 * CELL + 50
    pygame.init()
    pygame.display.set_caption('Pacman')
    screen = pygame.display.set_mode(size)

    # Анимации
    walk = [load_image(30, 10, 160, 140), load_image(190, 10, 310, 140),
            load_image(330, 10, 460, 140), load_image(190, 10, 310, 140)]
    walk_BLINKY = []
    walk_PINKY = []
    walk_INKY = []
    walk_CLYDE = []
    wall_charged = [[load_image(390, 640, 530, 780), load_image(560, 640, 700, 780)],
                    [load_image(730, 640, 870, 780), load_image(900, 640, 1040, 780)]]
    death_pacman = []
    Enemies_walk()

    # Спрайты
    all_sprites = pygame.sprite.Group()
    player_g = pygame.sprite.Group()
    borders = pygame.sprite.Group()
    point = pygame.sprite.Group()
    energy_point = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()

    all_results = 0
    lives = 3
    level = 1
    time_en = 0
    course, course_t = 'left', None
    new_start = True
    Start_game()

    intro = True
    running = False
    restart = False
    table = False

    cycle = True
    while cycle:
        Intro()
        Runing()
        Restart()
        Table()
    pygame.quit()
