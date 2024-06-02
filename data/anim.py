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
        self.idle = []
        self.walk = []
        self.jump = []
        self.run = []
        self.crouch = []

        self.frame = 0
        self.loop = loop
        self.tick_counter = 0
        self.delay = delay
        self.speed = 1

    def sheet_to_img(self, file, dimensions=(4, 14, 20, 34), has_alpha=True, colorkey=None):
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
        images = [self.sheet_to_img(file, dimension, has_alpha, colorkey) for dimension in tups]
        return images

    #def iter(self):
    #    self.frame = 0
    #    self.frame = self.total_frames
    #    return self

    def next(self, sheet, speed_mult=1, loop=True, first_frame=0, last_frame=0):
        last_frame = len(sheet)-1 if last_frame == 0 else last_frame
        if self.frame + first_frame > last_frame:
            if not loop:
                self.frame = last_frame
                return sheet[self.frame]
            else:
                self.frame = 0
        image = sheet[self.frame + first_frame]
        self.tick_counter += delta.time() * speed_mult
        #frames = self.total_frames / max(0.01, speed_mult)
        #self.frame -= 1
        if self.tick_counter >= self.delay:
            self.frame += 1
            self.tick_counter = 0
        #if self.frame == 0:
        #    self.counter += 1
        #    self.frame = frames
        return image



    #def __add__(self, sheet, external_sheet):
    #    sheet.extend(external_sheet.images)
    #    return sheet