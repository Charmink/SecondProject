import pygame
import copy
import os
import random
import sys


pygame.init()
size = width, height = 960, 540
screen = pygame.display.set_mode(size)

MUSIC = {'fon': "data/" + "fon.mp3", 'switch': "data/" + "switch.wav",
         'play': "data/" + "play.wav", 'back': "data/" + "back.wav",
         'exit': "data/" + "exit.wav"}


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def players_images(duration):
    players = None
    if duration == 'left':
        file = open('data/player_l.txt', 'r')
        players = [line.strip() for line in file]
    elif duration == 'right':
        file = open('data/player_r.txt', 'r')
        players = [line.strip() for line in file]
    return players


class Arrow(pygame.sprite.Sprite):
    image = load_image("arrow.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Arrow.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = random.randrange(height)

    def update(self, *args):

        if args and args[0].type == pygame.MOUSEMOTION:
            self.rect.x = args[0].pos[0]
            self.rect.y = args[0].pos[1]
        else:
            self.rect.x = width
            self.rect.y = height


class MarkerArrow(pygame.sprite.Sprite):
    image = load_image('marker.png')

    def __init__(self):
        super().__init__(marker)
        self.image = MarkerArrow.image
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 0
        self.marker_drawing = False
        self.music = True

    def update(self, pos):
        if 200 <= pos[0] <= 450 and 160 <= pos[1] <= 200:
            if self.rect.y != 165:
                self.rect.y = 165
                self.marker_drawing = True
                self.music = True
            else:
                self.music = False
        elif 200 <= pos[0] <= 450 and 210 <= pos[1] <= 250:
            if self.rect.y != 215:
                self.rect.y = 215
                self.marker_drawing = True
                self.music = True
            else:
                self.music = False
        elif 200 <= pos[0] <= 450 and 260 <= pos[1] <= 300:
            if self.rect.y != 265:
                self.rect.y = 265
                self.marker_drawing = True
                self.music = True
            else:
                self.music = False
        elif 200 <= pos[0] <= 450 and 310 <= pos[1] <= 350:
            if self.rect.y != 315:
                self.rect.y = 315
                self.marker_drawing = True
                self.music = True
            else:
                self.music = False

        else:
            self.rect.y = 0
            self.marker_drawing = False
            self.music = False


class BackArrow(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("back.png"), (70, 50))

    def __init__(self):
        super().__init__(back_arrow)
        self.image = BackArrow.image
        self.rect = self.image.get_rect()
        self.rect.x = 830
        self.rect.y = 450


class PlayerLeft(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group_l)
        self.i = 0
        self.image = load_image(players_images("left")[self.i])
        self.rect = pygame.Rect(150, 200, 150, 200)

    def update(self, *args):
        self.image = load_image(players_images("left")[self.i])


class PlayerRight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group_r)
        self.j = 0
        self.image = load_image(players_images("right")[self.j])
        self.rect = pygame.Rect(650, 200, 150, 200)

    def update(self, *args):
        self.image = load_image(players_images("right")[self.j])


class StartButton(pygame.sprite.Sprite):
    image = load_image('play.png')

    def __init__(self):
        super().__init__(start_button)
        self.image = StartButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 200


class BackGround(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('start.png'), (960, 540))

    def __init__(self):
        super().__init__(back_ground)
        self.image = BackGround.image
        self.rect = self.image.get_rect()


def main_menu():
    intro_text = ["", "",  "Играть", "Управление", "Разработчики", "Выход"]
    screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if marker_obj.rect.y == 165:
                        start.play()
                        pygame.time.delay(100)
                        choice()
                    elif marker_obj.rect.y == 215:
                        start.play()
                        control()
                    elif marker_obj.rect.y == 265:
                        start.play()
                        developers()
                    elif marker_obj.rect.y == 315:
                        ex.play()
                        pygame.time.delay(200)
                        terminate()
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(0)
                all_sprites.update(event)
                marker.update(event.pos)
                if marker_obj.music:
                    choice_hero.play()

        screen.fill(pygame.Color("white"))
        back_ground.draw(screen)
        text_coord = 50
        font = pygame.font.Font(None, 50)
        for line in intro_text:
            string = font.render(line, 1, pygame.Color("white"))
            intro_rect = string.get_rect()
            intro_rect.x = 200
            text_coord += 15
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string, intro_rect)

        clock.tick(30)
        if not pygame.mouse.get_focused():
            all_sprites.update()
        all_sprites.draw(screen)
        if marker_obj.marker_drawing:
            marker.draw(screen)
        pygame.display.flip()


def developers():
    pass


def control():
    intro_text = ["Назначение клавиш", "", "", "Влево - A / Стрелка влево",
                  "Вправо - D / Стрелка вправо", "Прыжок - W / Стрелка вверх",
                  "Удар - Space / Ctrl"]
    screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_arrow_obj.rect.x <= event.pos[0] <= back_arrow_obj.rect.x + 70 and \
                            back_arrow_obj.rect.y <= event.pos[1] <= back_arrow_obj.rect.y + 50:
                        back.play()
                        pygame.time.delay(100)
                        main_menu()
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(0)
                all_sprites.update(event)
                marker.update(event.pos)

        screen.fill(pygame.Color("white"))
        back_ground.draw(screen)
        back_arrow.draw(screen)
        text_coord = 50
        for line in intro_text:
            if line == "Назначение клавиш":
                font = pygame.font.Font(None, 50)
            else:
                font = pygame.font.Font(None, 40)
            string = font.render(line, 1, pygame.Color("white"))
            intro_rect = string.get_rect()
            if line == "Назначение клавиш":
                intro_rect.x = 300
            else:
                intro_rect.x = 200
            text_coord += 15
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string, intro_rect)

        clock.tick(30)
        if not pygame.mouse.get_focused():
            all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()


def choice():
    intro_text = ["Выбор персонажей", "",
                  'Player - 1                                              Player - 2']
    screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    if player_l_obj.rect.x + 150 >= event.pos[0] >= player_l_obj.rect.x and \
                            player_l_obj.rect.y + 200 >= event.pos[1] >= player_l_obj.rect.y:
                        player_l_obj.i = (player_l_obj.i + 1) % len(players_images("left"))
                        choice_hero.play()
                    elif player_r_obj.rect.x + 150 >= event.pos[0] >= player_r_obj.rect.x and \
                            player_r_obj.rect.y + 200 >= event.pos[1] >= player_r_obj.rect.y:
                        player_r_obj.j = (player_r_obj.j + 1) % len(players_images("right"))
                        choice_hero.play()

                elif event.button == 5:
                    if player_l_obj.rect.x + 150 >= event.pos[0] >= player_l_obj.rect.x and \
                            player_l_obj.rect.y + 200 >= event.pos[1] >= player_l_obj.rect.y:
                        player_l_obj.i = (player_l_obj.i - 1) % len(players_images("left"))
                        choice_hero.play()
                    elif player_r_obj.rect.x + 150 >= event.pos[0] >= player_r_obj.rect.x and \
                            player_r_obj.rect.y + 200 >= event.pos[1] >= player_r_obj.rect.y:
                        player_r_obj.j = (player_r_obj.j - 1) % len(players_images("right"))
                        choice_hero.play()
                elif event.button == 1 and \
                    start_button_obj.rect.x <= event.pos[0] <= start_button_obj.rect.x + 150 and \
                        start_button_obj.rect.y <= event.pos[1] <= start_button_obj.rect.y + 200:
                    start.play()
                elif event.button == 1 and \
                        back_arrow_obj.rect.x <= event.pos[0] <= back_arrow_obj.rect.x + 70 and \
                        back_arrow_obj.rect.y <= event.pos[1] <= back_arrow_obj.rect.y + 50:
                    back.play()
                    pygame.time.delay(100)
                    main_menu()
                player_group_l.update()
                player_group_r.update()
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(0)
                all_sprites.update(event)

        screen.fill(pygame.Color("white"))
        back_ground.draw(screen)
        back_arrow.draw(screen)
        player_group_l.draw(screen)
        player_group_r.draw(screen)
        text_coord = 50
        for line in intro_text:
            if line == "Выбор персонажей":
                font = pygame.font.Font(None, 50)
            else:
                font = pygame.font.Font(None, 40)
            string = font.render(line, 1, pygame.Color("white"))
            intro_rect = string.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            if line.count(' ') > 5:
                intro_rect.x = 150
            else:
                intro_rect.x = 300
            text_coord += intro_rect.height
            screen.blit(string, intro_rect)

        clock.tick(30)
        start_button.draw(screen)
        if not pygame.mouse.get_focused():
            all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()


player = None
back_ground = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
marker = pygame.sprite.Group()
player_group_l = pygame.sprite.Group()
player_group_r = pygame.sprite.Group()
back_arrow = pygame.sprite.Group()
start_button = pygame.sprite.Group()

back_obj = Arrow()
marker_obj = MarkerArrow()
player_l_obj = PlayerLeft()
player_r_obj = PlayerRight()
back_arrow_obj = BackArrow()
start_button_obj = StartButton()
back_ground_obj = BackGround()

pygame.mixer.music.load(MUSIC['fon'])
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

choice_hero = pygame.mixer.Sound(MUSIC['switch'])
choice_hero.set_volume(0.1)

start = pygame.mixer.Sound(MUSIC['play'])
start.set_volume(0.1)

back = pygame.mixer.Sound(MUSIC['back'])
back.set_volume(0.6)

ex = pygame.mixer.Sound(MUSIC['exit'])
ex.set_volume(0.4)

main_menu()
running = True
