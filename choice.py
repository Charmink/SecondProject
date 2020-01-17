import pygame
import copy
import os
import random
import sys


pygame.init()
size = width, height = 960, 580
screen = pygame.display.set_mode(size)

MUSIC = {'fon': "data/" + "fon.mp3", 'switch': "data/" + "switch.wav",
         'play': "data/" + "play.wav", 'back': "data/" + "back.wav",
         'exit': "data/" + "exit.wav"}
GRAVITY = 0.25


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
        if 200 <= pos[0] <= 450 and 220 <= pos[1] <= 300:
            if self.rect.y != 240:
                self.rect.y = 240
                self.marker_drawing = True
                self.music = True
            else:
                self.music = False
        elif 200 <= pos[0] <= 450 and 300 <= pos[1] <= 380:
            if self.rect.y != 320:
                self.rect.y = 320
                self.marker_drawing = True
                self.music = True
            else:
                self.music = False
        elif 200 <= pos[0] <= 450 and 380 <= pos[1] <= 460:
            if self.rect.y != 400:
                self.rect.y = 400
                self.marker_drawing = True
                self.music = True
            else:
                self.music = False
        elif 200 <= pos[0] <= 450 and 460 <= pos[1] <= 540:
            if self.rect.y != 480:
                self.rect.y = 480
                self.marker_drawing = True
                self.music = True
            else:
                self.music = False

        else:
            self.rect.y = 0
            self.marker_drawing = False
            self.music = False


class BackArrow(pygame.sprite.Sprite):
    image = load_image("back.png")

    def __init__(self):
        super().__init__(back_arrow)
        self.image = BackArrow.image
        self.rect = self.image.get_rect()
        self.rect.x = 830
        self.rect.y = 500


class PlayerLeft(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group_l)
        self.i = 0
        self.image = load_image(players_images("left")[self.i])
        self.rect = pygame.Rect(150, 250, 150, 200)

    def update(self, *args):
        self.image = load_image(players_images("left")[self.i])

    def move(self, duration):
        if duration == 0:
            self.rect = self.rect.move(1, 0)

        elif duration == 2:
            self.rect = self.rect.move(-1, 0)

    def jump(self, duration):
        if duration == 1:
            self.rect = self.rect.move(0, -1)
        else:
            self.rect = self.rect.move(0, 1)

    def position(self):
        return self.rect.x, self.rect.y


class PlayerRight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group_r)
        self.j = 0
        self.image = load_image(players_images("right")[self.j])
        self.rect = pygame.Rect(650, 250, 150, 200)

    def update(self, *args):
        if args:
            self.image = load_image(players_images("right")[args[0] % len(players_images("right"))])
        else:
            self.image = load_image(players_images("right")[self.j])

    def move(self, duration):
        if duration == 0:
            self.rect = self.rect.move(1, 0)

        elif duration == 2:
            self.rect = self.rect.move(-1, 0)

    def jump(self, duration):
        if duration == 1:
            self.rect = self.rect.move(0, -1)
        else:
            self.rect = self.rect.move(0, 1)

    def position(self):
        return self.rect.x, self.rect.y


class StartButton(pygame.sprite.Sprite):
    image = load_image('play.png')

    def __init__(self):
        super().__init__(start_button)
        self.image = StartButton.image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 250


class BackGround(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('start.png'), (960, 580))

    def __init__(self):
        super().__init__(back_ground)
        self.image = BackGround.image
        self.rect = self.image.get_rect()


class Ball(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('Ball.png'), (50, 50))

    def __init__(self):
        super().__init__(ball)
        self.image = Ball.image
        self.rect = self.image.get_rect()
        self.rect.x = 600
        self.rect.y = 400
        self.count_st = 0

    def start(self):
        self.count_st += 1
        if self.count_st % 2 == 1:
            self.rect.x = 700
            self.rect.y = 200
        else:
            self.rect.x = 200
            self.rect.y = 200

    def position(self):
        return self.rect.x, self.rect.y

    def shot1(self, key):
        if key == 1:
            if self.rect.x <= 300:
                self.rect = self.rect.move(3, -1)
                self.rect = self.rect.move(1, 0)
            elif self.rect.x <= 500:
                self.rect = self.rect.move(2, -1)
                self.rect = self.rect.move(1, 0)
            elif self.rect.x <= 540:
                self.rect = self.rect.move(1, 0)
                self.rect = self.rect.move(1, 0)
            elif self.rect.x <= 700:
                self.rect = self.rect.move(2, 1)
                self.rect = self.rect.move(1, 0)
            else:
                self.rect = self.rect.move(2, 2)
                self.rect = self.rect.move(1, 0)
        if key == 2:
            if self.rect.x > 700:
                self.rect = self.rect.move(-3, -1)
                self.rect = self.rect.move(-1, 0)
            elif self.rect.x > 500:
                self.rect = self.rect.move(-2, -1)
                self.rect = self.rect.move(-1, 0)
            elif 500 < self.rect.x <= 540:
                self.rect = self.rect.move(-1, 0)
                self.rect = self.rect.move(-1, 0)
            elif 300 < self.rect.x <= 500:
                self.rect = self.rect.move(-2, 1)
                self.rect = self.rect.move(-1, 0)
            elif self.rect.x < 300:
                self.rect = self.rect.move(-2, 2)
                self.rect = self.rect.move(-1, 0)

    def shot2(self, key, ballstart):
        if key == 1:
            if self.rect.x < ballstart + 250:
                self.rect = self.rect.move(3, -1)
                self.rect = self.rect.move(1, 0)
            elif self.rect.x < ballstart + 270:
                self.rect = self.rect.move(5, -1)
            elif self.rect.x < ballstart + 300:
                self.rect = self.rect.move(1, 0)
                self.rect = self.rect.move(1, 0)
            else:
                self.rect = self.rect.move(2, +2)
                self.rect = self.rect.move(1, 0)
        if key == 2:
            if self.rect.x > ballstart - 250:
                self.rect = self.rect.move(-3, -1)
                self.rect = self.rect.move(-1, 0)
            elif self.rect.x > ballstart - 280:
                self.rect = self.rect.move(-5, -1)
            elif self.rect.x > ballstart - 300:
                self.rect = self.rect.move(-1, 0)
                self.rect = self.rect.move(-1, 0)
            else:
                self.rect = self.rect.move(-2, 2)
                self.rect = self.rect.move(-1, 0)

    def shot3(self, key, ballstart):
        polet = random.randrange(280, 310)
        if key == 1:
            if self.rect.x < ballstart + polet:
                self.rect = self.rect.move(2, -1)
                self.rect = self.rect.move(1, 0)
            elif self.rect.x < ballstart + polet + 30:
                self.rect = self.rect.move(5, -1)
            elif self.rect.x < ballstart + polet + 50:
                self.rect = self.rect.move(1, 0)
                self.rect = self.rect.move(1, 0)
            else:
                self.rect = self.rect.move(2, +2)
                self.rect = self.rect.move(1, 0)
        if key == 2:
            if self.rect.x > ballstart - polet:
                self.rect = self.rect.move(-2, -1)
                self.rect = self.rect.move(-1, 0)
            elif self.rect.x > ballstart - polet - 30:
                self.rect = self.rect.move(-5, -1)
            elif self.rect.x > ballstart - polet - 50:
                self.rect = self.rect.move(-1, 0)
                self.rect = self.rect.move(-1, 0)
            else:
                self.rect = self.rect.move(-2, 2)
                self.rect = self.rect.move(-1, 0)


class Sound(pygame.sprite.Sprite):
    image_1 = load_image('sound.png')
    image_2 = load_image('sound_mute.png')

    def __init__(self):
        super().__init__(sound)
        self.image = Sound.image_1
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(900, 30)
        self.cnt = 1

    def update(self):
        self.cnt = (self.cnt + 1) % 2
        if not self.cnt:
            self.image = Sound.image_2
        else:
            self.image = Sound.image_1


screen_rect = (0, 0, width, height)


class Particle(pygame.sprite.Sprite):

    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(salut)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, period):
    if period != 1:
        return
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def mute():
    if sound_obj.cnt:
        pygame.mixer.music.set_volume(0.1)
        choice_hero.set_volume(0.3)
        start.set_volume(0.1)
        back.set_volume(0.6)
        ex.set_volume(0.4)
    else:
        pygame.mixer.music.set_volume(0)
        choice_hero.set_volume(0)
        start.set_volume(0)
        back.set_volume(0)
        ex.set_volume(0)


def main_menu():
    intro_text = ["Volleyball", "",  "Play", "Control", "Developers", "Exit"]
    screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if marker_obj.rect.y == 240:
                        start.play()
                        pygame.time.delay(100)
                        choice()
                    elif marker_obj.rect.y == 320:
                        start.play()
                        control()
                    elif marker_obj.rect.y == 400:
                        start.play()
                        developers()
                    elif marker_obj.rect.y == 480:
                        ex.play()
                        pygame.time.delay(200)
                        terminate()
                    elif 885 < event.pos[0] < 920 and 20 < event.pos[1] < 55:
                        sound.update()
                        mute()
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(0)
                all_sprites.update(event)
                marker.update(event.pos)

        screen.fill(pygame.Color("white"))
        back_ground.draw(screen)
        text_coord = 50
        font = pygame.font.Font('data/shs.ttf', 50)
        for line in intro_text:
            string = font.render(line, 1, pygame.Color("white"))
            intro_rect = string.get_rect()
            if line == 'Volleyball':
                intro_rect.x = 350
            else:
                intro_rect.x = 200
            text_coord += 15
            intro_rect.top = text_coord
            text_coord += intro_rect.height
            screen.blit(string, intro_rect)
        player_group_r.update(1)
        player_group_r.draw(screen)
        ball.draw(screen)
        sound.draw(screen)
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
    intro_text = ["Control", "", "To the left - A | Left arrow",
                  "To the right - D | Right arrow", "Jump - W | Up arrow",
                  "Hit - Space | Ctrl"]
    screen.fill(pygame.Color("white"))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_arrow_obj.rect.x - 10 <= event.pos[0] <= \
                            back_arrow_obj.rect.x + 80 and \
                            back_arrow_obj.rect.y <= event.pos[1] <= back_arrow_obj.rect.y + 50:
                        back.play()
                        pygame.time.delay(100)
                        main_menu()
                    elif 885 < event.pos[0] < 920 and 20 < event.pos[1] < 55:
                        sound.update()
                        mute()
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(0)
                all_sprites.update(event)
                marker.update(event.pos)

        screen.fill(pygame.Color("white"))
        back_ground.draw(screen)
        back_arrow.draw(screen)
        sound.draw(screen)
        text_coord = 50
        for line in intro_text:
            if line == "Control":
                font = pygame.font.Font('data/shs.ttf', 50)
            else:
                font = pygame.font.Font('data/shs.ttf', 40)
            string = font.render(line, 1, pygame.Color("white"))
            intro_rect = string.get_rect()
            if line == "Control":
                intro_rect.x = 400
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
    intro_text = ["Choice heroes", "",
                  'First player                         Second player']
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
                        start_button_obj.rect.y <= event.pos[1] <= start_button_obj.rect.y + 150:
                    start.play()
                    game()
                elif event.button == 1 and \
                        back_arrow_obj.rect.x - 10 <= event.pos[0] <= \
                        back_arrow_obj.rect.x + 80 and \
                        back_arrow_obj.rect.y <= event.pos[1] <= back_arrow_obj.rect.y + 50:
                    back.play()
                    pygame.time.delay(100)
                    main_menu()
                elif event.button == 1 and 885 < event.pos[0] < 920 and 20 < event.pos[1] < 55:
                    sound.update()
                    mute()
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(0)
                all_sprites.update(event)

        screen.fill(pygame.Color("white"))
        back_ground.draw(screen)
        back_arrow.draw(screen)
        player_group_l.update()
        player_group_r.update()
        player_group_l.draw(screen)
        player_group_r.draw(screen)
        sound.draw(screen)
        text_coord = 50
        for line in intro_text:
            if line == "Choice heroes":
                font = pygame.font.Font('data/shs.ttf', 50)
            else:
                font = pygame.font.Font('data/shs.ttf', 30)
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


def game():
    clock = pygame.time.Clock()
    ball_obj.start()
    key = False
    key2 = False
    jump = False
    jump2 = False
    shot = -1
    ball_key = None
    k = None
    k2 = None
    ballstart = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    key = 0
                    player_r_obj.move(0)
                elif event.key == pygame.K_LEFT:
                    key = 2
                    player_r_obj.move(2)
                elif event.key == pygame.K_UP:
                    if not jump:
                        k = 0
                        jump = True
                if event.key == pygame.K_d:
                    key2 = 0
                    player_l_obj.move(0)
                elif event.key == pygame.K_a:
                    key2 = 2
                    player_l_obj.move(2)
                elif event.key == pygame.K_w:
                    if not jump2:
                        k2 = 0
                        jump2 = True
                if event.key == pygame.K_SPACE:
                    a, b = player_l_obj.position()
                    ab, bb = ball_obj.position()
                    print(a, b, ab, bb)
                    if abs(a + 50 - ab) <= 50 and abs(b + 100 - bb) <= 150:
                        ballstart = ab
                        shot = random.choice(range(3))
                        ball_key = 1

                if event.key == 305:
                    a, b = player_r_obj.position()
                    ab, bb = ball_obj.position()
                    print(a, b, ab, bb)
                    if abs(a + 50 - ab) <= 50 and abs(b + 100 - bb) <= 150:
                        ballstart = ab
                        shot = random.choice(range(3))
                        ball_key = 2

            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) \
                        and pygame.key.get_pressed()[275] == 0 and \
                        pygame.key.get_pressed()[276] == 0:
                    key = False
                if (event.key == 100 or event.key == 97) \
                        and pygame.key.get_pressed()[97] == 0 and \
                        pygame.key.get_pressed()[100] == 0:
                    key2 = False

        if shot == 0:
            if ball_key == 1:
                ab, bb = ball_obj.position()
                if bb <= 450:
                    ball_obj.shot1(1)
                else:
                    ball_key = 0
            ab, bb = ball_obj.position()
            if ball_key == 2:
                ab, bb = ball_obj.position()
                if bb <= 450:
                    ball_obj.shot1(2)
                else:
                    ball_key = 0
        if shot == 1:
            if ball_key == 1:
                ab, bb = ball_obj.position()
                if bb <= 450:
                    ball_obj.shot2(1, ballstart)
                else:
                    ball_key = 0
            ab, bb = ball_obj.position()
            if ball_key == 2:
                ab, bb = ball_obj.position()
                if bb <= 450:
                    ball_obj.shot2(2, ballstart)
                else:
                    ball_key = 0
        if shot == 2:
            if ball_key == 1:
                ab, bb = ball_obj.position()
                if bb <= 450:
                    ball_obj.shot3(1, ballstart)
                else:
                    ball_key = 0
            ab, bb = ball_obj.position()
            if ball_key == 2:
                ab, bb = ball_obj.position()
                if bb <= 450:
                    ball_obj.shot3(2, ballstart)
                else:
                    ball_key = 0
        ab, bb = ball_obj.position()

        if bb >= 450:
            ball_key = 0
            clock.tick(5)
            clock.tick(5)
            ball_obj.start()
        if jump:
            if k < 50:
                player_r_obj.jump(1)
            else:
                player_r_obj.jump(2)
            k += 1
            if k == 100:
                jump = False
                k = 0
        # Прыжок второго игрока
        if jump2:
            if k2 < 50:
                player_l_obj.jump(1)
            else:
                player_l_obj.jump(2)
            k2 += 1
            if k2 == 100:
                jump2 = False
                k2 = 0

        if key is not False:
            player_r_obj.move(key)
        if key2 is not False:
            player_l_obj.move(key2)
        screen.fill(pygame.Color("white"))
        back_ground.draw(screen)
        player_group_l.draw(screen)
        player_group_r.draw(screen)
        ball.draw(screen)
        clock.tick(50)
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
ball = pygame.sprite.Group()
sound = pygame.sprite.Group()
salut = pygame.sprite.Group()


ball_obj = Ball()
back_obj = Arrow()
marker_obj = MarkerArrow()
player_l_obj = PlayerLeft()
player_r_obj = PlayerRight()
back_arrow_obj = BackArrow()
start_button_obj = StartButton()
back_ground_obj = BackGround()
sound_obj = Sound()

pygame.mixer.music.load(MUSIC['fon'])
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

choice_hero = pygame.mixer.Sound(MUSIC['switch'])
choice_hero.set_volume(0.3)

start = pygame.mixer.Sound(MUSIC['play'])
start.set_volume(0.1)

back = pygame.mixer.Sound(MUSIC['back'])
back.set_volume(0.6)

ex = pygame.mixer.Sound(MUSIC['exit'])
ex.set_volume(0.4)

main_menu()
running = True
