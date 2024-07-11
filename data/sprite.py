import random

import pygame
from data.config import render, delta
from data.stage import stage
from data.group import Group
from data.anim import Anim
from data.collision import Collision
from data.audio import *
from data.hearing import *
import copy

class Sprite(pygame.sprite.Sprite):
    class States:                           # H = Hanging / C = Crouching / S = Standing (idle) / J = Jumping
        IDLE = 'IDLE'
        HANGING = 'HANGING'
        CROUCHING = 'CROUCHING'
        RUNNING = 'RUNNING'
        H_CROUCHING = 'H_CROUCHING'
        WALKING = 'WALKING'
        H_WALKING = 'H_WALKING'
        C_WALKING = 'C_WALKING'
        C_RUNNING = 'C_RUNNING'
        HC_WALKING = 'HC_WALKING'
        JUMPING = 'JUMPING'
        S_JUMPING = 'S_JUMPING'
        H_JUMPING = 'H_JUMPING'
        FAST_JUMPING = 'FAST_JUMPING'
        FALLING = 'FALLING'
        C_FALLING = 'C_FALLING'
        H_FALLING = 'H_FALLING'
        HJ_FALLING = 'HJ_FALLING'
        F_BACKFLIP = 'F_BACKFLIP'
        ROLLING = 'ROLLING'

    class AIs:
        SOLDIER = 'SOLDIER'


    def __init__(
            self,
            img='',
            sheet=True,
            has_alpha=True,
            name='',
            type='',
            x=0,
            y=0,
            size_mult=1.5,
            speed=125,
            speed_mult=1,
            flipped=False,
            sheet_sprite_dimensions=(0, 0, 48, 48),
            sheet_image_count=4,
            sheet_step=1,
            sheet_colorkey=None,
            collision_offset=(0,0),
            collision_dimensions=(0, 0),
            jump_mult=1,
            #jump_height=4.75,
            jump_height=5.00,
            affected_by_gravity=True,
            has_collision=True,
            multiple_idles=False,
            light_radius=5,
            groups=[]):

        super().__init__(groups)
        self.img = pygame.image.load(img).convert_alpha() if has_alpha else pygame.image.load(img).convert()
        self.anim = Anim()

        if sheet:
            self.anim.idle = self.anim.populate(img, sheet_sprite_dimensions, sheet_image_count, sheet_step, has_alpha, sheet_colorkey)
            self.img = self.anim.idle[0]

        self.has_alpha = has_alpha
        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.default_x = x
        self.default_y = y
        self.size_mult = size_mult
        self.flipped = flipped
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.collision = Collision(x=self.rect.x + collision_offset[0], y=self.rect.y + collision_offset[1], size_mult=size_mult, flipped=flipped, offset=collision_offset, dimensions=collision_dimensions, anchor=self.rect)
        self.vision = Collision(anchor=self.collision.rect, x=self.collision.rect.x, y=self.collision.rect.y, offset=(self.width / 3, self.height / 2), size_mult=self.size_mult, flipped=self.flipped, dimensions=(self.collision.rect.width + 96, self.collision.rect.height - 16))
        self.change_size(size_mult)

        self.speed = speed
        self.speed_mult = speed_mult
        self.vector_x = 0
        self.vector_y = 0
        self.x_speed_limit = 300
        self.y_speed_limit = 600
        self.last_x_direction = 0
        self.last_y_direction = 0

        self.airborne = False
        self.crouching = False
        self.sprinting = False
        self.climbing = False
        self.sliding = False
        self.swimming = False
        self.flying = False
        self.hanging = False
        self.rolling = False
        self.on_wall = False
        self.cramped = False
        self.immortal = False
        self.jump_height = jump_height
        self.jump_mult = jump_mult
        self.affected_by_gravity = affected_by_gravity
        self.has_collision = has_collision

        self.state = self.States.IDLE
        self.last_state = self.States.IDLE
        self.stored_state = self.States.IDLE
        self.state_change_counter = 0

        self.multiple_idles = multiple_idles
        self.idle_tick_counter = 0
        self.idle_delay = 10

        self.sound_spheres = Group()

        self.step_tick_counter = 0
        self.step_delay = 0.5

        self.light_radius = light_radius

        self.hca = True        # Has Collision Attribute

        self.close_to_interactive = False

    # ---

    @property
    def coords(self):
        coords = (self.x, self.y)
        return coords

    @property
    def default_coords(self):
        coords = (self.default_x, self.default_y)
        return coords

    def set_coords(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.update_rect_position()

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

    def set_bottomleft(self, coords):
        self.x = coords[0] - (self.collision.left - self.rect.left)
        self.y = (coords[1] - self.height) + (self.rect.bottom - self.collision.bottom)
        self.update_rect_position()

    def set_midbottom(self, coords):
        self.x = coords[0] - round(self.width / 2)
        self.y = (coords[1] - self.height) + (self.rect.bottom - self.collision.bottom)
        self.update_rect_position()

    def set_bottomright(self, coords):
        self.x = (coords[0] - self.width) + (self.rect.right - self.collision.right)
        self.y = (coords[1] - self.height) + (self.rect.bottom - self.collision.bottom)
        self.update_rect_position()

    def set_midtop(self, coords):
        self.x = coords[0] - round(self.width / 2)
        self.y = coords[1] - (self.collision.top - self.rect.top)
        self.update_rect_position()

# ---

    def horizontal_flip(self):
        self.img = pygame.transform.flip(self.img, 1, 0)

    def vertical_flip(self):
        self.img = pygame.transform.flip(self.img, 0, 1)

    def rotate_around_center(self, angle):
        # tentar solução de compensar a posição com a diferença de tamanho
        wi = self.img.get_width()
        hi = self.img.get_height()

        rotimg = pygame.transform.rotate(self.img, angle)
        diffx = rotimg.get_width() - wi
        diffy = rotimg.get_height() - hi
        rotimg.get_rect().x -= diffx
        rotimg.get_rect().y -= diffy
        self.img = rotimg
        self.update_rect_position()
        if not self.flipped:
            self.rect.x -= diffx
            self.rect.y -= diffy


    def rotate(self, angle):
        self.img = pygame.transform.rotate(self.img, angle)
        #self.img = pygame.transform.rotozoom(self.img, angle, 1)
        new_rect = self.img.get_rect()
        new_rect.x = self.rect.x
        new_rect.y = self.rect.y
        self.rect = new_rect
        #self.update_rect_size()
        self.update_rect_position()

    def change_image(self, img):
        self.img = pygame.transform.scale_by(img, self.size_mult)
        #self.img = pygame.transform.rotate(self.img, 45)
        if self.flipped:
            self.horizontal_flip()
        self.update_rect_size()

    def change_size(self, size_mult):
        self.img = pygame.transform.scale_by(self.img, size_mult)
        self.size_mult = size_mult
        self.update_rect_size()

# ---

    def force_move(self, hor_speed=0, ver_speed=0):
        if hor_speed:
            self.x += hor_speed * delta.time()
            #self.rect.x += hor_speed * delta.time()
        if ver_speed:
            self.y += ver_speed * delta.time()
            #self.rect.y += ver_speed * delta.time()
        self.update_rect_position()


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
            self.vector_x = hor_speed * self.speed_mult
            self.x += self.vxdt

            self.update_rect_position()

            if hor_speed > 0:
                self.last_x_direction = 1
                return self.check_collision_right(stage.collision_group)
            else:
                self.last_x_direction = -1
                return self.check_collision_left(stage.collision_group)

        if ver_speed:
            self.vector_y += ver_speed  # VECTORS SHOULD NOT HAVE DELTA.TIME! THEY PERSIST BETWEEN FRAMES

            if abs(self.vector_y) > self.y_speed_limit:
                self.vector_y = self.y_speed_limit if self.vydt > 0 else -self.y_speed_limit

            self.y += self.vydt
            self.update_rect_position()
            if self.vector_y > 0:
                self.last_y_direction = 1
                return self.check_collision_down(stage.collision_group)
            else:
                self.last_y_direction = -1
                return self.check_collision_up(stage.collision_group)

    def move_left(self, dist=0):
        if dist:
            return self.move(hor_speed=-dist)
        else:
            return self.move(hor_speed=-self.speed)

    def move_up(self, dist=0):
        if dist:
            return self.move(ver_speed=-dist)
        else:
            return self.move(ver_speed=-self.speed)

    def move_right(self, dist=0):
        if dist:
            return self.move(hor_speed=dist)
        else:
            return self.move(hor_speed=self.speed)

    def move_down(self, dist=0):
        if dist:
            return self.move(ver_speed=dist)
        else:
            return self.move(ver_speed=self.speed)

# ---

    def jump(self, dist=None):
        if dist is not None:
            pass
            self.vector_y -= (dist * self.height * self.jump_mult)# * delta.time() * 17)
        else:
            #self.set_bottom(self.rect.bottom - 1)
            self.vector_y -= (self.jump_height * self.height * self.jump_mult)# * delta.time() * 17)
        self.update_rect_y()
        hits = self.check_collision_up(stage.collision_group)
        return hits
        #if hit:
        #    return hit
        #else:
        #    return False

    def apply_gravity(self, strength=0):
        if self.affected_by_gravity:
            oob_floor = 900  # out of bounds
            acceleration = strength * delta.time() if strength else 600 * delta.time() #10

            hits = self.move_down(acceleration)

            if self.bottom > oob_floor:
                self.airborne = False
                self.vector_y = 0
                self.set_bottom(160)

            return hits

# ---

    def crouch(self):
        offset = 20
        if not self.crouching:
            self.collision.height -= offset
            self.collision.rect.height -= offset
            self.collision.offset_top += offset
            self.collision.update_position()
            if self.hanging:
                self.y -= 20
                self.update_rect_y()
            self.crouching = True


    def stand(self):
        offset = 20
        if self.crouching:
            cramped = False
            self.collision.height += offset
            self.collision.rect.height += offset
            self.collision.offset_top -= offset
            self.collision.update_position()
            if self.hanging:
                self.y += 20
                self.update_rect_y()

            hit_list = self.collision.get_hits(stage.tile_group)
            if hit_list:
                self.collision.height -= offset
                self.collision.rect.height -= offset
                self.collision.offset_top += offset
                self.collision.update_position()
                if self.hanging:
                    self.y -= 20
                    self.update_rect_y()
                cramped = True

            if not cramped:
                #self.y -= offset
                #self.rect.y -= offset
                self.crouching = False

            return cramped

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

    def update_vision(self):
        if self.size_mult != self.vision.size_mult:
            self.vision.size_mult = self.size_mult
            self.vision.update_offset()
            self.vision.update_size()

        self.vision.anchor = self.rect
        self.vision.flipped = self.flipped
        self.vision.update_position()

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

    def check_collision_right(self, tiles, *args):
        if self.has_collision:
            self.collision.rect.x += 1
            collisions = self.collision.get_hits(tiles)
            if self in collisions:
                collisions.remove(self)
            self.collision.rect.x -= 1
            for tile in collisions:
                if tile.hca:
                    self.set_right(tile.collision.rect.left)
                else:
                    self.set_right(tile.rect.left)
                self.vector_x = 0
            return collisions
        else:
            return []

    def check_collision_bottomright(self, tiles):
        if self.has_collision:
            self.collision.rect.x += 1
            self.collision.rect.y += 1
            collisions = self.collision.get_hits(tiles, coords=self.collision.rect.bottomright, point_based=True)
            self.collision.rect.x -= 1
            self.collision.rect.y -= 1
            return collisions
        else:
            return []

    def check_collision_bottomleft(self, tiles):
        if self.has_collision:
            self.collision.rect.x -= 1
            self.collision.rect.y += 1
            collisions = self.collision.get_hits(tiles, coords=self.collision.rect.bottomleft, point_based=True)
            self.collision.rect.x += 1
            self.collision.rect.y -= 1
            return collisions
        else:
            return []

    def check_collision_midbottom(self, tiles):
        if self.has_collision:
            self.collision.rect.y += 1
            collisions = self.collision.get_hits(tiles, coords=self.collision.rect.midbottom, point_based=True)
            self.collision.rect.y -= 1
            return collisions
        else:
            return []


    def check_collision_left(self, tiles=None, sprites=None):
        if self.has_collision:
            self.collision.rect.x -= 1
            collisions = self.collision.get_hits(tiles)
            if self in collisions:
                collisions.remove(self)
            self.collision.rect.x += 1
            for tile in collisions:
                if tile.hca:
                    self.set_left(tile.collision.rect.right)
                else:
                    self.set_left(tile.rect.right)
                self.vector_x = 0
            return collisions
        else:
            return []

    def check_collision_down(self, tiles):
        if self.has_collision:
            #self.set_bottom(self.rect.bottom + 1) # DOES NOT WORK. MAKES JUMPING WEIRD. ALWAYS ROUNDS Y
            self.collision.rect.y += 1
            collisions = self.collision.get_hits(tiles)
            self.collision.rect.y -= 1
            if collisions:
                self.airborne = False
                if self.vector_y >= 150:
                    if not self.crouching:
                        if self.vector_y >= 450:
                            self.crash_fx()
                        else:
                            play_sfx('fall', volume=self.vector_y/1800)
                        Sound_sphere(origin=self.collision.rect.midbottom, groups=self.sound_spheres,
                                 max_radius=abs(self.vector_y/3))
                    else:
                        play_sfx('fall', volume=self.vector_y/3600)
                        Sound_sphere(origin=self.collision.rect.midbottom, groups=self.sound_spheres,
                                 max_radius=abs(self.vector_y/6))
            for tile in collisions:
                    if tile.hca:
                        self.set_bottom(tile.collision.rect.top)
                    else:
                        self.set_bottom(tile.rect.top)
                    self.vector_y = 0
            return collisions# if len(collisions) else False
        else:
            return []

    def check_collision_up(self, tiles):
        if self.has_collision:
            #self.set_bottom(self.rect.bottom + 1) # DOES NOT WORK. MAKES JUMPING WEIRD. ALWAYS ROUNDS Y
            self.collision.rect.y -= 1
            collisions = self.collision.get_hits(tiles)
            self.collision.rect.y += 1
            for tile in collisions:
                if tile.hca:
                    self.set_top(tile.collision.rect.bottom)
                else:
                    self.set_top(tile.rect.bottom)
                #dddif not self.hanging:
                #ddd    self.vector_y = 0
            return collisions# if len(collisions) else False
        else:
            return []

    def check_collision_point(self, coords):
        return self.collision.is_hitting_point(coords)

    def check_collision_sprite(self, sprite):
        return self.collision.is_hitting_sprite(sprite)

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
                    if self.multiple_idles:
                        if self.anim.last_sheet != self.anim.idle and self.anim.last_sheet != self.anim.random_idle:
                            self.idle_tick_counter = 0

                        if self.anim.last_sheet == self.anim.idle:
                            self.idle_tick_counter += delta.time()

                            if self.idle_tick_counter >= self.idle_delay:
                                self.anim.random_idle = random.choice([self.anim.idle2, self.anim.idle3, self.anim.idle4, self.anim.idle5])
                                #self.anim.random_idle = self.anim.idle6
                                self.change_image(self.anim.next(self.anim.random_idle, loop=False, speed_mult=0.25))
                                self.idle_tick_counter = 0

                        if self.anim.last_sheet:
                            if self.anim.last_sheet == self.anim.random_idle:
                                if self.idle_tick_counter < 1:
                                    self.change_image(self.anim.next(self.anim.random_idle, loop=False, speed_mult=1))

                                if len(self.anim.random_idle) - 1 == self.anim.frame:
                                    if self.anim.random_idle == self.anim.idle5:
                                        self.change_image(self.anim.next(self.anim.random_idle, loop=False, speed_mult=1))
                                        self.idle_tick_counter -= 0.9 * delta.time()

                                    self.idle_tick_counter += delta.time()

                                    if self.idle_tick_counter >= 0.25:
                                        self.change_image(self.anim.next(self.anim.idle))
                                        self.idle_tick_counter = 0

                            else:
                                self.change_image(self.anim.next(self.anim.idle))
                    else:
                        if self.type == 'Soldier':
                            if self.alert:
                                self.change_image(self.anim.next(self.anim.idle, speed_mult=5))
                            else:
                                self.change_image(self.anim.next(self.anim.idle))
                        else:
                            self.change_image(self.anim.next(self.anim.idle))

                case 'WALKING':
                    self.change_image(self.anim.next(self.anim.walk))
                case 'JUMPING' | 'FALLING':
                    self.change_image(self.anim.next(self.anim.jump))
                case 'FAST_JUMPING':
                    self.change_image(self.anim.next(self.anim.jump, speed_mult=3))
                case 'S_JUMPING':
                    self.change_image(self.anim.next(self.anim.s_jump, first_frame=1, last_frame=2, loop=False, step=-1))
                case 'C_FALLING':
                    if self.last_state == 'H_JUMPING' or self.last_state == 'HJ_FALLING':
                        self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1))
                    else:
                        self.change_image(self.anim.next(self.anim.hc_walk, first_frame=1, step=0))
                case 'RUNNING':
                    self.change_image(self.anim.next(self.anim.run, speed_mult=2))
                case 'CROUCHING':
                    if self.sliding:
                        self.change_image(self.anim.slide)
                    else:
                        self.change_image(self.anim.next(self.anim.crouch, first_frame=2, loop=False))
                case 'C_WALKING':
                    self.change_image(self.anim.next(self.anim.c_walk))
                case 'C_RUNNING':
                    self.change_image(self.anim.next(self.anim.c_walk, speed_mult=2))
                    #self.change_image(self.anim.next(self.anim.c_walk, first_frame=1, step=4))
                    #self.change_image(self.anim.next(self.anim.c_walk, first_frame=1, step=4))
                case 'HANGING':
                    self.change_image(self.anim.next(self.anim.hang, first_frame=1, last_frame=1, loop=False))
                case 'H_CROUCHING':
                    if self.last_state == 'H_JUMPING' or self.last_state == 'HJ_FALLING':
                        self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1))
                    else:
                        self.change_image(self.anim.next(self.anim.hc_walk, first_frame=1, step=0))
                case 'H_WALKING':
                    self.change_image(self.anim.next(self.anim.h_walk, last_frame=1))
                case 'HC_WALKING':
                    self.change_image(self.anim.next(self.anim.hc_walk))
                case 'H_FALLING':
                    self.change_image(self.anim.next(self.anim.h_fall, first_frame=4, loop=False))
                case 'H_JUMPING':
                    #self.change_image(self.anim.next(self.anim.h_jump, first_frame=1, last_frame=1, loop=False))
                    self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1))
                case 'HJ_FALLING':
                    self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1))
                case 'F_BACKFLIP':
                    if self.sliding:
                        self.change_image(self.anim.slide)
                        rotation = min(45, max(-45, int(-self.vector_y / 5)))
                        if not self.flipped:
                            if self.vector_y < 0:
                                self.rotate_around_center(rotation)
                            else:
                                self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=1, speed_mult=3))
                        if self.flipped:
                            if self.vector_y < 0:
                                self.rotate_around_center(-rotation)
                            else:
                                self.change_image(self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=1, speed_mult=3))
                    else:
                        self.change_image(
                            self.anim.next(self.anim.h_jump, last_frame=4, loop=True, step=-1, speed_mult=3))
                case 'ROLLING':
                    self.change_image(self.anim.next(self.anim.roll, last_frame=4, loop=False, speed_mult=3))


            #self.anim_tick_counter = 0

    def slide_fx(self):
        play_sfx('slide', extension='ogg')

    def crash_fx(self):
        play_sfx('deep_hit')


# ---

    def render(self):
        render(self.img, self.rect)
