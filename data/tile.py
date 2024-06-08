import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, coords, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=coords)

    def update(self, step):
        self.rect.x += step
