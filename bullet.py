import pygame
import math

size = (450, 600)


class Ordinary_Bullet(pygame.sprite.Sprite):
    def __init__(self, position, image, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            # or self.rect.left<0 or self.rect.right >self.rect.width
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Bounce_Bullet(pygame.sprite.Sprite):
    def __init__(self, position, image, speed, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = speed
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.dir = angle
        self.cur_dir = angle

    def move(self):
        self.rect.top -= self.speed * math.sin(self.cur_dir)
        print(math.sin(self.cur_dir))
        print(self.rect.top)
        #
        self.rect.left += self.speed * math.cos(self.cur_dir)
        if self.rect.top < 0:
            print("change", self.cur_dir, self.dir)
            self.cur_dir = self.dir
            # or self.rect.left<0 or self.rect.right >self.rect.width
            self.active = False

        if self.rect.left < 0 or self.rect.right > size[0]:
            self.cur_dir = math.pi - self.cur_dir

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True
        self.cur_dir = self.dir
