import pygame

class Anim:
    """sprite strip animator

    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """

    def __init__(self, loop=True, frames=60, speed=1):
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

        self.counter = 0
        self.loop = loop
        self.total_frames = frames
        self.frame = frames
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

    def populate(self, file, dimensions=(4, 14, 20, 34), image_count=4, step=1, has_alpha=True, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(dimensions[0] + dimensions[2] * x * step, dimensions[1], dimensions[2], dimensions[3])
                for x in range(image_count)]
        images = [self.sheet_to_img(file, dimension, has_alpha, colorkey) for dimension in tups]
        return images

    def iter(self):
        self.counter = 0
        self.frame = self.total_frames
        return self

    def next(self, sheet, speed_mult=1, loop=True, last_frame=0):
        last_frame = len(sheet)-1 if last_frame == 0 else last_frame
        if self.counter > last_frame:
            if not loop:
                self.counter = last_frame
                return sheet[self.counter]
            else:
                self.counter = 0
        image = sheet[self.counter]
        frames = self.total_frames / max(0.01, speed_mult)
        self.frame -= 1
        if self.frame == 0:
            self.counter += 1
            self.frame = frames
        return image



    #def __add__(self, sheet, external_sheet):
    #    sheet.extend(external_sheet.images)
    #    return sheet