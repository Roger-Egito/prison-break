import pygame
from data.config import window

class Sound_sphere(pygame.sprite.Sprite):
    def __init__(self, groups, min_radius=25, max_radius=300, origin=(window.width/2, window.height/2), speed=5):
        super().__init__(groups)
        self.min_radius = min_radius
        self.radius = min_radius
        self.max_radius = max_radius
        self.origin = origin
        self.speed = speed

    def update(self, speed=0):
        self.radius += speed if speed else self.speed
        pygame.draw.circle(window.display, (255, 255, 255, min(255, max(1, round(self.max_radius/3)))), self.origin, self.radius, width=2, )
        if self.radius >= self.max_radius:
            self.kill()
