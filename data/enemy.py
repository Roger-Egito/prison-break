from data.sprite import Sprite
from data.config import window, calc
import pygame
import random

class Enemy(Sprite):
    speed_mult = 0.75

    def distance_from(self, coords):
        distance = (coords[0] - self.center_x, coords[1] - self.center_y)
        return distance

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
