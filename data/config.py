import pygame
import sys
import random

testing = True


pygame.init()


class window:
    width = 800
    height = 448
    center_width = width / 2
    center_height = height / 2
    center = (center_width, center_height)
    display = pygame.display.set_mode((width, height))
    background_color = (10, 10, 10)


class fps:

    global clock

    @classmethod
    def get(cls):
        return int(clock.get_fps())

    max = 240           #random.randint(1, 10) * 100
    last_values = []
    max_samples = 5
    avg = 0
    show = True
    key_press_delay = 0.2

    tick_counter = 0
    loop_counter = 0

    font = pygame.font.Font(None, 64)
    color = 'lightsalmon' #(195, 100, 195)

    alignment = "topright"
    coords = (window.width - 64, 32)



    @classmethod
    def render(cls):
        cls.tick_counter += delta.time()

        if cls.tick_counter >= cls.key_press_delay and pygame.key.get_pressed()[pygame.K_f]:
            if cls.show:
                cls.show = False
                cls.tick_counter = 0
            else:
                cls.show = True
                cls.tick_counter = 0

        if cls.show:

            cls.loop_counter += 1

            if cls.loop_counter >= 100:

                cls.last_values.append(cls.get())

                if len(cls.last_values) >= cls.max_samples:
                   cls.avg = int(sum(cls.last_values) / len(cls.last_values))
                   cls.last_values.clear()
                cls.loop_counter = 0

            text = cls.font.render(str(cls.avg), 1, pygame.Color(cls.color))
            rect = text.get_rect()
            setattr(rect, cls.alignment, cls.coords)
            pygame.draw.rect(window.display, 'black', rect)
            render(text, rect)


class delta:
    curr_time = 0
    last_time = 0

    @classmethod
    def time(cls):
        delta_time = (cls.curr_time - cls.last_time) / 1000

        return delta_time

    @classmethod
    def time_update(cls):
        cls.last_time = cls.curr_time
        cls.curr_time = pygame.time.get_ticks()


class gravity():
    fall_speed_ceil = 600


def quit_game():
    pygame.quit()
    sys.exit()


def render(img, coords=(0, 0)):
    window.display.blit(img, coords)


clock = pygame.time.Clock()