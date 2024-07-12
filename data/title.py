import pygame
import sys
import random
from data.config import window, delta
from data.button import *
from data.star import *
#from fps_counter import render_fps
import data.game as game
from data.img import Background
#from difficulty import difficulty
#import timer
from data.audio import *
from data.sprite import Sprite
from data.stage import stage
from data.renderer import *

def quit_game():
    pygame.quit()
    sys.exit()



class menu:
    title = pygame.image.load('assets/Title4.png').convert_alpha()
    title_rect = title.get_rect()
    title_x = window.width / 2 - title.get_width() / 2
    title_y = window.height / 2 - title.get_height() / 2 + 25
    title_rect.x = round(title_x)
    title_rect.y = round(title_y)

    player = Sprite(img='assets/Characters/2 Punk/Punk_death.png', name='Title_player', x=120, y=230, collision_offset=[7, 14],
                    collision_dimensions=(15, 34),
                    multiple_idles=False,
                    light_radius=6,
                    sheet=True,
                    sheet_image_count=6,
                    sheet_default=5)
    player.horizontal_flip()

    #title = pygame.transform.scale_by(title, 0.4)

    # BACKGROUND CLOUDS
    #cloud_7_folder = 'assets/Background/clouds/Clouds 7/'
    #background_1 = Background(cloud_7_folder + '/1.png', has_alpha=False)
    #background_2 = Background(cloud_7_folder + '/2.png')
    #background_3 = Background(cloud_7_folder + '/3.png')
    #background_4 = Background(cloud_7_folder + '/4.png')

    start_button = Button2(centerx=window.center_width, centery=window.center_height + 80, text="Start", box=True)
    exit_button = Button2(centerx=window.center_width, centery=window.center_height + 80, text="Exit", row=1, box=False)

    #stars = 360
    #stars_speed = 600
    #reverse_stars_direction = random.randint(0, 1)
    #constellation = create_constellation(stars)

    # music.load('Menu')

    #click_tick_counter = 0
    #click_tick_delay = 0.5

    #animation_tick_counter = 0
    #animation_tick_delay = 0.1
    #title_rotation_direction = 1
    #title_angle = 0
    game_starting = False
    game_started = False

    stage.change(instant=True, coords=(0, 0), player=player)
    stage.min_coords = (0, 0)
    stage.max_coords = (6, 0)

    @classmethod
    def new_game(cls):
        fadeout_music(2000)
        #play_sfx('caution', stinger=True, volume=0.5, fade_ms=3000, fade_out=10000)
        cls.game_starting = True
        noise.strong = False
        #game.start()

    @classmethod
    def title_woosh(cls):
        if cls.title_y > -400:
            cls.title_y -= delta.time() * 300
            cls.title_rect.y = round(cls.title_y)
            cls.start_button.centery += delta.time() * 300
            cls.start_button.rect.y = round(cls.start_button.y)
            cls.exit_button.centery += delta.time() * 300
            cls.exit_button.rect.y = round(cls.start_button.y)
        else:
            cls.game_starting = False
            cls.game_started = True
            noise.strong = False
            game.start()

# ----------------------------------------------------------------------------------------------------------------------
def screen(ng2=False):
    play_music('somber')

    while True:
        if menu.game_starting:
            menu.title_woosh()

        if menu.game_started:
            menu.title_y = window.height / 2 - menu.title.get_height() / 2 + 25
            menu.title_rect.y = round(menu.title_y)
            menu.start_button.centery = window.center_height + 80
            menu.exit_button.centery = window.center_height + 80
            menu.start_button.rect.y = round(menu.start_button.y)
            menu.exit_button.rect.y = round(menu.exit_button.y)
            stage.change(instant=True, coords=(0, 0), player=menu.player)
            stage.min_coords = (0, 0)
            stage.max_coords = (6, 0)
            menu.game_started = False

        if ng2:
            noise.strong = True
            play_music('alert', fade_in=100)
            ng2 = False

        #menu.click_tick_counter += delta.time()
        #menu.animation_tick_counter += delta.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            #if menu.click_tick_counter > menu.click_tick_delay:
            #    menu.click_tick_counter = menu.click_tick_delay
            #    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #        if menu.reverse_stars_direction == False:
            #            menu.reverse_stars_direction = True
            #            menu.click_tick_counter = 0
            #        else:
            #            menu.reverse_stars_direction = False
            #            menu.click_tick_counter = 0
            Button2.click(menu.start_button, event, menu.new_game)#new_game(title_x, title_y, title))
            #Button.click(difficulty_button, event, game.loop)
            #Button.click(difficulty_button, event, difficulty, title, constellation, stars_speed, reverse_stars_direction)
            Button2.click(menu.exit_button, event, quit_game)

        #window.display.fill(window.background_color)
        #window.display.blit(bg, (0, 0))
        #render_constellation(constellation, stars_speed * delta.time(), reverse_stars_direction)
        #render_fps()

        # CLOUDS
        #menu.background_1.render()
        #menu.background_2.render()
        #menu.background_3.render_horizontal_scrolling(speed_mult=0.3)
        #menu.background_4.render_horizontal_scrolling(speed_mult=0.6)

        stage.background_render(menu.player)
        noise.render()

        for button in (menu.start_button, menu.exit_button):
            Button2.render(button)

        #if title_rotation_direction == 1:
        #    title = pygame.transform.rotate(title, -0.5)
        #    title_angle -= 0.5
        #    if title_angle < -50:
        #        title_angle = 0
        #        title_rotation_direction = -1
        #else:
        #    title = pygame.transform.rotate(title, 0.5)
        #    title_angle += 0.5
        #    if title_angle > 100:
        #        title_angle = 0
        #        title_rotation_direction = 1

        #title = pygame.transform.scale_by(title, 1.01)

        #Until around 420


        #if animation_tick_counter >= animation_tick_delay:
        #    animation_tick_counter = 0
        #    title = pygame.transform.scale_by(title, 1.01)
        #render(title, (window.width / 2 - title.get_width() / 2, window.height / 2 - title.get_height() / 2 + 25))
        render(menu.title, menu.title_rect)
        #pygame.draw.rect(window.display, 'yellow', mouse.create_rect(20, 20))
    # ----------------------------------------------------------------------------------------------------------------------
        mouse.update_last_pos()
        window.draw()
        pygame.display.update()
        delta.time_update()
