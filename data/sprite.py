import pygame
from data.spritesheet___ignore___ import spritesheet
from data.config import render, delta, window, gravity
from data.anim import Anim


class Sprite:
    class States:
        IDLE = 'IDLE'
        WALKING = 'WALKING'
        JUMPING = 'JUMPING'
        FALLING = 'FALLING'
        RUNNING = 'RUNNING'
        CROUCHING = 'CROUCHING'

    def __init__(
            self,
            img='',
            sheet=True,
            has_alpha=True,
            x=0,
            y=0,
            size_mult=1.5,
            speed=125,
            flipped=False,
            sheet_sprite_dimensions=(4, 14, 20, 34),
            sheet_image_count=4,
            sheet_step=1,
            sheet_colorkey=None):

        self.img = pygame.image.load(img).convert_alpha() if has_alpha else pygame.image.load(img).convert()
        self.anim = Anim()

        if sheet:
            self.anim.idle = self.anim.populate(img, sheet_sprite_dimensions, sheet_image_count, sheet_step, has_alpha, sheet_colorkey)
            self.img = self.anim.idle[0]

        #self.img_sheet = pygame.image.load(img_sheet).convert_alpha() if has_alpha else pygame.image.load(img_sheet).convert() #spritesheet('assets/Characters/2 Punk/Punk_idle.png').image_at((0, 0, 48, 48)) #pygame.image.load(img).convert_alpha() if has_alpha else pygame.image.load(img).convert()
        self.has_alpha = has_alpha
        self.x = x
        self.y = y
        self.default_x = x
        self.default_y = y
        self.size_mult = size_mult
        self.flipped = flipped
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.change_size(size_mult)

        self.speed = speed

        self.jumping = False
        self.jump_height = 3000

        self.fall_speed = 0

        self.state = self.States.IDLE

    @property
    def center(self):
        center = (self.x + self.center_width, self.y + self.center_height)
        return center

    @property
    def default_coords(self):
        return (self.default_x, self.default_y)

    @property
    def center_width(self):
        return round(self.width / 2)

    @property
    def center_height(self):
        return round(self.height / 2)

    @property
    def center_x(self):
        return round(self.x + self.width / 2)

    @property
    def center_y(self):
        return round(self.y + self.height / 2)

    @property
    def width(self):
        return self.img.get_width()
    
    @property
    def height(self):
        return self.img.get_height()

    @property
    def bottom(self):
        return self.y + self.height

    def set_center(self, coordinate):
        self.x = coordinate[0] - round(self.width / 2)
        self.y = coordinate[1] - round(self.height / 2)

    def set_bottom(self, y):
        self.y = y - self.height

    def set_top(self, y):
        self.y = y

    def set_left(self, x):
        self.x = x

    def set_right(self, x):
        self.x = x - self.width

    def horizontal_flip(self):
        self.img = pygame.transform.flip(self.img, 1, 0)

    def change_size(self, size_mult):
        self.img = pygame.transform.scale_by(self.img, size_mult)
        self.size_mult = size_mult
        self.update_rect_size()

    def change_image(self, img):
        self.img = pygame.transform.scale_by(img, self.size_mult)
        if self.flipped:
            self.horizontal_flip()
        self.update_rect_size()

    def move(self, vector_x=0, vector_y=0, flippable=True):

        if flippable and vector_x < 0 and self.flipped is False:
            self.horizontal_flip()
            self.flipped = True
        elif flippable and vector_x > 0 and self.flipped:
            self.horizontal_flip()
            self.flipped = False

        self.x += vector_x * delta.time()
        self.y += vector_y * delta.time()
        self.update_rect_coords()


    def move_right(self, dist=0):
        if dist:
            self.move(vector_x=dist)
        else:
            self.move(vector_x=self.speed)

    def move_left(self, dist=0):
        if dist:
            self.move(vector_x=-dist)
        else:
            self.move(vector_x=-self.speed)

    def move_up(self, dist=0):
        if dist:
            self.move(vector_y=-dist)
        else:
            self.move(vector_y=-self.speed)

    def move_down(self, dist=0):
        if dist:
            self.move(vector_y=dist)
        else:
            self.move(vector_y=self.speed)

    def jump(self, dist=0):
        if dist:
            self.y -= dist * delta.time()
        else:
            self.y -= 1
            self.fall_speed -= (self.jump_height * self.height) / 500 # * delta.time()
        if not self.flipped:
            self.x -= 14
        self.rect.y = round(self.y)


    def gravity(self, strength=0):

        if self.bottom < window.height - 32:
                self.fall_speed += strength * delta.time() if strength else 600 * delta.time()
                if self.fall_speed > gravity.fall_speed_ceil:
                    self.fall_speed = gravity.fall_speed_ceil
                self.y += self.fall_speed * delta.time()

        # Pseudo-floor. Delete later
        elif self.bottom > window.height - 32:
            self.jumping = False
            self.set_bottom(window.height - 32)
        elif self.bottom == window.height - 32:
            if self.jumping and not self.flipped:
                self.x += 14
            self.jumping = False
            self.fall_speed = 0
        self.rect.y = round(self.y)


    def update_rect_coords(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def update_rect_size(self):
        self.rect.width = round(self.width)
        self.rect.height = round(self.height)

    def render(self):
        render(self.img, self.rect)
