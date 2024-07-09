import pygame
import window
import sys
import music
import mouse

class Button:
    def __init__(self, x=window.center_width, y=window.center_height,  text='', color=(240, 240, 240), surface=(150, 50), width=150, height=50, shadow=True, highlight=True):
        self.surface = pygame.Surface(surface)
        self.shadow = shadow
        self.highlight = highlight
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 24)
        if self.text != '':
            self.text_render = self.font.render(self.text, True, (0, 0, 0))
            self.text_rect = self.text_render.get_rect(center=(self.surface.get_width() / 2, self.surface.get_height() / 2))

    def render(self):
        if self.rect.collidepoint(mouse.pos()):
            pygame.draw.rect(self.surface, (195, 100, 195), (0, 0, self.width, self.height))
            if self.rect.collidepoint(window.mouse_last_position) is False:
                music.play_sfx(window.sfx_menu_cursor)
        else:
            pygame.draw.rect(self.surface, self.color, (0, 0, self.width, self.height))
        self.surface.blit(self.text_render, self.text_rect)

        if self.shadow:
            shadow_x = self.rect.x-5
            shadow_y = self.rect.y-5
            shadow_color = (100, 100, 100)
            shadow_width = self.rect.width + 10
            shadow_height = self.rect.height + 10
            shadow_surface = pygame.Surface((shadow_width, shadow_height))

            if self.highlight:
                highlight_x = self.rect.x - 5
                highlight_y = self.rect.y - 5
                highlight_color = (250, 250, 250)
                highlight_width = self.rect.width + 5
                highlight_height = self.rect.height + 5
                highlight_surface = pygame.Surface((highlight_width, highlight_height))
                pygame.draw.rect(highlight_surface, highlight_color, (0, 0, highlight_width, highlight_height))

                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(shadow_surface, (105, 10, 105), (2, 2, shadow_width, shadow_height))
                    pygame.draw.rect(highlight_surface, (205, 110, 205), (0, 0, highlight_width, highlight_height))
                    window.display.blit(shadow_surface, (shadow_x, shadow_y))
                    window.display.blit(highlight_surface, (highlight_x+2, highlight_y+2))
                    window.display.blit(self.surface, (self.rect.x+2, self.rect.y+2))
                else:
                    pygame.draw.rect(shadow_surface, shadow_color, (0, 0, shadow_width, shadow_height))

                    window.display.blit(shadow_surface, (shadow_x, shadow_y))
                    window.display.blit(highlight_surface, (highlight_x, highlight_y))
                    window.display.blit(self.surface, (self.rect.x, self.rect.y))



        #if self.rect.collidepoint(pygame.mouse.get_pos()):
            #pygame.draw.rect(self.surface, (195, 100, 195), (0, 0, self.width, self.height))
            #pygame.draw.rect((self.surface+5, self.surface+5), (195, 100, 195), (0, 0, self.width, self.height))
        #else:

            #pygame.draw.rect(self.surface, (66, 66, 66), (0, 0, self.width, self.height))




    def click(self, event, function=None, *args):
        if function is not None:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
                music.play_sfx(window.sfx_menu_confirm)
                function(*args)
