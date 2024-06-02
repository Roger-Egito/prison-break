import pygame
from data.config import render, delta, stage, terminal_velocity
from data.anim import Anim
from data.collision import Collision
from data.audio import *
import copy

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
            sheet_sprite_dimensions=(0, 0, 48, 48),
            sheet_image_count=4,
            sheet_step=1,
            sheet_colorkey=None,
            collision_offset=(0,0),
            collision_dimensions=(0, 0),
            jump_mult=1,
            jump_height=4.2,
            affected_by_gravity=True):

        self.img = pygame.image.load(img).convert_alpha() if has_alpha else pygame.image.load(img).convert()
        self.anim = Anim()

        if sheet:
            self.anim.idle = self.anim.populate(img, sheet_sprite_dimensions, sheet_image_count, sheet_step, has_alpha, sheet_colorkey)
            self.img = self.anim.idle[0]

        self.has_alpha = has_alpha
        self.x = x
        self.y = y
        self.default_x = x
        self.default_y = y
        self.size_mult = size_mult
        self.flipped = flipped
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collision = Collision(x=self.rect.x + collision_offset[0], y=self.rect.y + collision_offset[1], size_mult=size_mult, flipped=flipped, offset=collision_offset, dimensions=collision_dimensions, anchor=self.rect)
        self.change_size(size_mult)

        self.speed = speed
        self.vector_x = 0
        self.vector_y = 0

        self.airborne = False
        self.crouching = False
        self.sprinting = False
        self.climbing = False
        self.sliding = False
        self.swimming = False
        self.jump_height = jump_height
        self.jump_mult = jump_mult
        self.affected_by_gravity = affected_by_gravity

        self.state = self.States.IDLE

    # ---

    @property
    def coords(self):
        coords = (self.x, self.y)
        return coords

    @property
    def default_coords(self):
        coords = (self.default_x, self.default_y)
        return coords

    # ---

    @property
    def width(self):
        return self.img.get_width()

    @property
    def height(self):
        return self.img.get_height()

    # ---

    @property
    def center(self):
        center = (self.center_x, self.center_y)
        return center

    @property
    def center_width(self):
        return round(self.width / 2)

    @property
    def center_height(self):
        return round(self.height / 2)

    @property
    def center_x(self):
        return round(self.x + self.center_width)

    @property
    def center_y(self):
        return round(self.y + self.center_height)

    def set_center(self, coordinate):
        self.x = coordinate[0] - round(self.width / 2)
        self.y = coordinate[1] - round(self.height / 2)

    # ---

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    def set_left(self, position):
        self.x = position - (self.collision.left - self.rect.left)
        self.update_rect_x()
        self.update_collision_x()

    def set_top(self, position):
        self.y = position - (self.collision.top - self.rect.top)

    def set_right(self, position):
        self.x = (position - self.width) + (self.rect.right - self.collision.right)
        self.update_rect_x()
        self.update_collision_x()

    def set_bottom(self, position):
        self.y = (position - self.height) + (self.rect.bottom - self.collision.bottom)

# ---

    def horizontal_flip(self):
        self.img = pygame.transform.flip(self.img, 1, 0)

    def change_image(self, img):
        self.img = pygame.transform.scale_by(img, self.size_mult)
        if self.flipped:
            self.horizontal_flip()
        self.update_rect_size()

    def change_size(self, size_mult):
        self.img = pygame.transform.scale_by(self.img, size_mult)
        self.size_mult = size_mult
        self.update_rect_size()

# ---

    def move(self, x=0, y=0, flippable=True):

        if flippable and x < 0 and self.flipped is False:
            self.horizontal_flip()
            self.x -= self.width / 2
            self.flipped = True
        elif flippable and x > 0 and self.flipped:
            self.horizontal_flip()
            self.x += self.width / 2
            self.flipped = False

        if x:
            self.vector_x = x * delta.time()
            self.x += self.vector_x
        if y:
            self.vector_y = y * delta.time()
            self.y = self.vector_y

        self.update_rect_position()

    def move_left(self, dist=0):
        if dist:
            self.move(x=-dist)
        else:
            self.move(x=-self.speed)

    def move_up(self, dist=0):
        if dist:
            self.move(y=-dist)
        else:
            self.move(y=-self.speed)

    def move_right(self, dist=0):
        if dist:
            self.move(x=dist)
        else:
            self.move(x=self.speed)

    def move_down(self, dist=0):
        if dist:
            self.move(y=dist)
        else:
            self.move(y=self.speed)

# ---

    def jump(self, dist=0):
        if dist:
            self.move(y=-dist)
        else:
            self.y -= 1
            self.vector_y -= (self.jump_height * self.height * self.jump_mult) # * delta.time()
        self.rect.y = round(self.y)

    def apply_gravity(self, strength=0):
        oob_floor = 900  # out of bounds

        self.vector_y += strength * delta.time() if strength else 600 * delta.time()
        if self.vector_y > terminal_velocity:
            self.vector_y = terminal_velocity
        self.y += self.vector_y * delta.time()

        if self.bottom > oob_floor:
            self.airborne = False
            self.vector_y = 0
            self.set_bottom(96)

        hit_list = self.collision.test(stage.tile_group)
        if len(hit_list) > 0:
            self.airborne = False
            self.set_bottom(hit_list[0].top+1)
            self.vector_y = 0

        self.rect.y = round(self.y)

# ---

    def crouch(self):
        offset = 10
        if not self.crouching:
            self.collision.height -= offset
            self.collision.rect.height -= offset
            self.collision.offset_top += offset
            self.crouching = True

    def stand(self):
        offset = 10
        if self.crouching:
            self.collision.height += offset
            self.collision.rect.height += offset
            self.collision.offset_top -= offset
            self.y += offset
            self.rect.y += offset
            self.crouching = False

# ---

    def update_rect_position(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def update_rect_x(self):
        self.rect.x = round(self.x)

    def update_rect_y(self):
        self.rect.y = round(self.y)

    def update_rect_size(self):
        self.rect.width = round(self.width)
        self.rect.height = round(self.height)

# ---

    def update_collision(self):
        if self.size_mult != self.collision.size_mult:
            self.collision.size_mult = self.size_mult
            self.collision.update_offset()
            self.collision.update_size()

        self.collision.anchor = self.rect
        self.collision.flipped = self.flipped
        self.collision.update_position()

    def update_collision_position(self):
        self.collision.update_position()

    def update_collision_x(self):
        self.collision.update_x()

    def update_collision_y(self):
        self.collision.update_y()

    #def update_collision_size(self):
    #    self.collision.width *= self.size_mult
    #    self.collision.height *= self.size_mult
    #    self.collision.rect.width = round(self.collision.width)
    #    self.collision.rect.height = round(self.collision.height)

# ---
    
    def animate(self):
            match self.state:
                case 'IDLE':
                    self.change_image(self.anim.next(self.anim.idle))
                case 'WALKING':
                    self.change_image(self.anim.next(self.anim.walk))
                case 'JUMPING' | 'FALLING':
                    self.change_image(self.anim.next(self.anim.jump))
                case 'RUNNING':
                    self.change_image(self.anim.next(self.anim.run, speed_mult=2))
                case 'CROUCHING':
                    self.change_image(self.anim.next(self.anim.crouch, first_frame=2, loop=False))
            #self.anim_tick_counter = 0

    def slide_fx(self):
        play_sfx('assets/audio/sfx/slide.ogg')


# ---

    def render(self):
        render(self.img, self.rect)
