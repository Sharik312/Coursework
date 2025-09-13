import pygame
from main import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, width, height, vel, direction, pos):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(red)
        self.rect = self.image.get_rect(center=pos)
        self.vel = vel

        self.direction = direction


    def update(self):
        if self.rect.x < 0 or self.rect.x > WIN_WIDTH or self.rect.y < 0 or self.rect.y > WIN_HEIGHT:
            self.kill()

        self.rect.x += self.vel*self.direction