import pygame

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
        self.anchor = anchor

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

    def test(self, tiles):
        hit_list = []
        for tile in tiles:
            rect = tile.rect
            if self.rect.colliderect(rect):
                hit_list.append(rect)
        return hit_list
