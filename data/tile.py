import pygame
from data.config import window, render, calc, delta



class Tile(pygame.sprite.Sprite):
    def __init__(self, coords, image, groups, name=''):
        super().__init__(groups)
        self.name = name
        self.img = image
        self.original_img = self.img.copy()
        self.img_hidden = self.img.copy()
        self.img_hidden.fill((255, 255, 255, 200), None, pygame.BLEND_RGBA_MULT)
        self.hidden = False
        self.x = coords[0]
        self.y = coords[1]
        self.speed = 200
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.rect = self.img.get_rect(topleft=coords)
        self.darkness_level = 255
        self.max_darkness = 255
        self.light_percentage = 0
        self.last_darkness_level = 255
        self.in_light = False
        self.light_radius = 6
        self.hca = False        # Has Collision Attribute


    def render(self):
        render(self.img, self.rect)

    def move(self, hor=0, ver=0, speed=0):
        if hor:
            hor_speed = hor * speed if speed else hor * self.speed
            self.x += hor_speed * delta.time()
            #self.rect.x += hor_speed * delta.time()
        if ver:
            ver_speed = ver * speed if speed else ver * self.speed
            self.y += ver_speed * delta.time()
            #self.rect.y += ver_speed * delta.time()
        self.update_rect_position()

    def hide(self):
        self.img = self.img_hidden

    def unhide(self):
        self.img = self.original_img

    def endarken(self, coords, direction=1, light_radius=13):
        distance_x = self.rect.centerx - coords[0]
        distance_y = self.rect.centery - coords[1]
        #distance_in_tiles_x = round(max(0.1, distance_x / 32))
        #distance_in_tiles_y = round(max(0.1, distance_x / 32))
        distance = calc.hypotenuse(abs(distance_x), abs(distance_y))
        distance_in_tiles = distance / 32
        distance_in_tiles_x = distance_x / 32
        distance_in_tiles_y = distance_y / 32


        if distance_in_tiles <= light_radius:
            darkness_level = ((max(0.1, distance_in_tiles)) * (self.max_darkness/light_radius))

            light_percentage = abs(100 - ((100 * darkness_level) / self.max_darkness))

            if self.in_light:
                if darkness_level < self.darkness_level:
                    self.light_percentage = light_percentage
                    self.darkness_level = (self.max_darkness * (100 - self.light_percentage)) / 100
            else:
                self.light_percentage = light_percentage
                self.darkness_level = (self.max_darkness * (100 - self.light_percentage)) / 100
                self.in_light = True

            #self.in_light = True
            #self.darkness_level = ((max(0.1, distance_in_tiles)) * (255/10)) #(255 / light_radius))
            #darkness_level = ((max(0.1, distance_in_tiles)) * (255 / light_radius))
            #if darkness_level < self.darkness_level:
            #self.darkness_level = darkness_level
        elif not self.in_light:
            self.darkness_level = self.max_darkness


    def update_rect_position(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def update(self, lightsource_group, is_tile=True, is_darkness=False, is_foreground=False, light_radius=5):
            self.in_light = False
            for sprite in lightsource_group:
                if sprite.light_radius:
                    if sprite.hca:
                        direction = -1 if sprite.flipped else 1
                        self.endarken(coords=(sprite.collision.rect.centerx, sprite.collision.rect.centery), direction=direction, light_radius=sprite.light_radius)
                    else:
                        self.endarken(coords=(sprite.rect.centerx, sprite.rect.centery), direction=1, light_radius=sprite.light_radius)

                    if sprite.name == 'Player':
                        if is_foreground and pygame.Rect.colliderect(self.rect, sprite.collision.rect):
                            self.hide()
                            self.hidden = True
                        elif is_foreground and self.hidden:
                            self.unhide()
                            self.hidden = False

            if self.darkness_level and is_darkness:
                s = pygame.Surface((self.rect.width, self.rect.height))
                s.set_alpha(self.darkness_level)
                s.fill((0, 0, 30))
                render(s, coords=(self.rect.x, self.rect.y))

