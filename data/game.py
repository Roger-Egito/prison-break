import pygame
from data.renderer import *
from data.player import *
from data.audio import *
from data.stage import stage

#player = Player('assets/Characters/Enemy 2/Idle.png', x=160, y=160, sheet_sprite_dimensions=(0, 0, 96, 96), size_mult=1.25, collision_offset=[12, 48], collision_dimensions=(30, 48))  #collision_offset=[2.5, 14], collision_dimensions=(20, 34))
#soldier = Enemy(img='assets/Characters/Enemy 2/Idle.png', x=544, y=65, sheet_sprite_dimensions=(0, 0, 96, 96), speed_mult=0.5, size_mult=1.33, collision_offset=[12, 48], collision_dimensions=(30, 48), ai='SOLDIER', hor_dir=-1)  #collision_offset=[2.5, 14], collision_dimensions=(20, 34))
#play_music('assets/audio/bgm/safe-1.mp3', volume=volume.current)

player = Player(img='assets/Characters/2 Punk/Punk_idle.png', name='Player', x=128, y=224, collision_offset=[7, 14],
                collision_dimensions=(15, 34),
                multiple_idles=True,
                light_radius=6)

def start():
    player.x = 160
    player.y = 192
    player.vector_x = 0
    player.vector_y = 0
    stage.change(instant=True, coords=(0, 0), player=player)
    stage.min_coords = (0, 0)
    stage.max_coords = (6, 0)
    play_music('safe')
    loop()

restarting = False
restarting_tick_counter = 0

def stage_restart(death=False):
    global restarting
    if not restarting:
        if death:
            play_sfx('death', volume=0.12, fade_out=2000)
        else:
            play_sfx('stage-restart', volume=0.25, fade_out=3000)
        player.can_move = False
        restarting = True
        player.immortal = True
        noise.strong = True
        player.set_coords(stage.player_starting_coords)
        player.sliding = False
        player.crouch()
        player.stand()
        stage.change(instant=True, coords=stage.coords, player=player, overwrite_player_direction=True, death=death)


def end_restart():
    global restarting
    play_music('safe')
    noise.strong = False
    player.can_move = True
    restarting = False
    player.immortal = False

def game_over():
    global restarting
    if not restarting:
        play_sfx('death', volume=0.12, fade_out=2000)
        restarting = True
        player.immortal = True
        player.sliding = False
        noise.strong = True
        player.set_coords(player.default_coords)
        stage.change(instant=True, coords=stage.default_coords, player=player, overwrite_player_direction=True)


def loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        if restarting:
            global restarting_tick_counter
            restarting_tick_counter += 1 * delta.time()
            if restarting_tick_counter >= 0.4:
                end_restart()
                restarting_tick_counter = 0



        render_game(player)
