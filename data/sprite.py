import pygame
from data.config import render, delta
from data.stage import *
from data.anim import Anim
from data.collision import Collision
from data.audio import *
import copy

class Sprite:
    class States:
        IDLE = 'IDLE'
        WALKING = 'WALKING'
        JUMPING = 'JUMPING'
        S_JUMPING = 'S_JUMPING'
        FALLING = 'FALLING'
        C_FALLING = 'C_FALLING'
        RUNNING = 'RUNNING'
        CROUCHING = 'CROUCHING'
        HANGING = 'HANGING'
        H_CROUCHING = 'H_CROUCHING'
        H_WALKING = 'H_WALKING'
        H_FALLING = 'H_FALLING'
        H_JUMPING = 'H_JUMPING'
        H_J_FALLING = 'H_J_FALLING'
        H_C_WALKING = 'H_C_WALKING'

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
            jump_height=4.75,
            affected_by_gravity=True,
            has_collision=True):

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
        self.x_speed_limit = 300
        self.y_speed_limit = 600

        self.airborne = False
        self.crouching = False
        self.sprinting = False
        self.climbing = False
        self.sliding = False
        self.swimming = False
        self.flying = False
        self.hanging = False
        self.jump_height = jump_height
        self.jump_mult = jump_mult
        self.affected_by_gravity = affected_by_gravity
        self.has_collision = has_collision

        self.state = self.States.IDLE
        self.last_state = self.States.IDLE
        self.stored_state = self.States.IDLE
        self.state_change_counter = 0

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
    def vxdt(self):
        return self.vector_x * delta.time()

    @property
    def vydt(self):
        return self.vector_y * delta.time()

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

    def set_top(self, position):
        self.y = position - (self.collision.top - self.rect.top)
        self.update_rect_y()

    def set_right(self, position):
        self.x = (position - self.width) + (self.rect.right - self.collision.right)
        self.update_rect_x()

    def set_bottom(self, position):
        self.y = (position - self.height) + (self.rect.bottom - self.collision.bottom)
        self.update_rect_y()

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

    def move(self, hor_speed=0, ver_speed=0, flippable=True):

        if flippable and hor_speed < 0 and self.flipped is False:
            self.horizontal_flip()
            self.x -= self.width / 2
            self.flipped = True
            self.collision.flipped = True
        elif flippable and hor_speed > 0 and self.flipped:
            self.horizontal_flip()
            self.x += self.width / 2
            self.flipped = False
            self.collision.flipped = False

        if hor_speed:
            self.vector_x = hor_speed
            self.x += self.vxdt

            self.update_rect_position()

            if hor_speed > 0:
                self.check_collision_right(stage.tile_group)
            else:
                self.check_collision_left(stage.tile_group)

        if ver_speed:
            self.vector_y += ver_speed  # VECTORS SHOULD NOT HAVE DELTA.TIME! THEY PERSIST BETWEEN FRAMES

            if abs(self.vector_y) > self.y_speed_limit:
                self.vector_y = self.y_speed_limit if self.vydt > 0 else -self.y_speed_limit

            self.y += self.vydt
            self.update_rect_position()
            if self.vector_y > 0:
                self.check_collision_down(stage.tile_group)
            else:
                self.check_collision_up(stage.tile_group)

    def move_left(self, dist=0):
        if dist:
            self.move(hor_speed=-dist)
        else:
            self.move(hor_speed=-self.speed)

    def move_up(self, dist=0):
        if dist:
            self.move(ver_speed=-dist)
        else:
            self.move(ver_speed=-self.speed)

    def move_right(self, dist=0):
        if dist:
            self.move(hor_speed=dist)
        else:
            self.move(hor_speed=self.speed)

    def move_down(self, dist=0):
        if dist:
            self.move(ver_speed=dist)
        else:
            self.move(ver_speed=self.speed)

# ---

    def jump(self, dist=0):
        if dist:
            pass
            #self.move(y=-dist)
        else:
            self.set_bottom(self.rect.bottom - 1)
            self.vector_y -= (self.jump_height * self.height * self.jump_mult)# * delta.time()
        self.update_rect_y()
        hit = self.check_collision_up(stage.tile_group)
        if hit:
            return True
        else:
            return False

    def apply_gravity(self, strength=0):
        if self.affected_by_gravity:
            oob_floor = 900  # out of bounds
            acceleration = strength if strength else 600 * delta.time()

            self.move_down(acceleration)

            if self.bottom > oob_floor:
                self.airborne = False
                self.vector_y = 0
                self.set_bottom(96)

# ---

    def crouch(self):
        offset = 20
        if not self.crouching:
            self.collision.height -= offset
            self.collision.rect.height -= offset
            self.collision.offset_top += offset
            self.collision.update_position()
            self.crouching = True

    def stand(self):
        offset = 20
        if self.crouching:
            cramped = False
            self.collision.height += offset
            self.collision.rect.height += offset
            self.collision.offset_top -= offset
            self.collision.update_position()

            hit_list = self.collision.get_hits(stage.tile_group)
            for tile in hit_list:
                if tile.y < self.collision.rect.y:
                    self.collision.height -= offset
                    self.collision.rect.height -= offset
                    self.collision.offset_top += offset
                    self.collision.update_position()
                    cramped = True
                    break

            if not cramped:
                #self.y -= offset
                #self.rect.y -= offset
                self.crouching = False

    #def slide(self, direction):
    #    offset = 10
    #    if not self.sliding:
    #        self.collision.height -= offset
    #        self.collision.rect.height -= offset
    #        self.collision.offset_top += offset
    #        self.collision.update_position()
    #        self.sliding = direction
#
    #def stop_slide(self):
    #    offset = 10
    #    if self.sliding:
    #        cramped = False
    #        self.collision.height += offset
    #        self.collision.rect.height += offset
    #        self.collision.offset_top -= offset
    #        self.collision.update_position()
#
    #        hit_list = self.collision.get_hits(stage.tile_group)
    #        for tile in hit_list:
    #            if tile.y < self.collision.rect.y:
    #                self.collision.height -= offset
    #                self.collision.rect.height -= offset
    #                self.collision.offset_top += offset
    #                self.collision.update_position()
    #                cramped = True
    #                break
#
    #        if not cramped:
    #            self.y += offset
    #            self.rect.y += offset
    #            self.sliding = False

# ---

    def update_rect_position(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        self.collision.update_position()

    def update_rect_x(self):
        self.rect.x = round(self.x)
        self.collision.update_x()

    def update_rect_y(self):
        self.rect.y = round(self.y)
        self.collision.update_y()

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

#    def check_collision_x(self, tiles):
#        if self.has_collision:
#            self.collision.rect.x += 1
#            collisions = self.collision.get_hits(tiles)
#            self.collision.rect.x -= 1
#            for tile in collisions:
#                #if
#                if self.vector_x > 0:
#                    self.set_right(tile.left)
#                    self.vector_x = 0
#                elif self.vector_x < 0:
#                    self.set_left(tile.right)
#                    self.vector_x = 0

    def check_collision_right(self, tiles):
        if self.has_collision:
            self.collision.rect.x += 1
            collisions = self.collision.get_hits(tiles)
            self.collision.rect.x -= 1
            for tile in collisions:
                self.set_right(tile.left)
                self.vector_x = 0

    def check_collision_left(self, tiles):
        if self.has_collision:
            self.collision.rect.x -= 1
            collisions = self.collision.get_hits(tiles)
            self.collision.rect.x += 1
            for tile in collisions:
                self.set_left(tile.right)
                self.vector_x = 0

    def check_collision_down(self, tiles):
        if self.has_collision:
            #self.set_bottom(self.rect.bottom + 1) # DOES NOT WORK. MAKES JUMPING WEIRD. ALWAYS ROUNDS Y
            self.collision.rect.y += 1
            collisions = self.collision.get_hits(tiles)
            self.collision.rect.y -= 1
            for tile in collisions:
                    self.airborne = False
                    self.set_bottom(tile.top)
                    self.vector_y = 0

    def check_collision_up(self, tiles):
        if self.has_collision:
            #self.set_bottom(self.rect.bottom + 1) # DOES NOT WORK. MAKES JUMPING WEIRD. ALWAYS ROUNDS Y
            self.collision.rect.y -= 1
            collisions = self.collision.get_hits(tiles)
            self.collision.rect.y += 1
            for tile in collisions:
                self.set_top(tile.bottom)
                self.vector_y = 0
            if len(collisions):
                return True

#    def check_collision(self, tiles):
#        sprite = self.collision.rect
#        if self.has_collision:
#            collisions = self.collision.get_hits(tiles)
#            for tile in collisions:
#                dist_up = abs(sprite.bottom - tile.top)
#                dist_down = abs(tile.bottom - sprite.top)
#                dist_right = abs(tile.right - sprite.left)
#                dist_left = abs(sprite.right - tile.left)
#                closest_direction = min(dist_up, dist_down, dist_right, dist_left)
#
#                if closest_direction == dist_up:
#                    self.vector_y = 0
#                    self.set_bottom(tile.top+1)
#                elif closest_direction == dist_down:
#                    self.vector_y = 0
#                    self.set_top(tile.bottom)
#                elif closest_direction == dist_right:
#                    self.vector_x = 0
#                    self.set_left(tile.right)
#                else:
#                    self.vector_x = 0
#                    self.set_right(tile.left)



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
                case 'C_FALLING':
                    self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1, speed_mult=3))
                case 'S_JUMPING':
                    self.change_image(self.anim.next(self.anim.s_jump, first_frame=1, last_frame=2, loop=False, step=-1))
                case 'RUNNING':
                    self.change_image(self.anim.next(self.anim.run, speed_mult=2))
                case 'CROUCHING':
                    if self.sliding:
                        self.change_image(self.anim.slide)
                    else:
                        self.change_image(self.anim.next(self.anim.crouch, first_frame=2, loop=False))
                case 'HANGING':
                    self.change_image(self.anim.next(self.anim.hang, first_frame=1, last_frame=1, loop=False))
                case 'H_CROUCHING':
                    if self.last_state == 'H_JUMPING' or self.last_state == 'H_J_FALLING':
                        self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1))
                    else:
                        self.change_image(self.anim.next(self.anim.h_c_walk, first_frame=1, step=0))
                case 'H_WALKING':
                    self.change_image(self.anim.next(self.anim.h_walk, last_frame=1))
                case 'H_C_WALKING':
                    self.change_image(self.anim.next(self.anim.h_c_walk))
                case 'H_FALLING':
                    self.change_image(self.anim.next(self.anim.h_fall, first_frame=4, loop=False))
                case 'H_JUMPING':
                    #self.change_image(self.anim.next(self.anim.h_jump, first_frame=1, last_frame=1, loop=False))
                    self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1))
                case 'H_J_FALLING':
                    self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1))

            #self.anim_tick_counter = 0

    def slide_fx(self):
        play_sfx('assets/audio/sfx/slide.ogg')


# ---

    def render(self):
        render(self.img, self.rect)
