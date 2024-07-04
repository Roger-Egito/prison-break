import pygame
from data.config import *
from data.stage import *
from data.img import *
from data.player import Player
from data.enemy import Enemy
from data.tile import Tile
from data.hearing import *
from data.audio import *
from data.light import *

def render_billboard(text, object):
    text = pygame.font.Font(None, 24).render(text, 1, 'white')
    rect = text.get_rect()
    setattr(rect, "midbottom", (object.center_x, object.y - 10))  # (window.width - 16, 32))
    pygame.draw.rect(window.display, 'black', (rect[0] - 5, rect[1] - 5, rect[2] + 10, rect[3] + 10))
    render(text, rect)

def render_billboard_2(text, object):
    text = pygame.font.Font(None, 24).render(text, 1, 'white')
    rect = text.get_rect()
    setattr(rect, "midbottom", (object.center_x, object.y - 30))  # (window.width - 16, 32))
    pygame.draw.rect(window.display, 'black', (rect[0] - 5, rect[1] - 5, rect[2] + 10, rect[3] + 10))
    render(text, rect)

def render_billboard_3(text, object):
    text = pygame.font.Font(None, 24).render(text, 1, 'white')
    rect = text.get_rect()
    setattr(rect, "midbottom", (object.center_x, object.y - 50))  # (window.width - 16, 32))
    pygame.draw.rect(window.display, 'black', (rect[0] - 5, rect[1] - 5, rect[2] + 10, rect[3] + 10))
    render(text, rect)

def render_debug_sprite_information(text, x=25, y=25):
    text = pygame.font.Font(None, 24).render(text, 1, 'white')
    rect = text.get_rect()
    setattr(rect, "midleft", (x, y))  # (window.width - 16, 32))
    #pygame.draw.rect(window.display, 'black', (rect[0] - 5, rect[1] - 5, rect[2] + 10, rect[3] + 10))
    render(text, rect)

def testing():

    # ------------------------------------------------------------------------------------------------------------------
    # BACKGROUND

    #stage.load('assets/maps/tmx/Screenshot1.tmx')
    #stage.set_name('assets/maps/tmx/Screenshot1.tmx')

    #stage.load('assets/maps/tmx/Testing6.tmx')
    #stage.load('assets/maps/tmx/Testing3.tmx')
    #stage.load('assets/maps/tmx/Testing7.tmx')

    stage.load('assets/maps/tmx/0-0.tmx')
    stage.set_name('assets/maps/tmx/0-0.tmx')
    
    light_group = pygame.sprite.Group()
    sun = Light(x=32, y=-50, radius=10, groups=light_group)

    # ------------------------------------------------------------------------------------------------------------------
    # SPRITES

    # X and Y is the spawn point, you may want to change that to test maps
    # Bottom = x=254, y=344 <- Ignore this
    # Top = x=32, y=-50 <- Ignore this
    #player = Player('assets/Characters/2 Punk/Punk_idle.png', x=32, y=-50, collision_offset=[7, 14], collision_dimensions=(15, 34))  #collision_offset=[2.5, 14], collision_dimensions=(20, 34))
    #player = Player('assets/Characters/Soldier_1/Temp.png', x=32, y=-50, collision_offset=[7, 14], collision_dimensions=(15, 34))  #collision_offset=[2.5, 14], collision_dimensions=(20, 34))
    player = Player('assets/Characters/2 Punk/Punk_idle.png', x=10, y=160, collision_offset=[7, 14], collision_dimensions=(15, 34))  #collision_offset=[2.5, 14], collision_dimensions=(20, 34))

    player.anim.walk = player.anim.populate('assets/Characters/2 Punk/Walk.png', image_count=6)
    player.anim.jump = player.anim.populate('assets/Characters/2 Punk/Punk_jump.png', image_count=4)
    player.anim.run = player.anim.populate('assets/Characters/2 Punk/Punk_run.png', image_count=6)
    player.anim.crouch = player.anim.populate('assets/Characters/2 Punk/Sitdown.png', image_count=3)
    player.anim.hang = player.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
    player.anim.h_crouch = player.anim.populate('assets/Characters/2 Punk/HCWalk.png', image_count=2)
    player.anim.h_fall = player.anim.populate('assets/Characters/2 Punk/Happy.png', image_count=6)
    player.anim.s_jump = player.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
    #player.anim.h_jump = player.anim.populate('assets/Characters/2 Punk/Pullup.png', image_count=6, dimensions=(0, 41, 48, 48))
    player.anim.h_walk = player.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
    player.anim.hc_walk = player.anim.populate('assets/Characters/2 Punk/HCWalk.png', image_count=2)
    player.anim.h_jump = player.anim.populate('assets/Characters/2 Punk/Punk_doublejump.png', image_count=6)
    player.anim.slide = player.anim.img('assets/Characters/2 Punk/Slide.png')
    #player.anim.slide = player.anim.img('assets/Characters/Soldier_1/Temp.png')
    player.anim.idle2 = player.anim.populate('assets/Characters/2 Punk/Talk.png', image_count=6)
    player.anim.idle3 = player.anim.populate('assets/Characters/2 Punk/Use.png', image_count=6)
    player.anim.idle4 = player.anim.populate('assets/Characters/2 Punk/Happy.png', image_count=6)
    player.anim.idle5 = player.anim.populate('assets/Characters/2 Punk/Idle2.png', image_count=4)

    #ghost = Enemy('assets/Characters/ghost/ghost.png', sheet_sprite_dimensions=(6, 4, 14, 17))

    # ------------------------------------------------------------------------------------------------------------------
    # MUSIC

    #play_music('assets/audio/bgm/groovy-ambient-funk-slowed.ogg', volume=volume.current)
    play_music('assets/audio/bgm/somber.mp3', volume=volume.current)

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

        player.apply_gravity()
        player.allow_movement()
        player.update_collision()
        player.state_control()
        player.animate()

        #ghost.move_to(player)

        # --------------------------------------------------------------------------------------------------------------
        # DEBUG STUFF

        #pygame.draw.rect(window.display, 'pink', (ghost.rect))

        # --------------------------------------------------------------------------------------------------------------
        # RENDER

        #ghost.render()
        fps.render()

        # DEBUG FOREGROUND
        #render_billboard_2(player.last_state, player.collision)

        #player.collision.render_light_circle()
        stage.background_render()
        stage.foreground_render()
        stage.background_group.update(method=0)
        stage.background_group.update(method=2, new_group=stage.tile_group_lighted, light_radius=player.collision.l_radius, object=player, coords=(player.collision.rect.centerx, player.collision.rect.centery))
        stage.decor_group.update(method=0, decor_group=True)
        stage.decor_group.update(method=2, new_group=stage.tile_group_lighted, light_radius=player.collision.l_radius, object=player, coords=(player.collision.rect.centerx, player.collision.rect.centery))

        #pygame.draw.rect(window.display, 'pink', (player.rect))
        #pygame.draw.rect(window.display, 'green' if not player.crouching else 'blue', (player.collision.rect))
        player.render()
        stage.tile_group.update(method=0)
        stage.tile_group.update(method=2, new_group=stage.tile_group_lighted, light_radius=player.collision.l_radius, object=player, coords=(player.collision.rect.centerx, player.collision.rect.centery))
        stage.tile_group.update(method=0)

        stage.foreground_group.update(method=0)
        stage.foreground_group.update(method=2, new_group=stage.tile_group_lighted, light_radius=player.collision.l_radius, object=player, coords=(player.collision.rect.centerx, player.collision.rect.centery))

        player.sound_spheres.update()



        #render_billboard(player.state, player.collision)

        #render_debug_sprite_information("X: %0.2f Y: %0.2f VX: %0.2f VY: %0.2f DT: %0.2f" % (round(player.x, 2), round(player.y, 2), round(player.vector_x, 2), round(player.vector_y, 2), delta.time()))
        #render_debug_sprite_information(str(player.on_wall), 25, 50)

        window.draw()
        pygame.display.update()
