from data.sprite import Sprite
from data.config import window, calc
from data.stage import *
from data.game import game_over, stage_restart
from data.collision import *
from data.audio import *
from data.hearing import Sound_sphere
from data.renderer import noise
import pygame
import random

class Enemy(Sprite):

    def __init__(self, type=None, ai=None, hor_dir=1, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = type
        self.allow_movement = True
        self.ai = ai
        self.hor_dir = hor_dir
        self.wandering = True
        self.checking = False
        self.point_of_interest = False
        self.chasing = False
        self.alert = False
        self.waiting_tick_counter = 0
        self.step_tick_counter = 0

        if self.type == 'Soldier':
            self.anim.walk = self.anim.populate('assets/Characters/Enemy 2/Walk.png', image_count=6, dimensions=(0, 0, 96, 96))
            self.anim.run = self.anim.populate('assets/Characters/Enemy 2/Attack2.png', image_count=6, dimensions=(0, 0, 96, 96))
            self.anim.jump = self.anim.populate('assets/Characters/Enemy 2/Attack3.png', image_count=6, dimensions=(0, 0, 96, 96))


    def state_control(self):
        s = self.States
        st = self.state
        walking = self.vector_x != 0
        airborne = self.airborne

        if airborne and self.anim.jump:
            self.state = s.FAST_JUMPING
        elif walking and self.anim.walk:
            self.state = s.WALKING
            if self.alert and self.anim.run:
                self.state = s.RUNNING
        else:
            self.state = s.IDLE

    def ai_control(self, player):
        AI = self.AIs

        if self.ai == AI.SOLDIER:
            if not self.airborne:
                self.vector_y = 0
            self.allow_movement = not stage.in_transition
            if pygame.Rect.colliderect(self.vision.rect, player.collision.rect):
                if not self.chasing:
                    self.alert = True
                    self.checking = True
                    self.chasing = True
                    play_music('action')
                    play_sfx('alert-3', channel=2)
                    #play_sfx('woob')
            else:
                #play_music('safe')
                self.alert = False
                print(self.alert)
                self.chasing = False
                self.airborne = self.vector_y != 0

            if all(not enemy.alert for enemy in stage.enemy_group):
                play_music('safe')

            if self.allow_movement:
                speed = self.speed
                collisions = []
                if self.alert:
                    speed *= 5
                if self.chasing:
                    collisions = self.move_hor_to(player.collision.center_x, sprinting=True)
                elif self.checking:
                    collisions = []
                    self.vector_x = 0
                    if self.point_of_interest:
                        collisions = self.move_hor_to(self.point_of_interest[0], jogging=True)
                elif self.wandering:
                    if self.hor_dir == 1:
                        collisions = self.move_right(speed)
                    else:
                        collisions = self.move_left(speed)

                player_hit = self.collision.is_hitting_sprite(player)
                edge_hit = False
                edge2_hit = False
                edge3_hit = False
                reverse_edge_hit = False

                if self.vector_x > 0:
                    edge_hit = not self.check_collision_bottomright(stage.tile_group)
                    if edge_hit:
                        self.collision.rect.x += 32
                        edge2_hit = not self.check_collision_bottomright(stage.tile_group)
                        self.collision.rect.x -= 32
                        reverse_edge_hit = not self.check_collision_bottomleft(stage.tile_group)
                        if edge2_hit:
                            self.collision.rect.x += 64
                            edge3_hit = not self.check_collision_bottomright(stage.tile_group)
                            self.collision.rect.x -= 64

                elif self.vector_x < 0:
                    edge_hit = not self.check_collision_bottomleft(stage.tile_group)
                    if edge_hit:
                        self.collision.rect.x -= 32
                        edge2_hit = not self.check_collision_bottomleft(stage.tile_group)
                        self.collision.rect.x += 32
                        reverse_edge_hit = not self.check_collision_bottomright(stage.tile_group)
                        if edge2_hit:
                            self.collision.rect.x -= 64
                            edge3_hit = not self.check_collision_bottomleft(stage.tile_group)
                            self.collision.rect.x += 64
                if edge_hit or self.airborne:
                    if (self.chasing and edge2_hit and not edge3_hit) or self.airborne:
                        if not self.airborne:
                            self.jump(1)
                        self.airborne = True
                        if self.vector_x > 0:
                            self.move_right(self.speed * 2)
                        elif self.vector_x < 0 :
                            self.move_left(self.speed * 2)

                    if edge2_hit and not self.chasing:
                        self.x -= self.vector_x * delta.time()
                        self.vector_x = 0
                        if reverse_edge_hit:
                            self.wandering = False
                    else:
                        self.wandering = True


                for enemy in stage.enemy_group:
                    for sound in enemy.sound_spheres:
                        if self.name != enemy.name and self.collision.is_hitting_circle(sound.radius, sound.origin):
                            self.checking = True
                            self.point_of_interest = sound.origin

                for sound in player.sound_spheres:
                    if self.collision.is_hitting_circle(sound.radius, sound.origin):
                        self.checking = True
                        self.point_of_interest = sound.origin

                if self.checking:
                    if self.vector_x == 0:
                        self.waiting_tick_counter += 1 * delta.time()
                        if self.waiting_tick_counter >= 3:
                            self.point_of_interest = False
                            self.checking = False
                            self.waiting_tick_counter = 0
#                    if self.vector_x == 0 or pygame.Rect.collidepoint(self.collision.rect, (self.point_of_interest[0], self.collision.rect.centery)):
#                        self.waiting_tick_counter += 1 * delta.time()
#                        if self.waiting_tick_counter >= 3:
#                            self.point_of_interest = False
#                            self.checking = False
#                            self.waiting_tick_counter = 0


                sprite_hit = False
                for sprite in stage.enemy_group:
                    if self.collision.is_hitting_sprite(sprite) and self.name != sprite.name:
                        sprite_hit = True
                if player_hit and not player.immortal:
                    stage_restart(death=True)
                elif len(collisions) or edge_hit or sprite_hit:
                    if self.chasing:
                        self.vector_x = 0
                    else:
                        self.hor_dir *= -1

                if self.vector_x != 0:
                    self.step_tick_counter += 1 * delta.time()
                    step_delay = 0.75
                    if self.chasing:
                        step_delay = 0.2
                    if self.step_tick_counter >= step_delay:
                        Sound_sphere(origin=self.collision.rect.center, groups=self.sound_spheres,
                                     max_radius=abs(self.vector_x))
                        self.step_tick_counter = 0

    def distance_from(self, coords):
        distance = (coords[0] - self.center_x, coords[1] - self.center_y)
        return distance

    def distance_x(self, x):
        return self.collision.center_x - x

    def distance_x_tiles(self, x):
        return (self.collision.center_x - x) / 32

    def distance_from_percentage(self, coords):
        distance = self.distance_from(coords)
        distance_percentage = (distance[0] / window.width, distance[1] / window.width)
        return distance_percentage

    def move_to(self, coords):
            distance = self.distance_from((coords.center_x, coords.center_y))
            #distance_percentage = self.distance_from_percentage((coords.center_x, coords.center_y))
            hypotenuse = max(1, calc.hypotenuse(distance[0], distance[1]))
            #hypotenuse_speed = (self.speed / 2) * (1 - hypotenuse / window.width)
            if (pygame.Rect.colliderect(self.rect, coords.rect)):
                vector_x = 0
                vector_y = 0
            else:
                vector_x = (distance[0] / hypotenuse) * self.speed
                vector_y = (distance[1] / hypotenuse) * self.speed
            #vector_x = (hypotenuse_speed * distance[0] / hypotenuse)
            #vector_y = (hypotenuse_speed * distance[1] / hypotenuse)
            self.move(vector_x, vector_y)
            #   if (pygame.Rect.colliderect(self.rect, coords.rect)):
            #       self.x = random.randint(0, window.width - self.width)
            #       self.y = random.randint(0, window.height - self.height)

    def move_hor_to(self, x, jogging=False, sprinting=False, speed=0):
            distance = self.distance_x_tiles(x)
            hor_speed = speed if speed else self.speed if distance else 0
            if jogging:
                hor_speed *= 2
            if sprinting:
                hor_speed *= 5

            if distance > 0.1:
                collisions = self.move(hor_speed=-hor_speed)
            elif distance < -0.1:
                collisions = self.move(hor_speed=hor_speed)
            else:
                self.vector_x = 0
                collisions = []
            return collisions