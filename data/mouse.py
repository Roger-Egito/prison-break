import pygame
from data.config import window

def pos():
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (mouse_pos[0] - window.srd[0]/2, mouse_pos[1] - window.srd[1]/2)
    return mouse_pos

def update_last_pos():
    window.mouse_last_position = pos()

def create_rect(width=20, height=20):
    mouse_pos = pos()
    return pygame.Rect(mouse_pos[0]-width/2, mouse_pos[1]-height/2, width, height)