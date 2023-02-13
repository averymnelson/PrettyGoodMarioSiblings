import pygame
import random
import time

from pygame.locals import *
from time import sleep

red = random.randint(0, 255)
green = random.randint(0, 255)
blue = random.randint(0, 255)


class Sprite:
    def __init__(self, x1, y1):
        super().__init__()
        self.x = x1
        self.y = y1
        self.w = 100
        self.h = 100

    def ispipe(self):
        return False

    def ismario(self):
        return False

    def isgoomba(self):
        return False

    def isfireball(self):
        return False


class Mario(Sprite):
    def __init__(self, x1, y1):
        super().__init__(x1, y1)
        self.x = x1
        self.y = y1
        self.w = 60
        self.h = 95
        self.vertVel = 0
        self.jumping = False
        self.prevx = 0
        self.prevy = 0
        self.groundtime = 0
        self.marionum = 0
        self.jumptime = 0
        self.marioimg = []
        self.marioimg.append(pygame.image.load("mario1.png"))
        self.marioimg.append(pygame.image.load("mario2.png"))
        self.marioimg.append(pygame.image.load("mario3.png"))
        self.marioimg.append(pygame.image.load("mario4.png"))
        self.marioimg.append(pygame.image.load("mario5.png"))

    def coordinates(self):
        # print("CALLING SET PREVIOUS")
        self.prevx = self.x
        self.prevy = self.y

    def update(self):
        # print("mario updated")
        self.vertVel += 1.2
        self.y += self.vertVel
        if self.y > 500:
            self.vertVel = 0.0
            self.y = 500
            self.groundtime = 0
        self.groundtime += 1
        if self.jumping:
            self.jumptime += 1

    def getout(self, p):
        # print("X OF MARIO", self.x)
        # print("prevX OF MARIO", self.prevx)
        if (self.y + self.h >= p.y) and (self.prevy + self.h <= p.y):
            self.vertVel = 0.0
            self.y = p.y - self.h
            self.groundtime = 0
            # print("t/b")
        if (self.y <= p.y + p.h) and (self.prevy >= p.y + p.h):
            self.vertVel = 0.0
            self.y = p.y + p.h
            # print("t/b")
        if (self.x + self.w >= p.x) and (self.prevx + self.w <= p.x):
            self.x = p.x - self.w
            # print("l/r")
        if (self.x <= p.x + p.w) and (self.prevx >= p.x + p.w):
            self.x = p.x + p.w
            # print("l/r")

    def ispipe(self):
        return False

    def ismario(self):
        return True

    def isgoomba(self):
        return False

    def isfireball(self):
        return False


class Pipe(Sprite):
    def __init__(self, x1, y1):
        super().__init__(x1, y1)
        self.w = 55
        self.h = 400
        self.pipetemp = pygame.image.load("pipe.png")

    def update(self):
        pass

    def ispipe(self):
        return True

    def ismario(self):
        return False

    def isgoomba(self):
        return False

    def isfireball(self):
        return False


class Goomba(Sprite):
    def __init__(self, x1, y1):
        super().__init__(x1, y1)
        self.w = 37
        self.h = 45
        self.vertVel = 0
        self.onfire = False
        self.killcounter = 0
        self.prevxg = 0
        self.xvel = 4
        self.goombafire = pygame.image.load("goomba_fire.png")
        self.goomba = pygame.image.load("goomba.png")
    # 	image junk

    def changedirection(self):
        self.xvel = self.xvel * (-1)

    def coordinates(self):
        self.prevxg = self.x

    def update(self):
        # print("goomba updated")
        self.coordinates()
        self.vertVel += 1.2
        self.y += self.vertVel
        if self.y > 545:
            self.vertVel = 0.0
            self.y = 545
        self.fire()
        self.x += self.xvel

    def fire(self):
        if self.onfire:
            self.killcounter += 1
            self.xvel = 0

    def getout(self, p):
        if (self.x + self.w >= p.x) and (self.prevxg + self.w <= p.x):
            self.x = p.x - self.w
            self.changedirection()
        if (self.x <= p.x + p.w) and (self.prevxg >= p.x + p.w):
            self.x = p.x + p.w
            self.changedirection()

    def ispipe(self):
        return False

    def ismario(self):
        return False

    def isgoomba(self):
        return True

    def isfireball(self):
        return False


class Fireball(Sprite):
    def __init__(self, x1, y1):
        super().__init__(x1, y1)
        self.w = 47
        self.h = 47
        self.vertVel = 0
        self.fireball = pygame.image.load("fireball.png")

    def update(self):
        # print("thrown")
        self.vertVel += 1.2
        self.y += self.vertVel
        if self.y > 550:
            self.vertVel = -10
        self.x += 20

    def ispipe(self):
        return False

    def ismario(self):
        return False

    def isgoomba(self):
        return False

    def isfireball(self):
        return True


class Model:
    def __init__(self):
        # array append
        # self.sprites.append(Lettuce(x, y)
        # for loop variation
        # for sprite in self.model.sprites:
        self.grey = True
        self.sprites = []
        self.removed = []
        self.mario = Mario(100, 100)
        self.sprites.append(self.mario)

        self.sprites.append(Pipe(287, 550))
        self.sprites.append(Pipe(311, 586))
        self.sprites.append(Pipe(497, 580))
        self.sprites.append(Pipe(589, 512))
        self.sprites.append(Pipe(791, 509))
        self.sprites.append(Pipe(937, 580))
        self.sprites.append(Pipe(1061, 515))
        self.sprites.append(Pipe(1179, 530))
        self.sprites.append(Pipe(1633, 575))
        self.sprites.append(Pipe(1870, 560))
        self.goombaadd = 0
        while self.goombaadd < 25:
            self.moresprites = random.randint(310, 1750)
            self.sprites.append(Goomba(self.moresprites, 400))
            self.goombaadd += 1
        self.sprites.append(Goomba(562, 400))
        self.sprites.append(Goomba(615, 400))

    def throwfire(self):
        self.sprites.append(Fireball((self.mario.x + self.mario.w), (self.mario.y + self.mario.h / 2)))

    def collision(self, mr, p):
        self.grey = True
        if mr.x + mr.w < p.x:
            self.grey = False
        if mr.x > p.x + p.w:
            self.grey = False
        if mr.y + mr.h < p.y:
            self.grey = False
        if mr.y > p.y + p.h:
            self.grey = False
        return self.grey

    def update(self):
        self.removed = []
        for i in self.sprites:
            i.update()
            for j in range(1, len(self.sprites)):
                if self.collision(i, self.sprites[j]):
                    if i.ismario():
                        if self.sprites[j].ispipe():
                            i.getout(self.sprites[j])

                    if i.isgoomba():
                        if self.sprites[j].ispipe():
                            i.getout(self.sprites[j])

                        if self.sprites[j].isfireball():
                            self.removed.append(self.sprites[j])
                            i.onfire = True
                        if i.onfire and i.killcounter >= 15:
                            self.removed.append(i)
                if i.isfireball():
                    if i.x - self.mario.x >= 680:
                        # print("FIREBALL: ", i)
                        self.removed.append(i)
        for i in self.removed:
            if i in self.sprites:
                self.sprites.remove(i)


class View:
    def __init__(self, model):
        screen_size = (800, 650)
        self.scrollPos = model.mario.x - 100
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.model = model

    def update(self):
        # print("calling view draw")
        # print("draw set")
        self.scrollPos = self.model.mario.x - 100
        self.screen.fill([red, green, blue])
        pygame.draw.line(self.screen, 'black', (0, 590), (2000, 590), width=1)
        for i in self.model.sprites:
            sprite = i
            if sprite.isgoomba():
                if sprite.onfire:
                    self.screen.blit(sprite.goombafire, (sprite.x - self.scrollPos, sprite.y))
                else:
                    self.screen.blit(sprite.goomba, (sprite.x - self.scrollPos, sprite.y))
            if sprite.ispipe():
                self.screen.blit(sprite.pipetemp, (sprite.x - self.scrollPos, sprite.y))
            if sprite.isfireball():
                self.screen.blit(sprite.fireball, (sprite.x - self.scrollPos, sprite.y))
            if sprite.ismario():
                self.screen.blit(sprite.marioimg[sprite.marionum], (sprite.x - self.scrollPos, sprite.y))
        pygame.display.flip()


class Controller:
    def __init__(self, model):
        self.model = model
        self.keep_going = True

    def update(self):
        self.model.mario.coordinates()
        for event in pygame.event.get():
            if event.type == QUIT:
                print("Thanks for playing!")
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.model.mario.jumping = True
                if event.key == K_ESCAPE:
                    print("Thanks for playing!")
                    self.keep_going = False
            elif event.type == KEYUP:
                if event.key == K_RCTRL or event.key == K_LCTRL:
                    self.model.throwfire()
                if event.key == K_1 or event.key == K_KP1:
                    print("RGB:", red, ",", green, ",", blue)
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     self.model.set_dest(pygame.mouse.get_pos())
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT]:
            self.model.mario.x += 20
            if self.model.mario.marionum >= 4:
                self.model.mario.marionum = 0
            else:
                self.model.mario.marionum += 1
        if keys[K_LEFT]:
            # self.model.mario.coordinates()
            self.model.mario.x -= 20
            if self.model.mario.marionum <= 0:
                self.model.mario.marionum = 4
            else:
                self.model.mario.marionum -= 1
        if keys[K_SPACE]:
            if (self.model.mario.vertVel == 0) and (self.model.mario.jumptime < 3):
                self.model.mario.vertVel = -15.0
            else:
                if (self.model.mario.vertVel == 0) and (self.model.mario.jumptime >= 3):
                    self.model.mario.vertVel = -25.0
            self.model.mario.jumptime = 0


print("Use the L & R arrow keys to move, space to jump, control to throw fireballs, and ESC to quit.")
print("To get the randomized RGB code of the background, press 1.")
# pygame.init()


m = Model()
v = View(m)
c = Controller(m)
# print("CALLING")
while c.keep_going:
    c.update()
    m.update()
    # print("about to call view update")
    v.update()
    sleep(0.04)
