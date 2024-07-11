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

def quit_game():
    pygame.quit()
    sys.exit()



def menu():
    title = pygame.image.load('assets/Title4.png').convert_alpha()
    title_rect = title.get_rect()
    title_x = window.width / 2 - title.get_width() / 2
    title_y = window.height / 2 - title.get_height() / 2 + 25
    title_rect.x = round(title_x)
    title_rect.y = round(title_y)


    #title = pygame.transform.scale_by(title, 0.4)

    # BACKGROUND CLOUDS
    cloud_7_folder = 'assets/Background/clouds/Clouds 7/'
    background_1 = Background(cloud_7_folder + '/1.png', has_alpha=False)
    background_2 = Background(cloud_7_folder + '/2.png')
    background_3 = Background(cloud_7_folder + '/3.png')
    background_4 = Background(cloud_7_folder + '/4.png')

    start_button = Button2(centerx=window.center_width, centery=window.center_height + 80, text="Start", box=True)
    exit_button = Button2(centerx=window.center_width, centery=window.center_height + 80, text="Exit", row=2, box=False)

    stars = 360
    stars_speed = 600
    reverse_stars_direction = random.randint(0, 1)
    constellation = create_constellation(stars)

    # music.load('Menu')

    click_tick_counter = 0
    click_tick_delay = 0.5

    animation_tick_counter = 0
    animation_tick_delay = 0.1
    title_rotation_direction = 1
    title_angle = 0

    play_music('music-box', volume=0.2)

    def new_game(title_x, title_y, title):

        if title_x > -420:
            title_x -= delta.time() * 150
            title = pygame.transform.smoothscale(title, (title.get_width() + 1, title.get_height() + 1))
            title_y -= 0
            title_rect.x = round(title_x)
            title_rect.y = round(title_y)
        else:
            game.loop()

# ----------------------------------------------------------------------------------------------------------------------

    while True:
        #window.clock.tick(test_fps)
        #window.clock.tick(window.max_fps)

        click_tick_counter += delta.time()
        animation_tick_counter += delta.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if click_tick_counter > click_tick_delay:
                click_tick_counter = click_tick_delay
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if reverse_stars_direction == False:
                        reverse_stars_direction = True
                        click_tick_counter = 0
                    else:
                        reverse_stars_direction = False
                        click_tick_counter = 0
            Button2.click(start_button, event, new_game(title_x, title_y, title))
            #Button.click(difficulty_button, event, game.loop)
            #Button.click(difficulty_button, event, difficulty, title, constellation, stars_speed, reverse_stars_direction)
            Button2.click(exit_button, event, quit_game)

        #window.display.fill(window.background_color)
        #window.display.blit(bg, (0, 0))
        #render_constellation(constellation, stars_speed * delta.time(), reverse_stars_direction)
        #render_fps()

        # CLOUDS
        background_1.render()
        background_2.render()
        background_3.render_horizontal_scrolling(speed_mult=0.3)
        background_4.render_horizontal_scrolling(speed_mult=0.6)


        for button in (start_button, exit_button):
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
        render(title, title_rect)
        pygame.draw.rect(window.display, 'yellow', mouse.create_rect(20, 20))
    # ----------------------------------------------------------------------------------------------------------------------
        mouse.update_last_pos()
        window.draw()
        pygame.display.update()
        delta.time_update()
