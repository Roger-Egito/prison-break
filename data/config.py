import pygame
import sys
import random
import math
import os
from data.audio import *
import pytmx
from pytmx.util_pygame import *

testing = True


pygame.init()


class window:
    width = 800
    height = 448
    screen_size = (1607, 900) #(1920, 1080)
    center_width = width / 2
    center_height = height / 2
    center = (center_width, center_height)
    #os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((screen_size))#, pygame.NOFRAME)
    display = pygame.Surface((width, height), pygame.SRCALPHA)
    background_color = (10, 10, 10)

    @classmethod
    def draw(cls):
        cls.screen.blit(pygame.transform.scale(window.display, window.screen_size), (0, 0))



class fps:

    global clock

    @classmethod
    def get(cls):
        return int(clock.get_fps())

    max = 60                #random.randint(1, 10) * 100
    last_values = []
    max_samples = 5
    avg = 0
    show = True
    key_press_delay = 0.2

    key_tick_counter = 0
    text_tick_counter = 0

    font = pygame.font.Font(None, 32)
    color = 'lightsalmon'

    alignment = "topright"
    coords = (window.width - 16, 8)

    @classmethod
    def render(cls):
        cls.key_tick_counter += delta.time()
        cls.text_tick_counter += delta.time()

        if cls.key_tick_counter >= cls.key_press_delay:
            if pygame.key.get_pressed()[pygame.K_f]:
                if cls.show:
                    cls.show = False
                    cls.key_tick_counter = 0
                else:
                    cls.show = True
                    cls.key_tick_counter = 0
            else:
                cls.key_tick_counter = cls.key_press_delay

        if cls.show:

            if cls.text_tick_counter >= 0.5:

                cls.last_values.append(cls.get())

                if len(cls.last_values) >= cls.max_samples:
                   cls.avg = int(sum(cls.last_values) / len(cls.last_values))
                   cls.last_values.clear()

                cls.text_tick_counter = 0

            text = cls.font.render("FPS: " + str(cls.avg), 1, pygame.Color(cls.color))
            rect = text.get_rect()
            setattr(rect, cls.alignment, cls.coords)
            pygame.draw.rect(window.display, 'black', rect)
            render(text, rect)


class volume:

    max = 0.2
    current = 0.2
    paused = False

    key_press_delay = 0.2
    tick_counter = 0
    loop_counter = 0

    @classmethod
    def check_mute(cls):
        cls.tick_counter += delta.time()
        if cls.tick_counter >= cls.key_press_delay and pygame.key.get_pressed()[pygame.K_m]:
            if cls.paused:
                resume_music()
                cls.paused = False
                cls.tick_counter = 0
            else:
                pause_music()
                cls.paused = True
                cls.tick_counter = 0


class delta:
    curr_time = 0
    last_time = 0

    @classmethod
    def time(cls):          # How much time between last frame and this frame - in seconds
        delta_time = min(0.02, (cls.curr_time - cls.last_time) / 1000)

        return delta_time

    @classmethod
    def time_update(cls):
        cls.last_time = cls.curr_time
        cls.curr_time = pygame.time.get_ticks()


class calc:
    @classmethod
    def hypotenuse(cls, a, b):
        return math.sqrt(a ** 2 + b ** 2)


def quit_game():
    pygame.quit()
    sys.exit()


def render(img, coords=(0, 0)):
    window.display.blit(img, coords)


clock = pygame.time.Clock()