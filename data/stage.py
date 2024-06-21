from data.tile import *
from data.img import Background
from data.config import window
from pytmx.util_pygame import *


class stage:
    path = 'assets/maps/tmx/'
    extension = '.tmx'
    name = ''
    last = ''
    tile_group = pygame.sprite.Group()
    decor_group = pygame.sprite.Group()
    foreground_group = pygame.sprite.Group()
    background_group = pygame.sprite.Group()
    x = 0
    y = 0

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

    @classmethod
    def clear(cls):
        cls.tile_group = pygame.sprite.Group()
        cls.decor_group = pygame.sprite.Group()
        cls.foreground_group = pygame.sprite.Group()
        cls.background_group = pygame.sprite.Group()

    @classmethod
    def remove_out_of_bounds_tiles(cls, window):
        removedTiles = 0
        tiles = cls.tile_group.sprites()
        decors = cls.decor_group.sprites()
        foreground = cls.foreground_group.sprites()
        background = cls.background_group.sprites()

        for tile in tiles:
            if tile.rect.x < 0:
                cls.tile_group.remove(tile)
                removedTiles += 1
            elif tile.rect.x > window.width:
                cls.tile_group.remove(tile)
                removedTiles += 1
            elif tile.rect.y < 0:
                cls.tile_group.remove(tile)
                removedTiles += 1
            elif tile.rect.y > window.height:
                cls.tile_group.remove(tile)
                removedTiles += 1

        for back in background:
            if back.rect.x < 0:
                cls.background_group.remove(back)
                removedTiles += 1
            elif back.rect.x > window.width:
                cls.background_group.remove(back)
                removedTiles += 1
            elif back.rect.y < 0:
                cls.background_group.remove(back)
                removedTiles += 1
            elif back.rect.y > window.height:
                cls.background_group.remove(back)
                removedTiles += 1

        for fore in foreground:
            if fore.rect.x < 0:
                cls.foreground_group.remove(fore)
                removedTiles += 1
            elif fore.rect.x > window.width:
                cls.foreground_group.remove(fore)
                removedTiles += 1
            elif fore.rect.y < 0:
                cls.foreground_group.remove(fore)
                removedTiles += 1
            elif fore.rect.y > window.height:
                cls.foreground_group.remove(fore)
                removedTiles += 1

        for decor in decors:
            if decor.rect.x < 0:
                cls.decor_group.remove(decor)
                removedTiles += 1
            elif decor.rect.x > window.width:
                cls.decor_group.remove(decor)
                removedTiles += 1
            elif decor.rect.y < 0:
                cls.decor_group.remove(decor)
                removedTiles += 1
            elif decor.rect.y > window.height:
                cls.decor_group.remove(decor)
                removedTiles += 1
        print(removedTiles)




    @classmethod
    def set_name(cls, filepath):
        cls.last = cls.name
        cls.name = filepath[len(cls.path):-len(cls.extension)]

    @classmethod
    def load(cls, filepath):
        #TODO: Check pygame's sprite.LayeredUpdates

        cls.clear()
        file = load_pygame(filepath)

        try:
            for x, y, image in file.get_layer_by_name('Tiles').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=cls.tile_group)
        except:
            pass

        try:
            for x, y, image in file.get_layer_by_name('Decor').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=cls.decor_group)
        except:
            pass

        try:
            for x, y, image in file.get_layer_by_name('Foreground').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=cls.foreground_group)
        except:
            pass

        try:
            for x, y, image in file.get_layer_by_name('Background').tiles():
                coords = (x * 32, y * 32)
                Tile(coords=coords, image=image, groups=cls.background_group)
        except:
            pass

    @classmethod
    def transition(cls, filepath, left = False):
        file = load_pygame(filepath)
        if not left:
            for x, y, image in file.get_layer_by_name('Tiles').tiles():
                coords = (x * 32 + window.width, y * 32)
                Tile(coords=coords, image=image, groups=cls.tile_group)

            try:
                for x, y, image in file.get_layer_by_name('Decor').tiles():
                    coords = (x * 32 + window.width, y * 32)
                    Tile(coords=coords, image=image, groups=cls.decor_group)
            except ValueError:
                print('huh')
            try:
                for x, y, image in file.get_layer_by_name('Foreground').tiles():
                    coords = (x * 32 + window.width, y * 32)
                    Tile(coords=coords, image=image, groups=cls.foreground_group)
            except:
                print("No foreground")

            try:
                for x, y, image in file.get_layer_by_name('Background').tiles():
                    coords = (x * 32 + window.width, y * 32)
                    Tile(coords=coords, image=image, groups=cls.background_group)
            except:
                print("No background")
        else:
            for x, y, image in file.get_layer_by_name('Tiles').tiles():
                coords = (x * 32 - window.width, y * 32)
                Tile(coords=coords, image=image, groups=cls.tile_group)

            try:
                for x, y, image in file.get_layer_by_name('Decor').tiles():
                    coords = (x * 32 - window.width, y * 32)
                    Tile(coords=coords, image=image, groups=cls.decor_group)
            except ValueError:
                print('huh')
            try:
                for x, y, image in file.get_layer_by_name('Foreground').tiles():
                    coords = (x * 32 - window.width, y * 32)
                    Tile(coords=coords, image=image, groups=cls.foreground_group)
            except:
                print("No foreground")

            try:
                for x, y, image in file.get_layer_by_name('Background').tiles():
                    coords = (x * 32 - window.width, y * 32)
                    Tile(coords=coords, image=image, groups=cls.background_group)
            except:
                print("No background")

    @classmethod
    def move(cls, width, lefttoright = False):
        if lefttoright:
            step = -2
        else:
            step = 2
        #if stage.name == 'Screenshot1':
        cls.tile_group.update(-step)
        cls.decor_group.update(-step)
        cls.foreground_group.update(-step)
        cls.background_group.update(-step)
        cls.x -= step
        print(cls.x)
        return -cls.x
        #elif stage.name == 'Screenshot2':
            # cls.tile_group.update(step)
            # cls.decor_group.update(step)
            # cls.foreground_group.update(step)
            # cls.background_group.update(step)
            # cls.x += step

    @classmethod
    def render(cls, player):
        # CLOUDS
        cls.background_1.render()
        cls.background_2.render()
        cls.background_3.render_horizontal_scrolling(speed_mult=0.3)
        cls.background_4.render_horizontal_scrolling(speed_mult=0.6)
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

        cls.decor_group.draw(window.display)
        cls.background_group.draw(window.display)
        if player is not None:
            player.render()
        cls.tile_group.draw(window.display)
        cls.foreground_group.draw(window.display)

    # This version will make EVERY tile have collision. You can uncomment the code below to put the layers you want to
    # not have collision inside decor_group
    #for layer in file.layers:
    #    if isinstance(layer, pytmx.TiledTileLayer):                 # Alternative: if hasattr(layer, 'data'):
    #       for x, y, image in layer.tiles():
    #           coords = (x * 32, y * 32)
    #           Tile(coords=coords, image=image, groups=tile_group)

    #tiles = file.get_layer_by_name('Tiles')
    #decor = file.get_layer_by_name('Decor')
    #foreground = file.get_layer_by_name('Foreground')


    #for x, y, image in file.layers[2].tiles():
    #    coords = (x * 32, y * 32)
    #    Tile(coords=coords, image=image, groups=foreground_group)
#
    #for x, y, image in file.layers[1].tiles():
    #    coords = (x * 32, y * 32)
    #    Tile(coords=coords, image=image, groups=tile_group)
##
    #for x, y, image in file.layers[0].tiles():
    #    coords = (x * 32, y * 32)
    #    Tile(coords=coords, image=image, groups=decor_group)