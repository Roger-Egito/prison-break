import pygame
from data.config import *
from data.img import *
from data.player import Player
from data.enemy import Enemy
from data.tile import Tile
from data.audio import *


def render_billboard(text, object):
    text = pygame.font.Font(None, 24).render(text, 1, 'white')
    rect = text.get_rect()
    setattr(rect, "midbottom", (object.center_x, object.y - 10))  # (window.width - 16, 32))
    pygame.draw.rect(window.display, 'black', (rect[0] - 5, rect[1] - 5, rect[2] + 10, rect[3] + 10))
    render(text, rect)

def testing():

    # ------------------------------------------------------------------------------------------------------------------
    # BACKGROUND

    # CLOUDS
    cloud_7_folder = 'assets/Background/clouds/Clouds 7/'
    background_1 = Background(cloud_7_folder+'/1.png', has_alpha=False)
    background_2 = Background(cloud_7_folder+'/2.png')
    background_3 = Background(cloud_7_folder+'/3.png')
    background_4 = Background(cloud_7_folder+'/4.png')
    #background_5 = Background('tiled_exports/caua.png')

    # SNOWY
    #snowy_folder = 'assets/Background/snowy/BG_04/'
    #background_1 = Background(snowy_folder+'Sky.png', has_alpha=False)
    #background_2 = Background(snowy_folder+'Moon.png')
    #background_3 = Background(snowy_folder+'BG.png')
    #background_4 = Background(snowy_folder+'Ground_01.png')
    #background_5 = Background(snowy_folder+'Ground_02.png')
    #background_6 = Background(snowy_folder+'Snow.png')
    #background_7 = Background('tiled_exports/caua.png')

    # ------------------------------------------------------------------------------------------------------------------
    # SPRITES

    # X and Y is the spawn point, you may want to change that to test maps
    player = Player('assets/Characters/2 Punk/Punk_idle.png', x=35, y=346, collision_offset=[2.5, 14], collision_dimensions=(20, 34))
    player.anim.walk = player.anim.populate('assets/Characters/2 Punk/Walk.png', image_count=6)
    player.anim.jump = player.anim.populate('assets/Characters/2 Punk/Punk_jump.png', image_count=4)
    player.anim.run = player.anim.populate('assets/Characters/2 Punk/Punk_run.png', image_count=6)
    player.anim.crouch = player.anim.populate('assets/Characters/2 Punk/Sitdown.png', image_count=3)

    ghost = Enemy('assets/Characters/ghost/ghost.png', sheet_sprite_dimensions=(6, 4, 14, 17))

    # ------------------------------------------------------------------------------------------------------------------
    # MUSIC

    play_music('assets/audio/bgm/groovy-ambient-funk-slowed.ogg', volume=volume.current)

# ----------------------------------------------------------------------------------------------------------------------

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        # --------------------------------------------------------------------------------------------------------------
        # UPDATE

        clock.tick(fps.max)
        volume.check_mute()
        delta.time_update()

        player.allow_movement()
        player.apply_gravity()
        player.update_collision()
        player.state_control()
        player.animate()

        ghost.move_to(player)

        # --------------------------------------------------------------------------------------------------------------
        # BACKGROUND

        # CLOUDS
        background_1.render()
        background_2.render()
        background_3.render_horizontal_scrolling(speed_mult=0.3)
        background_4.render_horizontal_scrolling(speed_mult=0.6)
        #background_5.render()

        # SNOWY
        #background_1.render()
        #background_2.render()
        #background_3.render()
        #background_4.render()
        #background_5.render()
        #background_6.render_vertical_scrolling()
        #background_7.render()

        stage.tile_group.draw(window.display)
        stage.decor_group.draw(window.display)

        # --------------------------------------------------------------------------------------------------------------
        # DEBUG STUFF


        #pygame.draw.rect(window.display, 'pink', (player.rect))
        #pygame.draw.rect(window.display, 'green', (player.collision.rect))
        #pygame.draw.rect(window.display, 'pink', (ghost.rect))

        #render_billboard(player.state, player.collision)

        # --------------------------------------------------------------------------------------------------------------
        # RENDER

        player.render()
        #ghost.render()
        fps.render()

        window.draw()
        pygame.display.update()
