from data.sprite import Sprite
from data.config import window
import pygame

class Player(Sprite):
    def allow_movement(self):
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not pygame.key.get_pressed()[pygame.K_LEFT]:
            if self.rect.right >= window.width:
                self.set_right(window.width)
            else:
                self.move_right()
        if pygame.key.get_pressed()[pygame.K_LEFT] and not pygame.key.get_pressed()[pygame.K_RIGHT]:
            if self.rect.left <= 0:
                self.set_left(0)
            else:
                self.move_left()
        if self.jumping is False:
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.jumping = True
                self.jump()
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.move_down()