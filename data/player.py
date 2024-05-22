from data.sprite import Sprite
from data.config import window
import pygame

class Player(Sprite):
    def allow_movement(self):
        self.state = self.States.IDLE
        if (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]) and not (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]):
            if self.rect.right >= window.width:
                self.set_right(window.width)
            else:
                if not self.jumping: self.state = self.States.WALKING
                self.move_right()
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.jumping: self.state = self.States.RUNNING
                    self.move_right(self.speed)
        if (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]) and not (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]):
            if self.rect.left <= 0:
                self.set_left(0)
            else:
                if not self.jumping: self.state = self.States.WALKING
                self.move_left()
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.jumping: self.state = self.States.RUNNING
                    self.move_left(self.speed)
        if self.jumping is False:
            if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE]:
                self.jumping = True
                self.jump()
        else:
            self.state = self.States.JUMPING
        if pygame.key.get_pressed()[pygame.K_DOWN] or (pygame.key.get_mods() & pygame.KMOD_CTRL):
            if self.jumping is False and not ((pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]) or (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d])):
                self.state = self.States.CROUCHING
            self.move_down()