import pygame
import random
import time
import math
from random import *


class Enemy_1(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
                pygame.image.load("images/enemy1_down1.png").convert_alpha(),
                pygame.image.load("images/enemy1_down2.png").convert_alpha(),
                pygame.image.load("images/enemy1_down3.png").convert_alpha(),
                pygame.image.load("images/enemy1_down4.png").convert_alpha()
        ])
        self.image_size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.active = True
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-5 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.time = 0
        self.angel = 0

    def move(self):
        if self.rect.top < self.height:
            if self.time % 30 == 0:
                self.angle = uniform(0, 10) % math.pi
            # print(self.height,self.width)
            self.rect.top += self.speed * math.sin(self.angle)
            if (self.rect.right + self.speed * math.cos(
                    self.angle) > self.width or self.rect.left + self.speed * math.cos(self.angle) < 0):
                self.angle = math.pi - self.angle
            self.rect.left += self.speed * math.cos(self.angle)
            self.time += 1
            return False
        else:
            self.reset()
            return True

    def reset(self):
        self.active = True
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-5 * self.height, 0)


class Enemy_2(pygame.sprite.Sprite):
    energy = 8  # 血量

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
                pygame.image.load("images/enemy2_down1.png").convert_alpha(),
                pygame.image.load("images/enemy2_down2.png").convert_alpha(),
                pygame.image.load("images/enemy2_down3.png").convert_alpha(),
                pygame.image.load("images/enemy2_down4.png").convert_alpha()
        ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-10 * self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.energy = Enemy_2.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
            return False
        else:
            self.reset()
            return True

    def reset(self):
        self.active = True
        self.energy = Enemy_2.energy
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-10 * self.height, -self.height)


class Enemy_3(pygame.sprite.Sprite):
    energy = 50

    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.image_hit = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([
                pygame.image.load("images/enemy3_down1.png").convert_alpha(),
                pygame.image.load("images/enemy3_down2.png").convert_alpha(),
                pygame.image.load("images/enemy3_down3.png").convert_alpha(),
                pygame.image.load("images/enemy3_down4.png").convert_alpha(),
                pygame.image.load("images/enemy3_down5.png").convert_alpha(),
                pygame.image.load("images/enemy3_down6.png").convert_alpha()
        ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-15 * self.height, -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image1)
        self.energy = Enemy_3.energy
        self.hit = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
            return False
        else:
            self.reset()
            return True

    def reset(self):
        self.active = True
        self.energy = Enemy_3.energy
        self.rect.left = randint(0, self.width - self.rect.width)
        self.rect.top = randint(-15 * self.height, -5 * self.height)
