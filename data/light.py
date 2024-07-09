import pygame

class Light(pygame.sprite.Sprite):
    def __init__(self,
                 groups,
                 anchor=None,
                 x=0,
                 y=0,
                 size_mult=1,
                 flipped=False,
                 offset=(0, 0),
                 max_radius=20,
                 strength=60,
                 dimensions=(0, 0)
                 ):
        super().__init__(groups)
        self.max_radius = max_radius

        #self.offset_left = offset[0] * size_mult
        #self.offset_top = offset[1] * size_mult
        #self.x = x + self.offset_left
        #self.y = y + self.offset_top
        #self.default_x = x
        #self.default_y = y
        ##self.width = dimensions[0] * size_mult if dimensions[0] else anchor.width * size_mult
        ##self.height = dimensions[1] * size_mult if dimensions[1] else anchor.height * size_mult
        #self.size_mult = size_mult
        ##self.default_width = self.width
        ##self.default_height = self.height
        #self.flipped = flipped
        ##self.default_dimensions = dimensions
        ##self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #self.radius = 1
        #self.strength = 1
        ##self.light = pygame.Rect(self.x - self.l_radius - ((self.height - self.width) / 2), self.y - self.l_radius,
        ##                         self.height + 2 * self.l_radius, self.height + 2 * self.l_radius)
        ## self.light_circle =
        #self.anchor = anchor
