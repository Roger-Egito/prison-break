import pygame
from data.config import window, render

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def _create_border(text_surface, font, text, border_px=2, border_color=(0,0,0)):
    w = text_surface.get_width() + 2 * border_px
    h = font.get_height()
    border_surf = pygame.Surface((w, h + 2 * border_px)).convert_alpha()
    border_surf.fill((0, 0, 0, 0))
    surf = border_surf.copy()
    border_surf.blit(font.render(text, True, border_color).convert_alpha(), (0, 0))
    for dx, dy in _circlepoints(border_px):
        surf.blit(border_surf, (dx + border_px, dy + border_px))
    surf.blit(text_surface, (border_px, border_px))
    return surf

def write(text, font_name=None, font_size=24, font_color=pygame.Color('white'), border_color=(0, 0, 0), border_px=2, border=True, rect=True, draw=True, x=0, y=0, row=0, row_spacing=50, text_align="center"):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, font_color).convert_alpha()

    if border:
        text_surface = _create_border(text_surface, font, text, border_px, border_color)

    if rect:
        text_rect = text_surface.get_rect()
        setattr(text_rect, text_align, (x, (y + (row * row_spacing))))
        if draw:
            render(text_surface, text_rect)
        return text_rect
    else:
        if draw:
            render(text_surface, (x, y))
        return text_surface



smoothscale_tick_counter = 0


def smoothscale_text_rect(current_size, original_size, add=1, to=0, mult=0, step=1):

    if add:
        pass