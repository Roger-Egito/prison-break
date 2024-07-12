import pygame
from data.config import window, render
from data.text import write
from data.audio import play_sfx
import sys
from data.audio import music
import data.mouse as mouse

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
                play_sfx('cursor-hover')
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse.pos()):
                #music.play_sfx(window.sfx_menu_confirm)
                function(*args)


class Button2:
    def __init__(self, text='', centerx=window.width/2, centery=window.height/2, row=0, row_spacing=50, text_size=32, text_color='white', box_color='black', box=True, shadow=False, border=True, border_px=2, border_color='black', text_align="topleft"):
        self.text = text
        #self.bigger_text_render = write(text, border=border, font_size=text_size+5, font_color=text_color, border_color=border_color, border_px=border_px)
        #self.shadow = pygame.font.Font(None, text_size).render(text, 1, 'black') if shadow else False
        self.border = border
        self.border_px = border_px
        self.border_color = border_color
        self.centerx = centerx
        self.centery = centery
        self.row = row
        self.row_spacing = row_spacing
        self.text_size = text_size
        self.text_color = text_color
        self.box_color = box_color
        self.box = box
        self.text_align = text_align

        self.rect = write(self.text, border=self.border, font_size=self.text_size + 5, font_color=self.text_color,
                  border_color=self.border_color,
                  border_px=self.border_px, x=self.centerx, y=self.centery + (self.row * self.row_spacing), draw=False)

        #setattr(self.rect, self.text_align, (self.x, (self.y + ((self.row-1) * self.row_spacing))))
        #setattr(self.bigger_rect, self.text_align, (self.x, (self.y + ((self.row-1) * self.row_spacing))))
        #self.label = write(text, border=border, font_size=text_size, font_color=text_color, border_color=border_color, border_px=border_px)
        #self.big_label = write(text, border=border, font_size=text_size+5, font_color=text_color, border_color=border_color, border_px=border_px)


    @property
    def x(self):
        return self.centerx - self.width / 2

    @property
    def y(self):
        return self.centery - self.height / 2

    @property
    def selected_text_size(self):
        return self.text_size + 5

    #def alter_text(self, size=None):        # Obviously this method is incomplete, but I will be completing it as necessary
    #    if size is not None:
    #        self.text_size = size
    #    self.text_render = write(self.text, border=self.border, font_size=self.text_size, font_color=self.text_color, border_color=self.border_color, border_px=self.border_px)
    #    self.rect = self.text_render.get_rect()
    #    setattr(self.rect, self.text_align, (self.x, (self.y + ((self.row-1) * self.row_spacing))))

    def render(self):   #((10 * row + ((row-1) * (rect.height+1))))))  # (window.width - 16, 32))
        if self.rect.collidepoint(mouse.pos()):
            self.rect = write(self.text, border=self.border, font_size=self.text_size + 5, font_color=self.text_color,
                  border_color=self.border_color,
                  border_px=self.border_px, x=self.centerx, y=self.centery + (self.row * self.row_spacing))
            if self.rect.collidepoint(window.mouse_last_position) is False:
                play_sfx('cursor-hover', fade_out=1000)
        else:
            write(self.text, border=self.border, font_size=self.text_size, font_color=self.text_color,
                  border_color=self.border_color,
                  border_px=self.border_px, x=self.centerx, y=self.centery + (self.row * self.row_spacing))





    def click(self, event, function=None, *args):
        if function is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.Rect.collidepoint(self.rect, mouse.pos()):
                    function(*args)

    # ---

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    # ---

    @property
    def center(self):
        center = (self.centerx, self.centery)
        return center

    #@property
    #def center_width(self):
    #    return round(self.width / 2)
#
    #@property
    #def center_height(self):
    #    return round(self.height / 2)
#
    #@property
    #def center_x(self):
    #    return round(self.x + self.center_width)
#
    #@property
    #def center_y(self):
    #    return round(self.y + self.center_height)
#
    #def set_center(self, coordinate):
    #    self.x = coordinate[0] - round(self.width / 2)
    #    self.y = coordinate[1] - round(self.height / 2)

    # ---