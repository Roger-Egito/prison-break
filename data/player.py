from data.sprite import Sprite
from data.config import window, delta
import pygame


class Player(Sprite):
    slide_tick_counter = 0
    slide_delay = 0.5
    can_slide = True

    def block_right_border(self):
        beyond_border = self.collision.right >= window.width
        if beyond_border:
            self.set_right(window.width)
        return beyond_border

    def block_left_border(self):
        beyond_border = self.collision.left <= 0
        if beyond_border:
            self.set_left(0)
        return beyond_border

    def state_control(self):
        if self.crouching:
            self.state = self.States.CROUCHING
        elif self.vector_y < 0:
            self.state = self.States.JUMPING
        elif self.vector_y > 0:
            self.state = self.States.FALLING
        elif self.vector_x != 0:
            if self.sprinting:
                self.state = self.States.RUNNING
            else:
                self.state = self.States.WALKING
        else:
            self.state = self.States.IDLE

    def allow_movement(self):
        pressing_right = (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d])
        pressing_left = (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a])
        pressing_up = pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_w]
        pressing_down = pygame.key.get_pressed()[pygame.K_DOWN] or (pygame.key.get_mods() & pygame.KMOD_CTRL) or pygame.key.get_pressed()[pygame.K_s]
        pressing_shift = pygame.key.get_mods() & pygame.KMOD_SHIFT

        self.sprinting = pressing_shift
        self.airborne = self.vector_y != 0

        airborne = self.airborne
        crouching = self.crouching
        crawling = crouching and not airborne
        sprinting = self.sprinting
        sliding = self.sliding
        can_slide = self.can_slide

        idle = (not pressing_right and not pressing_left and not pressing_up and not pressing_down and not airborne)

        if idle:
            self.vector_x = 0
            #self.vector_y = 0
            self.stand()
        else:
            # ----------------------------------------------------------------------------------------------------------
            # DIRECTIONS

            if pressing_right and not pressing_left:
                vector_x = self.speed
                if sprinting:
                    vector_x *= 2
                if crawling:
                    vector_x /= 2
                self.move_right(vector_x)
                self.block_right_border()

            elif pressing_left and not pressing_right:
                vector_x = -self.speed
                if sprinting:
                    vector_x *= 2
                if crawling:
                    vector_x /= 2
                self.move_right(vector_x)
                self.block_left_border()

            elif pressing_right and pressing_left:
                self.vector_x = 0

            # ----------------------------------------------------------------------------------------------------------
            # JUMP

            if pressing_up:
                if not airborne:
                        self.airborne = True
                        self.jump()

            # ----------------------------------------------------------------------------------------------------------
            # CROUCH / SLIDE

            if pressing_down:
                self.crouch()
                if airborne:
                    self.vector_y += self.speed * 10 * delta.time()
                elif sprinting and can_slide:
                    if pressing_right or sliding == 1:
                        if not sliding:
                            self.slide_fx()
                        self.sliding = 1
                        self.move_right(self.speed * 2)
                        self.block_right_border()
                        self.slide_tick_counter += delta.time()
                    elif pressing_left or sliding == -1:
                        if not sliding:
                            self.slide_fx()
                        self.sliding = -1
                        self.move_left(self.speed * 2)
                        self.block_left_border()
                        self.slide_tick_counter += delta.time()
                    else:
                        self.can_slide = False
                    if self.slide_tick_counter >= 0.3:
                        self.can_slide = False
                        self.sliding = False
                        self.slide_tick_counter = 0
                else:
                    self.can_slide = False
            else:
                self.can_slide = True
                self.sliding = False
                self.stand()
                self.slide_tick_counter = 0
