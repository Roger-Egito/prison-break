import pygame
from data.config import window, delta
import sys
import random
import math
import data.mouse as mouse


class Star:
    def __init__(self, x, y, width=2, height=2, corruption=False, size_mult=1, planet=False, planet_size_mult=1, planet_color=(255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size_mult = size_mult
        self.rect = pygame.Rect(x, y, width, height)
        self.corruption = corruption
        self.planet = planet
        self.planet_size_mult = planet_size_mult
        self.planet_color = planet_color

    @property
    def center(self):
        center = (self.x + self.width / 2, self.y + self.width / 2)
        return center

    def set_center(self, coordinate):
        self.x = coordinate[0] - self.width / 2
        self.y = coordinate[1] - self.height / 2

    def set_size(self, size):
        self.size_mult = size

    def distance_from_mouse(self):
        star_distance_from_mouse_x = self.x + (self.width / 2 * self.size_mult) - mouse.pos()[0]  # window.center_width
        star_distance_from_mouse_y = self.y + (self.height / 2 * self.size_mult) - mouse.pos()[1]  # window.center_height
        star_distance_from_mouse = (star_distance_from_mouse_x, star_distance_from_mouse_y)
        return star_distance_from_mouse


def create_constellation(number):
    constellation = []
    for star in range(number):
        star = Star(random.randint(0, window.width), random.randint(0, window.height))
        constellation.append(star)
    return constellation

#def get_star_distance_from_center():
#    star_distance_from_mouse_x = star.x + star.width / 2 - mouse.pos()[0]  # window.center_width
#    star_distance_from_mouse_y = star.y + star.height/2 - mouse.pos()[1]#window.center_height


def render_constellation(constellation, speed=5, moving_to_mouse=False):
    for star in constellation:
        star_distance_from_mouse = Star.distance_from_mouse(star)
        star_distance_from_mouse_percentage = (star_distance_from_mouse[0] / (window.width),
                                                               star_distance_from_mouse[1] / (window.width))

        if moving_to_mouse:

            star_distance_from_mouse_hipotenuse = math.sqrt(star_distance_from_mouse[0] ** 2 + star_distance_from_mouse[1] ** 2)
            star_distance_from_mouse_hipotenuse_speed = speed/2 * (1 - star_distance_from_mouse_hipotenuse / window.width)

            star.x -= star_distance_from_mouse_hipotenuse_speed * star_distance_from_mouse[0] / star_distance_from_mouse_hipotenuse #star_distance_from_mouse_hipotenuse_speed if star_distance_from_mouse[0] > 0 else -star_distance_from_mouse_hipotenuse_speed
            star.y -= star_distance_from_mouse_hipotenuse_speed * star_distance_from_mouse[1] / star_distance_from_mouse_hipotenuse #star_distance_from_mouse_hipotenuse_speed if star_distance_from_mouse[1] > 0 else -star_distance_from_mouse_hipotenuse_speed

        else:
            star.x += speed * star_distance_from_mouse_percentage[0]
            star.y += speed * star_distance_from_mouse_percentage[1]

        if moving_to_mouse:
            if star.rect.colliderect(mouse.create_rect()):
                star_spawn_direction = random.randint(0, 3)
                if star_spawn_direction == 0: Star.set_center(star, (random.randint(0, window.width), 0 - star.height/2))
                if star_spawn_direction == 1: Star.set_center(star, (window.width + star.width/2, random.randint(0, window.height)))
                if star_spawn_direction == 2: Star.set_center(star, (random.randint(0, window.width), window.height + star.height/2))
                if star_spawn_direction == 3: Star.set_center(star, (0 - star.width/2, random.randint(0, window.height)))

                planet_dice_roll = random.randint(0, 60)

                if planet_dice_roll == 60:
                    star.planet = True
                    star.planet_size_mult = random.randint(2, 3)
                    star.planet_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                else:
                    star.planet = False
                    star.planet_size_mult = 1
        else:
            while(
                star.x > window.width or
                star.x - star.width < 0 or
                star.y > window.height or
                star.y - star.height < 0
            ):
                Star.set_center(star, (mouse.pos()[0] + random.randint(-100, 100), mouse.pos()[1] + random.randint(-100, 100)))

                planet_dice_roll = random.randint(0, 60)

                if planet_dice_roll == 60:
                    star.planet = True
                    star.planet_size_mult = random.randint(2, 3)
                    star.planet_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                else:
                    star.planet = False
                    star.planet_size_mult = 1

                #if star.corruption is False:
                #   star.corruption = True
                #else:
                #   star.corruption = False

        star_new_distance_from_mouse = Star.distance_from_mouse(star)

        star_absolute_new_distance_from_mouse_percentage = max(abs(star_new_distance_from_mouse[0] / (window.width)), abs(star_new_distance_from_mouse[1] / (window.width)))

        Star.set_size(star, star_absolute_new_distance_from_mouse_percentage * star.planet_size_mult * 5 + 1)

        star.rect.x = round(star.x)
        star.rect.y = round(star.y)
        star.rect.width = round(star.width * star.size_mult * star.planet_size_mult)
        star.rect.height = round(star.height * star.size_mult * star.planet_size_mult)

        if star.rect.collidepoint(mouse.pos()) and star.corruption is False:
            star.corruption = True
            pygame.draw.rect(window.display, (195, 100, 195), star)
        elif star.corruption:
            pygame.draw.rect(window.display, (195, 100, 195), star)
        elif star.planet:
            pygame.draw.rect(window.display, star.planet_color, star)
        else:
            pygame.draw.rect(window.display, (255, 255, 255), star)
