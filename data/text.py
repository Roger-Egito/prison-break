import pygame

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

def write(text, font_name=None, font_size=64, font_color=pygame.Color('white'), border_color=(0, 0, 0), border_px=2, border=True):
    font = pygame.font.SysFont(font_name, font_size)
    text_surface = font.render(text, True, font_color).convert_alpha()


    if border:
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
    else:
        return text_surface