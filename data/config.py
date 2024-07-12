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

def return_random_color():
    random_color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    return random_color

class window:
    width = 800
    height = 448
    screen_size = (1280, 720) #(1920, 1080)
    srd = (screen_size[0] - width, screen_size[1] - height)  # Screen Resolution Difference
    srdp = (screen_size[0] / width, screen_size[1] / height)  # Screen Resolution Difference Proportion (2 = 200% original size)
    center_width = width / 2
    center_height = height / 2
    center = (center_width, center_height)
    #os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen = pygame.display.set_mode((screen_size))#, pygame.NOFRAME)
    display = pygame.Surface((width, height), pygame.SRCALPHA)
    background_color = (10, 10, 10)
    gm_tick_counter = 0
    gm_tick_delay = 0.4
    mouse_is_still_on_top = False
    mouse_last_position = (0, 0)

    @classmethod
    def draw(cls):
        cls.screen.blit(pygame.transform.scale(window.display, window.screen_size), (0, 0))

class flags:
    map_00_key_collected = False
    map_00_door_opened = False
    map_01_door_opened = False

class fps:

    global clock

    @classmethod
    def get(cls):
        return int(clock.get_fps())

    max = 60                #random.randint(1, 10) * 100
    last_values = []
    max_samples = 5
    avg = 0
    show = False
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


class delta:
    curr_time = 0
    last_time = 0

    @classmethod
    def time(cls):          # How much time between last frame and this frame - in seconds
        delta_time = min(0.06, (cls.curr_time - cls.last_time) / 1000)

        return delta_time

    @classmethod
    def time_update(cls):
        cls.last_time = cls.curr_time
        cls.curr_time = pygame.time.get_ticks()


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