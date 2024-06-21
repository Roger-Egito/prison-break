import pygame
from data.config import window, render, calc

class Tile(pygame.sprite.Sprite):
    def __init__(self, coords, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=coords)
        self.illuminated = 1
        self.last_light_level = 0

    def update(self, method=0, coords=(0, 0), step=0, light_radius=5, light_strength=35, object=0, tiles=0, decor_group=False, new_group=0):
        match method:
            case 0:
                if self.illuminated:
                    #self.image.fill((0, 0, 255))#, special_flags=pygame.BLEND_MULT)
                    s = pygame.Surface((self.rect.width, self.rect.height))
                    s.set_alpha(self.illuminated)
                    s.fill((0, 0, 30))
                    #m = None
                    #if decor_group:
                    #    m = pygame.mask.from_surface(self.image)
                    #else:
                    #self.image.blit(s, (self.rect.x,self.rect.y))
                    render(s, coords=(self.rect.x, self.rect.y))

                else:
                    #self.image.fill((255, 0, 0))#, special_flags=pygame.BLEND_MULT)
                    #if decor_group:
                    #    c = pygame.mask.from_surface(self.image)
                    #    c = c.to_surface()
                    #else:
                    c = pygame.Surface((self.rect[2], self.rect[3]))
                    c.set_alpha(220)
                    c.fill((0, 0, 30))
                    #self.image.blit(c, (self.rect.x,self.rect.y))
                    render(c, coords=(self.rect.x, self.rect.y))

            case 1:
                self.rect.x += step
            case 2:
                distance_x = self.rect.centerx - coords[0]
                distance_y = self.rect.centery - coords[1]
                distance_in_tiles_x = round(max(0.1, distance_x / 32))
                distance_in_tiles_y = round(max(0.1, distance_x / 32))
                direction_x = 0
                if distance_x > 0: direction_x = 1
                elif distance_x < 0: direction_x = -1
                direction_y = 0
                if distance_y > 0: direction_y = 1
                elif distance_y < 0: direction_y = -1
                distance = calc.hypotenuse(abs(distance_x), abs(distance_y))
                distance_in_tiles = round(max(0.1, distance / 32))

                if distance_in_tiles <= light_radius * 2:
                    #if distance_in_tiles * light_strength > self.illuminated:
                    #self.illuminated = 1
                    self.illuminated = ((distance / 64) * light_strength)
                    #self.add(new_group)
                else:
                    self.illuminated = 0
                    #self.remove(new_group)
                    #self.groups.remove(new_group)
                #if self in new_group:
                #    target_x = distance_x + (32 * direction_x)
                #    target_y = distance_y + (32 * direction_y)
                #    for tile in new_group:
                #        if tile.rect.collidepoint(target_x, target_y):
                #            self.illuminated = 0
                #            self.remove(new_group)

