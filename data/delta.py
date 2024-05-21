import pygame
from data.config import window


def time():
    now = pygame.time.get_ticks()
    delta_time = (now - window.prev_time) / 1000
    window.prev_time = now
    return delta_time

