import pygame


def play_music(file_path, volume=1, loops=-1, start=0, fade_in=1000):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops, start, fade_in)


def pause_music():
    pygame.mixer.music.pause()


def resume_music():
    pygame.mixer.music.unpause()

# ---

def play_sfx(file_path):
    sfx = pygame.mixer.Sound(file_path)
    sfx.play()
