import pygame
from data.config import *
from data.img import *
from data.player import Player


def testing():
    cloud_7_folder = 'assets/Background/clouds/Clouds 7/'

    background_1 = Background(cloud_7_folder+'/1.png')
    background_2 = Background(cloud_7_folder+'/2.png', has_alpha=True)
    background_3 = Background(cloud_7_folder+'/3.png', has_alpha=True, x=200)
    background_4 = Background(cloud_7_folder+'/4.png', has_alpha=True)
    foreground = Foreground('tiled_exports/Screenshot_1.png')
    player = Player('assets/Characters/2 Punk/Punk_idle.png', x=window.width/2, y=window.height/2)

# ----------------------------------------------------------------------------------------------------------------------

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        # --------------------------------------------------------------------------------------------------------------
        # UPDATE
        clock.tick(fps.max)

        delta.time_update()
        player.allow_movement()
        player.gravity()

        # --------------------------------------------------------------------------------------------------------------
        # DRAW

        background_1.render()
        background_2.render()
        background_3.render_horizontal_scrolling(speed_mult=0.3)
        background_4.render_horizontal_scrolling(speed_mult=0.6)
        foreground.render()
        player.update_rect_coords()
        player.render()

        fps.render()
        pygame.display.update()
