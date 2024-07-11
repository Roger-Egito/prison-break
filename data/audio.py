import pygame

music = ''

def play_music(file_name, volume=1, loops=-1, start=0, fade_in=0, extension='mp3'):
    global music
    if music != file_name:
        path = 'assets/audio/bgm/'
        extension = '.'+extension
        if music == 'action' and file_name == 'safe':
            play_sfx('deescalate', channel=3, volume=0.5)
        pygame.mixer.music.load(path + file_name + extension)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops, start, fade_in)
        music = file_name

def pause_music():
    pygame.mixer.music.pause()


def resume_music():
    pygame.mixer.music.unpause()

# ---

def play_sfx(file_name, volume=1, fade_ms=0, fade_out=0, extension='mp3', channel=-1):
    path = 'assets/audio/sfx/'
    extension = '.'+extension
    if channel >= 0:
        channel = pygame.mixer.Channel(channel)
        sfx = pygame.mixer.Sound(path + file_name + extension)
        sfx.set_volume(volume)
        channel.play(sfx, fade_ms=fade_ms)
    else:
        sfx = pygame.mixer.Sound(path + file_name + extension)
        sfx.set_volume(volume)
        sfx.play(fade_ms=fade_ms)
    if fade_out:
        sfx.fadeout(fade_out)
