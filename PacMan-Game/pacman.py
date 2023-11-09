import pygame
import random
import copy
from pygame.locals import(RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, K_z, K_x)

pygame.init()
WIDTH, HEIGHT = 1366, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac Man - By Tushar')

class Walls(pygame.sprite.Sprite):
    def __init__(self, a, b, c, d):
        super().__init__()
        self.id = "WALL"
        self.surf = pygame.Surface((a, b))
        self.rect = self.surf.get_rect(
            center=(c+a/2, d+b/2)
        )
        self.surf.fill((0, 0, 0))   

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.id = "PLAYER"
        self.surf = self.surf = pygame.image.load("images/pacman.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(30, 190)
        )
        self.restate = self.rect
    def update(self, pressed_keys):
        self.restate = copy.deepcopy(self.rect)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

    def balance(self,  out_of_bond):
        if player.rect.top < out_of_bond[-1].rect.top:
            player.rect.top = player.restate[1]
        if player.rect.bottom > out_of_bond[-1].rect.bottom:
            player.rect.bottom = player.restate[1] + 25
        if player.rect.left < out_of_bond[-1].rect.left:
            player.rect.left = player.restate[0]
        if player.rect.right > out_of_bond[-1].rect.right:
            player.rect.right = player.restate[0] + 25
        if len(out_of_bond) > 1: out_of_bond.pop(0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.id = "ENEMY"
        self.surf = pygame.image.load("images/penemy.png").convert_alpha()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(1366, 195)
        )
        self.motion = [-1, 0]
        self.mlist = [] # Component of motion changing
        self.mlistbool = True

    def update(self, sprites):
        self.rect.move_ip(self.motion)
        for sprite in sprites:
            if sprite.id == "WALL":
                dup = copy.deepcopy(self.rect)
                dup[2] = 50; dup[3] = 50
                dup[0] = dup[0] - 15; dup[1] = dup[1] - 15
                self.mlist.append(bool(sprite.rect.contains(dup)))
        if self.mlistbool:
            if self.mlist.count(True) == 2:
                self.motion = random.choice([[0, 1], [1, 0], [-1, 0], [0, -1]])
                self.mlistbool = False
        if self.mlist.count(True) == 1:
            self.mlistbool = True
        self.mlist.clear()

        if self.rect.top <= 0:
            self.motion = [0, 1]
        if self.rect.left < 0:
            self.motion = [1, 0]
        if self.rect.right > WIDTH:
            self.motion = [-1, 0]
        if self.rect.bottom >= HEIGHT:
            self.motion = [0, -1]

class Points(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.id = "POINT"
        self.surf = pygame.Surface((10, 10))
        self.rect = self.surf.get_rect(
            center=(x, y)
        )
        self.surf.fill((255, 255, 255))


clock = pygame.time.Clock()
allsprite = pygame.sprite.Group()
pointsprite = pygame.sprite.Group() # For collision detection
enemies = pygame.sprite.Group()
for i in range(170, 531, 180):
    allsprite.add(Walls(1366, 50, 0, i))
    for j in range(136, 1360, 1360):
        point = Points(j, i + 25)
        allsprite.add(point)
        pointsprite.add(point)

for i in range(200, 1201, 200):
    allsprite.add(Walls(50, 700, i, 0))
    for j in range(70, 700, 70):
        point = Points(i + 25, j)
        allsprite.add(point)
        pointsprite.add(point)

for en in range(10):
    new_enemy = Enemy()
    enemies.add(new_enemy)
    allsprite.add(new_enemy)

run = True
out_of_bond = []
player = Player()
allsprite.add(player)

while run:
    for events in pygame.event.get():
        if events.type == QUIT:
            run = False
    screen.fill((0, 128, 0))

    for sprite in allsprite:
        if sprite.rect.contains(player.rect) and sprite.id == "WALL":
            out_of_bond.append(sprite)
    player.balance(out_of_bond)
    for sprite in allsprite:
        screen.blit(sprite.surf, sprite.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        run = False
    if pygame.sprite.spritecollideany(player, pointsprite):
        pcollided = pygame.sprite.spritecollide(player, pointsprite, True)
    if not pointsprite:
        run = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update(allsprite)
    pygame.display.flip()
    clock.tick(100)
pygame.quit()
