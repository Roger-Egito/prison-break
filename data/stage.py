import math
import json

from data.tile import *
from data.img import Background
from data.config import window
from data.group import *
from data.audio import *
from pytmx.util_pygame import *

def is_obj_hor_flipped(obj):
    return is_last_bin_digit_one(bin(obj.gid))

def is_last_bin_digit_one(binary):
    if int(binary[-1]):
        return True
    else:
        return False

class stage:
    path = 'assets/maps/tmx/'
    extension = '.tmx'
    name = ''
    last = ''
    coords = None
    default_coords = None
    min_coords = (0, 0)
    max_coords = (0, 0)

    player_starting_coords = (0, 0)
    player_starting_flipped = False

    gm_tick_counter = 0
    lighting = True
    show_enemy_sight = False
    show_collisions = False

    tile_group = Group()
    darkness_group = Group()
    light_group = Group()
    lightsource_group = Group()
    decor_group = Group()
    foreground_group = Group()
    background_group = Group()
    enemy_group = Group()
    sound_group = Group()
    collision_group = Group()
    hiding_group = Group()
    interactive_group = Group()
    #x = 0
    #y = 0
    offset_x = 0
    offset_y = 0

    in_transition = False
    transition_speed = 0
    transition_default_speed = 1600
    transition_direction = (0,0)

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

    overlay = Background('assets/Background/overlays/6.png')
    overlay.img.fill((255, 255, 255, 60), None, pygame.BLEND_RGBA_MULT)

    @classmethod
    def get_pos(cls):
        pos = str(cls.coords[0]) + '-' + str(cls.coords[1])
        return pos

    @classmethod
    def get_data_file(cls):
        data_file = cls.path + cls.get_pos() + cls.extension
        return data_file

    @classmethod
    def get_data(cls):
        data = load_pygame(cls.get_data_file())
        return data

    @classmethod
    def render_billboard(cls, text, object, row=1, text_size=24, text_color='white', box_color='black', box=True, text_align="midbottom"):
        text = pygame.font.Font(None, text_size).render(text, 1, text_color)
        rect = text.get_rect()
        setattr(rect, text_align, (object.centerx, object.y - (11 * row + row * rect.height - rect.height - 1))) #((10 * row + ((row-1) * (rect.height+1))))))  # (window.width - 16, 32))
        if box:
            pygame.draw.rect(window.display, box_color, (rect[0] - 5, rect[1] - 5, rect[2] + 10, rect[3] + 10))
        render(text, rect)

    @classmethod
    def change(cls, hor=0, ver=0, instant=False, coords=None, player=None, speed=0, overwrite_player_direction=False):

        if coords:
            if cls.coords is None:
                cls.default_coords = list(coords)
            cls.coords = list(coords)

        if instant:
            cls.load(player, overwrite_player_direction=overwrite_player_direction)
        else:
            cls.start_transition(hor=hor, ver=ver, speed=speed, player=player)

        cls.set_name()

    @classmethod
    def clear(cls, player):
        cls.tile_group = Group()
        cls.decor_group = Group()
        cls.foreground_group = Group()
        cls.background_group = Group()
        cls.darkness_group = Group()
        cls.light_group = Group()
        cls.lightsource_group = Group()
        cls.enemy_group = Group()
        cls.collision_group = Group()
        cls.hiding_group = Group()
        cls.interactive_group = Group()
        cls.lightsource_group.add(player)

    @classmethod
    def set_name(cls):
        cls.last = cls.name
        filepath = cls.get_data_file()
        cls.name = filepath[len(cls.path):-len(cls.extension)]

    @classmethod
    def load(cls, player=None, overwrite_player_direction=False):
        play_music('safe')
        cls.clear(player)
        data = cls.get_data()

        cls.player_starting_coords = player.coords
        if overwrite_player_direction:
            player.flipped = cls.player_starting_flipped
        else:
            cls.player_starting_flipped = player.flipped

        try:
            for x, y, image in data.get_layer_by_name('Tiles').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=(cls.tile_group, cls.collision_group, cls.hiding_group), hca=False)
        except:
            pass

        try:
            for x, y, image in data.get_layer_by_name('Doors').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, type='Door', interactive=True, groups=(cls.tile_group, cls.collision_group, cls.hiding_group, cls.interactive_group))
        except:
            pass

        try:
            for x, y, image in data.get_layer_by_name('Decor').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=cls.decor_group)
        except:
            pass

        #TODO: Transform Foreground tile images into images with alpha, even when 100% opaque
        try:
            for x, y, image in data.get_layer_by_name('Foreground').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=(cls.foreground_group, cls.hiding_group))
        except:
            pass

        try:
            for x, y, image in data.get_layer_by_name('Background').tiles():
                coords = (x * 32, y * 32)
                image.fill((250, 250, 250, 255), None, pygame.BLEND_RGBA_MULT)
                #s = pygame.Surface((image.rect.width, image.rect.height))
                #s.set_alpha(200)
                #s.fill((0, 0, 30))
                Tile(coords=coords, image=image, groups=cls.background_group)

        except:
            pass



        try:
            for x, y, image in data.get_layer_by_name('Lights').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=(cls.light_group, cls.lightsource_group, cls.collision_group))
        except:
            pass

        try:
            for x, y, image in data.get_layer_by_name('Background').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=cls.darkness_group)
        except:
            pass

        try:
            from data.enemy import Enemy
            for enemy in data.get_layer_by_name('Enemies'):
                match enemy.type:
                    case 'Soldier':
                        flipped = is_obj_hor_flipped(enemy)
                        direction = -1 if flipped else 1
                        Enemy(img='assets/Characters/Enemy 2/Idle.png', name=enemy.name, type=enemy.type, x=enemy.x, y=enemy.y-enemy.height+64,
                                sheet_sprite_dimensions=(0, 0, enemy.width, enemy.height), speed_mult=0.5, size_mult=1.33,
                                collision_offset=[23, 58], collision_dimensions=(13, 38), ai='SOLDIER',
                                hor_dir=direction, flipped=flipped, light_radius=6, groups=(cls.enemy_group, cls.lightsource_group))  # collision_offset=[2.5, 14], collision_dimensions=(20, 34))
        except:
            pass

    @classmethod
    def start_transition(cls, hor=0, ver=0, speed=0, player=None):
        data = cls.get_data()
        cls.in_transition = True
        cls.transition_speed = speed if speed else cls.transition_default_speed
        cls.transition_direction = (hor, ver)

        try:
            for x, y, image in data.get_layer_by_name('Tiles').tiles():
                coords = (x * 32 + window.width * hor, y * 32 + window.height * ver)
                Tile(coords=coords, image=image, groups=(cls.tile_group, cls.collision_group, cls.hiding_group))
        except:
            print('No Tiles')

        try:
            for x, y, image in data.get_layer_by_name('Doors').tiles():
                coords = (x * 32 + window.width * hor, y * 32 + window.height * ver)
                Tile(coords=coords, image=image, type='Door', interactive=True, groups=(cls.tile_group, cls.collision_group, cls.hiding_group, cls.interactive_group))
        except:
            print('No Tiles')

        try:
            for x, y, image in data.get_layer_by_name('Decor').tiles():
                coords = (x * 32 + window.width * hor, y * 32 + window.height * ver)
                Tile(coords=coords, image=image, groups=cls.decor_group)
        except:
            print('No Decor')

        try:
            for x, y, image in data.get_layer_by_name('Foreground').tiles():
                coords = (x * 32 + window.width * hor, y * 32 + window.height * ver)
                Tile(coords=coords, image=image, groups=(cls.foreground_group, cls.hiding_group))
        except:
            print("No Foreground")

        try:
            for x, y, image in data.get_layer_by_name('Background').tiles():
                coords = (x * 32 + window.width * hor, y * 32 + window.height * ver)
                image.fill((250, 250, 250, 255), None, pygame.BLEND_RGBA_MULT)
                Tile(coords=coords, image=image, groups=cls.background_group)
        except:
            print("No Background")

        try:
            for x, y, image in data.get_layer_by_name('Lights').tiles():
                coords = (x * 32 + window.width * hor, y * 32 + window.height * ver)
                Tile(coords=coords, image=image, groups=(cls.light_group, cls.lightsource_group, cls.collision_group))
        except:
            print("No Lights")

        try:
            for x, y, image in data.get_layer_by_name('Background').tiles():
                coords = (x * 32 + window.width * hor, y * 32 + window.height * ver)
                Tile(coords=coords, image=image, groups=cls.darkness_group)
        except:
            print("Please insert background!")

        try:
            from data.enemy import Enemy
            for enemy in data.get_layer_by_name('Enemies'):
                match enemy.type:
                    case 'Soldier':
                        flipped = is_obj_hor_flipped(enemy)
                        direction = -1 if flipped else 1
                        Enemy(img='assets/Characters/Enemy 2/Idle.png', x=enemy.x + window.width * hor, y=enemy.y-enemy.height+64 + window.height * ver,
                                sheet_sprite_dimensions=(0, 0, enemy.width, enemy.height), speed_mult=0.5, size_mult=1.33,
                                collision_offset=[7, 48], collision_dimensions=(23, 48), ai='SOLDIER',
                                hor_dir=direction, flipped=flipped, light_radius=6, groups=(cls.enemy_group, cls.lightsource_group))  # collision_offset=[2.5, 14], collision_dimensions=(20, 34))
        except:
            pass

    @classmethod
    def update(cls, player):
        if cls.in_transition:
            hor = cls.transition_direction[0]
            ver = cls.transition_direction[1]
            speed = cls.transition_speed

            cls.move(hor=-hor, ver=-ver, speed=speed, player=player)

            if abs(cls.offset_x) >= window.width:
                cls.end_transition(player)

    @classmethod
    def end_transition(cls, player):
        cls.transition_speed = 0
        cls.transition_direction = (0,0)
        cls.offset_x = 0
        cls.load(player)
        cls.in_transition = False

    @classmethod
    def move(cls, hor=0, ver=0, speed=0, player=None, movePlayer=True):
        cls.tile_group.move(hor=hor, ver=ver, speed=speed)
        cls.light_group.move(hor=hor, ver=ver, speed=speed)
        cls.decor_group.move(hor=hor, ver=ver, speed=speed)
        cls.foreground_group.move(hor=hor, ver=ver, speed=speed)
        cls.background_group.move(hor=hor, ver=ver, speed=speed)
        cls.enemy_group.force_move(hor=hor, ver=ver, speed=speed)
        if player and movePlayer:
            player.force_move(hor_speed=hor*speed*0.9, ver_speed=ver*speed*0.95)
        cls.offset_x += hor * speed * delta.time()
        cls.offset_y += ver * speed * delta.time()

    @classmethod
    def transition_right(cls, player):
        if cls.coords[0] == cls.max_coords[0]:
            cls.coords[0] = cls.min_coords[0]
        else:
            cls.coords[0] += 1
        cls.change(player=player, hor=1)

    @classmethod
    def transition_left(cls, player):
        if cls.coords[0] == cls.min_coords[0]:
            cls.coords[0] = cls.max_coords[0]
        else:
            cls.coords[0] -= 1
        cls.change(player=player, hor=-1)

    @classmethod
    def transition_up(cls, player):
        if cls.coords[1] == cls.min_coords[1]:
            cls.coords[1] = cls.max_coords[1]
        else:
            cls.coords[1] -= 1
        cls.change(player=player, ver=1)

    @classmethod
    def transition_down(cls, player):
        if cls.coords[1] == cls.max_coords[1]:
            cls.coords[1] = cls.min_coords[1]
        else:
            cls.coords[1] += 1
        cls.change(player=player, ver=-1)

    @classmethod
    def background_render(cls, player):

        # CLOUDS
        #cls.background_1.render()
        #cls.background_2.render()
        #cls.background_3.render_horizontal_scrolling(speed_mult=0.3)
        #cls.background_4.render_horizontal_scrolling(speed_mult=0.6)
        #background_5.render()

        # SNOWY
        #background_1.render()
        #background_2.render()
        #background_3.render()
        #background_4.render()
        #background_5.render()
        #background_6.render_vertical_scrolling()
        #background_7.render()

        # ---

        cls.background_group.render()



        if cls.show_enemy_sight:
            for i in cls.enemy_group:
                pygame.draw.rect(window.display, i.random_color, i.vision.rect)

        window.gm_tick_counter += delta.time()
        if window.gm_tick_counter >= window.gm_tick_delay:
            window.gm_tick_counter = window.gm_tick_delay
            if pygame.key.get_pressed()[pygame.K_4]:
                window.gm_tick_counter = 0
                if not cls.show_collisions:
                    cls.show_collisions = True
                else:
                    cls.show_collisions = False

        if cls.show_collisions:
            pygame.draw.rect(window.display, 'pink', (player.rect))
            pygame.draw.rect(window.display, 'green' if not player.crouching else 'blue', (player.collision.rect))
            for i in stage.enemy_group:
                pygame.draw.rect(window.display, 'pink', (i.rect))
                pygame.draw.rect(window.display, 'green', (i.collision.rect))

        if player is not None:
            player.render()
            cls.enemy_group.render()
        else:
            print("aaahh, sumiu")

        cls.tile_group.render()
        cls.decor_group.render()
        cls.foreground_group.render()
        cls.overlay.render()
        for enemy in cls.enemy_group:
            if enemy.chasing:
                cls.render_billboard(text='!', object=enemy.collision.rect, text_size=64, text_color='red', box=False)
                enemy.light_radius = 12
            elif enemy.checking:
                enemy.light_radius = 6
                cls.render_billboard(text='?', object=enemy.collision.rect, text_size=64, text_color='yellow', box=False)
            else:
                enemy.light_radius = 0
        cls.light_group.render()


        #cls.render_billboard(str(player.state) + ' | ' + str(player.last_state), player.collision.rect)
        #cls.render_billboard(str(int(player.vector_x)) + ' | ' + str(int(player.vector_y)), player.collision.rect, row=2)
        #cls.render_billboard(str(player.airborne), player.collision.rect, row=3)
        #cls.render_billboard(str(player.sliding), player.collision.rect, row=4)
        #cls.render_billboard(str(player.close_to_interactive), player.collision.rect, row=1)

        window.gm_tick_counter += delta.time()
        if window.gm_tick_counter >= window.gm_tick_delay:
            window.gm_tick_counter = window.gm_tick_delay
            if pygame.key.get_pressed()[pygame.K_2]:
                window.gm_tick_counter = 0
                if cls.lighting:
                    cls.lighting = False
                else:
                    cls.lighting = True

        if cls.lighting:
            cls.background_group.update(cls.lightsource_group)
            cls.decor_group.update(cls.lightsource_group, is_tile=False)
            cls.tile_group.update(cls.lightsource_group)
            cls.foreground_group.update(cls.lightsource_group, is_foreground=True)
            cls.darkness_group.update(cls.lightsource_group, is_darkness=True)

        cls.light_group.update(cls.lightsource_group, is_tile=False)

        if window.gm_tick_counter >= window.gm_tick_delay:
            window.gm_tick_counter = window.gm_tick_delay
            if pygame.key.get_pressed()[pygame.K_3]:
                window.gm_tick_counter = 0
                if cls.show_enemy_sight:
                    cls.show_enemy_sight = False
                else:
                    cls.show_enemy_sight = True

        player.apply_gravity()
        player.allow_movement()
        player.update_collision()
        player.state_control()
        player.animate()
        player.sound_spheres.update()
        cls.enemy_group.animate()
        cls.enemy_group.state_control()
        cls.enemy_group.apply_gravity()
        cls.enemy_group.update_collision()
        cls.enemy_group.update_vision()
        cls.enemy_group.render_spheres()
        cls.enemy_group.ai_control(player)

        #for enemy in cls.enemy_group:
        #    cls.render_billboard('AB: ' + str(enemy.airborne), enemy.collision.rect)
            #cls.render_billboard('Y: ' + str(enemy.vector_y), enemy.collision.rect, text_align="midleft", row=1)
            #cls.render_billboard('X: ' + str(enemy.vector_x), enemy.collision.rect, text_align="midleft", row=2)
        #    cls.render_billboard(str(enemy.chasing), enemy.collision.rect, row=1)
        #    cls.render_billboard(str(enemy.checking), enemy.collision.rect, row=2)
        #    cls.render_billboard(str(enemy.wandering), enemy.collision.rect, row=3)
