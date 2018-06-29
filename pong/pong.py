import pygame, os

class paddle(pygame.sprite.Sprite):
    def __init__(self, w, h):
        pygame.sprite.Sprite.__init__(self)
        # Here, we set the height, width, and displacement/delta  of x
        self.height = 10
        self.width = 70
        self.dx = 20
        # Here we create a pygame Surface object
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill([50,255,200])
        self.rect = self.image.get_rect()
        #
        self.rect.x = w/2
        self.rect.y = h - 60

    def update(self, pressed_keys,w):
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.dx, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.dx, 0)
        if self.rect.x < -self.width + 10:
            self.rect.x = -self.width + 10
        if self.rect.x > w - 10:
            self.rect.x = w - 10

class ball(pygame.sprite.Sprite):
    def __init__(self, color, speed):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.radius = 10
        self.dx = speed + 1
        self.dy = speed - 1

        self.image = pygame.Surface([20,20])
        self.image.fill([255,255,255])
        self.rect = self.image.get_rect()
        self.image.set_colorkey([255,255,255])
        pygame.draw.circle(self.image, self.color, [10,10], self.radius, 0)

        self.paddle_collision = pygame.mixer.Sound("resources/bleep8bit.wav")
        self.wall_collision = pygame.mixer.Sound("resources/plop8bit.wav")
        self.wall_collision.set_volume(0.10)


    def update(self, paddle, points_display, w, h):
        self.rect.move_ip(self.dx, self.dy)
        if self.rect.x < 0 or self.rect.x > w:
            self.dx *= -1
            self.wall_collision.play()
        if self.rect.y < 0:
            self.dy *= -1
            self.wall_collision.play()
        if self.rect.y > h-40:
            self.kill()
            self.wall_collision.play()
        if pygame.sprite.collide_rect(self, paddle):
            self.dy *= -1
            self.paddle_collision.play()
            points_display.increment_points()


class points_display():
    def __init__(self, w):
        self.points = 0
        self.point_string = str(self.points)
        print(os.getcwd())
        #self.image = pygame.image.load(os.getcwd() + "/resources/cloud.jpg").conver_alpha()
        self.image = pygame.image.load("resources/graph.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,0))
        self.rect.x = w - 200
        self.rect.y = 15
        self.font = pygame.font.Font(None, 35)
        self.score_text = self.font.render("Score: " + self.point_string,1,(100,100,255))
        self.score_position = self.score_text.get_rect()
        self.score_position.x = self.rect.x + (self.rect.width/2) - 58
        self.score_position.y = self.rect.y + (self.rect.height/2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.score_text, self.score_position)

    def increment_points(self):
        self.points += 1
        self.point_string = str(self.points)
        self.score_text = self.font.render("Score: " + self.point_string,1,(100,100,255))


class background_music():
    def __init__(self):
        self.music = pygame.mixer.music.load("resources/offlimits.wav")
    def play(self):
        if pygame.mixer.music.get_busy():
            pass
        else:
            pygame.mixer.music.play()


class game():
    def __init__(self):
        self.running = True

        self.w = 700
        self.h = 600
        self.screen = pygame.display.set_mode([self.w, self.h])

        pygame.init()
        pygame.mixer.init()

        self.background = pygame.image.load("resources/graph.jpg")
        self.background_music = background_music()

        self.bg = pygame.sprite.Group()
        self.points_display = points_display(self.w)
        self.p = pygame.sprite.Group()

        self.firstBall = ball([215, 150, 255], 10)
        self.bg.add(self.firstBall)
        self.paddle = paddle(self.w, self.h)
        self.p.add(self.paddle)

    def main_loop(self):
        while self.running:
            self.screen.fill([255, 255, 255])
            self.screen.blit(self.background, (0,0))
            self.points_display.draw(self.screen)
            self.background_music.play()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.pressed_keys = pygame.key.get_pressed()
            self.paddle.update(self.pressed_keys, self.w)
            if self.pressed_keys[pygame.K_SPACE]:
                self.firstBall = ball([215,150, 210], 10)
                self.bg.add(self.firstBall)
                print("ah")
            self.bg.draw(self.screen)
            self.p.draw(self.screen)
            for b in self.bg:
                b.update(self.paddle, self.points_display, self.w, self.h)

            pygame.display.update()

        pygame.quit()


# How we actually run the game
g = game()
g.main_loop()

