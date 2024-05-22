import pygame
from data.config import *
from data.img import *
from data.player import Player
from data.enemy import Enemy
from data.audio import *
from data.anim import Anim

def testing():
    cloud_7_folder = 'assets/Background/clouds/Clouds 7/'

    background_1 = Background(cloud_7_folder+'/1.png')
    background_2 = Background(cloud_7_folder+'/2.png', has_alpha=True)
    background_3 = Background(cloud_7_folder+'/3.png', has_alpha=True)
    background_4 = Background(cloud_7_folder+'/4.png', has_alpha=True)
    background_5 = Background('tiled_exports/Screenshot_1.png', has_alpha=True)
    player = Player('assets/Characters/2 Punk/Punk_idle.png', x=window.width/2, y=window.height/2, sheet_step=2.4)
    player.anim.walk = player.anim.populate('assets/Characters/2 Punk/Walk.png', step=2.4, image_count=6)
    player.anim.jump = player.anim.populate('assets/Characters/2 Punk/Punk_jump.png', step=1.6, image_count=4, dimensions=(0, 10, 30, 34))
    player.anim.run = player.anim.populate('assets/Characters/2 Punk/Punk_run.png', step=2.4, image_count=6)
    player.anim.crouch = player.anim.populate('assets/Characters/2 Punk/Sitdown.png', step=2.4, image_count=3)
    ghost = Enemy('assets/Characters/ghost/ghost.png', sheet_sprite_dimensions=(6, 4, 14, 17))

    #test = player.sheet_to_imgs(dimensions=(4, 14, 20, 34), image_count=4, step=2.4)
    #player.anim = Anim(test)

    play_music('assets/audio/bgm/groovy-ambient-funk-slowed.ogg', volume=0.2)

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
        background_5.render()

        ghost.move_to(player)

        if player.state == player.States.IDLE:
            player.change_image(player.anim.next(player.anim.idle))
        elif player.state == player.States.WALKING:
            player.change_image(player.anim.next(player.anim.walk))
        elif player.state == player.States.JUMPING:
            player.change_image(player.anim.next(player.anim.jump))
        elif player.state == player.States.RUNNING:
            player.change_image(player.anim.next(player.anim.run, speed_mult=2))
        elif player.state == player.States.CROUCHING:
            player.change_image(player.anim.next(player.anim.crouch, loop=False))

        player.update_rect_coords()

        # DEBUG RECTANGLES
        #pygame.draw.rect(window.display, 'pink', (player.rect))
        #pygame.draw.rect(window.display, 'pink', (ghost.rect))

        player.render()
        ghost.render()
        fps.render()

        text = pygame.font.Font(None, 24).render(player.state, 1, 'white')
        rect = text.get_rect()
        setattr(rect, "midbottom", (player.center_x, player.y - 10)) #(window.width - 16, 32))
        pygame.draw.rect(window.display, 'black', (rect[0]-5, rect[1]-5, rect[2]+10, rect[3]+10))
        render(text, rect)

        pygame.display.update()