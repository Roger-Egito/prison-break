import pygame
from data.config import delta

class Anim:
    """sprite strip animator

    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """

    def __init__(self, loop=True, delay=0.25, speed=1):
        """construct a SpriteStripAnim

        filename, dimensions, count, and colorkey are the same arguments used
        by spritesheet.load_strip.

        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.

        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        #self.images = images

        # Sheets
        self.last_sheet = []
        self.idle = []
        self.idle2 = []
        self.idle3 = []
        self.idle4 = []
        self.idle5 = []
        self.random_idle = []
        self.walk = []
        self.jump = []
        self.s_jump = []
        self.run = []
        self.crouch = []
        self.c_walk= []
        self.slide = []
        self.hang = []
        self.h_crouch = []
        self.h_walk = []
        self.hc_walk = []
        self.h_fall = []
        self.h_jump = []
        self.roll = []

        self.frame = 0
        self.loop = loop
        self.tick_counter = 0
        self.delay = delay
        self.speed = 1

    def img(self, file, dimensions=(0, 0, 48, 48), has_alpha=True, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rectangle = pygame.Rect(dimensions)
        image = pygame.Surface(rectangle.size)
        image.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        file_image = pygame.image.load(file).convert_alpha() if has_alpha else pygame.image.load(file).convert()
        image.blit(file_image, (0, 0), rectangle)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        # self.img = image
        return image

    def populate(self, file, dimensions=(0, 0, 48, 48), image_count=4, step=1, has_alpha=True, colorkey=None):  #(4, 14, 20, 34)
        "Loads a strip of images and returns them as a list"
        tups = [(dimensions[0] + dimensions[2] * x * step, dimensions[1], dimensions[2], dimensions[3])
                for x in range(image_count)]
        images = [self.img(file, dimension, has_alpha, colorkey) for dimension in tups]
        return images

    #def iter(self):
    #    self.frame = 0
    #    self.frame = self.total_frames
    #    return self

    def next(self, sheet, speed_mult=1, loop=True, first_frame=0, last_frame=0, step=1):  # Step < 0 reverses animation

        if sheet != self.last_sheet:
            self.frame = 0
        self.last_sheet = sheet
        last_frame = len(sheet)-1 if last_frame == 0 else last_frame

        if step >= 0:
            if self.frame + first_frame > last_frame:
                if not loop:
                    self.frame = last_frame
                    return sheet[self.frame]
                else:
                    self.frame = 0
            image = sheet[self.frame + first_frame]
        else:
            if last_frame + self.frame < first_frame:
                if not loop:
                    self.frame = first_frame - last_frame
                    return sheet[first_frame]
                else:
                    self.frame = 0
            image = sheet[last_frame + self.frame]

        self.tick_counter += delta.time() * speed_mult

        if self.tick_counter >= self.delay:
            self.frame += step
            self.tick_counter = 0

        return image

    def animation_is_over(self, sheet, first_frame=0, last_frame=0):
        last_frame = len(sheet) - 1 if last_frame == 0 else last_frame
        if self.frame + first_frame > last_frame:
            return True
        else:
            return False


    #def __add__(self, sheet, external_sheet):
    #    sheet.extend(external_sheet.images)
    #    return sheet