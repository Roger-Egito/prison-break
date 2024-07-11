import pygame
from data.config import window

class Collision:

    def __init__(
            self,
            anchor,
            x=0,
            y=0,
            size_mult=1.5,
            flipped=False,
            offset=(0, 0),
            dimensions=(0, 0)
):

        self.offset_left = offset[0] * size_mult
        self.offset_top = offset[1] * size_mult
        self.x = x + self.offset_left
        self.y = y + self.offset_top
        self.default_x = x
        self.default_y = y
        self.width = dimensions[0] * size_mult if dimensions[0] else anchor.width * size_mult
        self.height = dimensions[1] * size_mult if dimensions[1] else anchor.height * size_mult
        self.size_mult = size_mult
        self.default_width = self.width
        self.default_height = self.height
        self.flipped = flipped
        self.default_dimensions = dimensions
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #self.l_radius = 13
        #self.light = None
        #self.light_circle =
        self.anchor = anchor

    def render_light_circle(self):
        pygame.draw.circle(window.display, (200, 150, 100, 10), self.light.center, self.light.width)

    @property
    def coords(self):
        coords = (self.x, self.y)
        return coords

    @property
    def default_coords(self):
        coords = (self.default_x, self.default_y)
        return coords

# ---

    @property
    def center(self):
        center = (self.center_x, self.center_y)
        return center

    @property
    def center_width(self):
        return round(self.width / 2)

    @property
    def center_height(self):
        return round(self.height / 2)

    @property
    def center_x(self):
        return round(self.x + self.center_width)

    @property
    def center_y(self):
        return round(self.y + self.center_height)

    # ---

    @property
    def left(self):
        return self.x

    @property
    def top(self):
        return self.y

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height

    # ---

    def update_offset(self):
        self.offset_left *= self.size_mult
        self.offset_top *= self.size_mult

    def update_position(self):
        if self.flipped:
            self.x = self.anchor.right - self.offset_left - self.width
        else:
            self.x = self.anchor.x + self.offset_left

        self.y = self.anchor.y + self.offset_top

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
        #self.update_light()

    #def update_light(self):
    #    self.light.x = self.rect.x - self.l_radius - ((self.height - self.width) / 2)
    #    self.light.y = self.rect.y - self.l_radius

    def update_x(self):
        if self.flipped:
            self.x = self.anchor.right - self.offset_left - self.width
        else:
            self.x = self.anchor.x + self.offset_left
        self.rect.x = round(self.x)

    def update_y(self):
        self.y = self.anchor.y + self.offset_top
        self.rect.y = round(self.y)

    def update_size(self):
        self.width *= self.size_mult
        self.height *= self.size_mult
        self.rect.width = round(self.width)
        self.rect.height = round(self.height)

#    def get_hits(self, tiles, coords=(0,0), collision_based=False, point_based=False):
#        hit_list = []
#        for tile in tiles:
#            if collision_based:
#                collision = tile.collision.rect
#                if self.rect.colliderect(collision):
#                    hit_list.append(collision)
#            elif point_based:
#                if tile.rect.collidepoint(coords):
#                    hit_list.append(tile.rect)
#            else:
#                rect = tile.rect
#                if self.rect.colliderect(rect):
#                    hit_list.append(rect)
#        return hit_list

    def get_hits(self, tiles, coords=(0,0), collision_based=False, point_based=False):
        hit_list = []
        for tile in tiles:
            if point_based:
                if tile.rect.collidepoint(coords):
                    hit_list.append(tile.rect)
            else:
                if not hasattr(tile, 'hca'):
                    print('what?')
                if tile.hca:
                    collision = tile.collision.rect
                    if self.rect.colliderect(collision):
                        hit_list.append(tile)
                else:
                    rect = tile.rect
                    if self.rect.colliderect(rect):
                        hit_list.append(tile)


        return hit_list

    def is_hitting_sprite(self, sprite):
        return self.rect.colliderect(sprite.collision.rect)

    def is_hitting_point(self, coords):
        return self.rect.collidepoint(coords)

    def is_hitting_circle(self, r, center):
        circle_distance_x = abs(center[0] - self.rect.centerx)
        circle_distance_y = abs(center[1] - self.rect.centery)
        if circle_distance_x > self.rect.w / 2.0 + r or circle_distance_y > self.rect.h / 2.0 + r:
            return False
        if circle_distance_x <= self.rect.w / 2.0 or circle_distance_y <= self.rect.h / 2.0:
            return True
        corner_x = circle_distance_x - self.rect.w / 2.0
        corner_y = circle_distance_y - self.rect.h / 2.0
        corner_distance_sq = corner_x ** 2.0 + corner_y ** 2.0
        return corner_distance_sq <= r ** 2.0

    def get_line_hits(self, tiles, x, y, width, height):
        hit_list = []
        for tile in tiles:
            rect = tile.rect
            if rect.clipline((x, y), (width, height)):
                hit_list.append(rect)
        return hit_list