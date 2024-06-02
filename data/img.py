import pygame
from data.config import window, render, delta

class img:
    def __init__(self, image, has_alpha=True, stretch=False, x=0, y=0):
        self.load = pygame.image.load
        self.transform = pygame.transform

        self.img = self.load(image).convert_alpha() if has_alpha else self.load(image).convert()
        self.img = self.transform.scale(self.img, (window.width, window.height)) if stretch else self.img
        self.has_alpha = has_alpha
        self.stretch = stretch
        self.x = x
        self.y = y
        self.default_x = x
        self.default_y = y

    @property
    def coords(self):
        return self.x, self.y

    @property
    def default_coords(self):
        return self.default_x, self.default_y

    @property
    def width(self):
        return self.img.get_width()

    @property
    def height(self):
        return self.img.get_height()

    @property
    def center_width(self):
        return round(self.width / 2)

    @property
    def center_height(self):
        return round(self.height / 2)

    @property
    def center(self):
        center = (self.x + self.center_width, self.y + self.center_height)
        return center

    def render(self):
        render(self.img, self.coords)

class Background(img):
    def __init__(self, image, has_alpha=True, stretch=True, x=0, y=0):
        super().__init__(image, has_alpha, stretch, x, y)

    def render_horizontal_scrolling(self, speed=50, direction=-1, speed_mult=1):
        render(self.img, self.coords)
        render(self.img, (self.x + (self.width * -direction), self.y))
        self.x += speed * direction * speed_mult * delta.time()
        if (self.x * direction) >= self.width:
            self.x = self.default_x

    def render_vertical_scrolling(self, speed=50, direction=1, speed_mult=1):
        render(self.img, self.coords)
        render(self.img, (self.x, self.y + (self.height * -direction)))
        self.y += speed * direction * speed_mult * delta.time()
        if (self.y * direction) >= self.height:
            self.y = self.default_y

class Foreground(img):
    def __init__(self, image, has_alpha=True, stretch=True, x=0, y=0):
        super().__init__(image, has_alpha, stretch, x, y)