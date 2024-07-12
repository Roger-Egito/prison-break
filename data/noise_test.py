
#!/usr/bin/env python3

"""
WARNING:    CAN TRIGGER EPILEPSY, ESPECIALLY IF ZOOMED IN !
This is a very stupid white noise generator.
It simulates a TV screen's static noise so that you can display it onto a screen
and make it look like a TV.
I made it because I like that effect and couldn't find an app for it, but only shitty GIFs that aren't really random.
CONTROLS:
    - SPACE BAR to "pause" the generation of static.
    - MOUSE SCROLL to "zoom" into the picture. Essentially make the "pixels" bigger or smaller.
    - LEFT MOUSE CLICK to cycle between different upsampling algorithms.
       This will change the crispiness and aspects of the "zoomed" pixels. Has no effect when fully unzoomed.
Samuel Prevost 2021-12-09
"""

from itertools import cycle
import pygame
from PIL import Image
import numpy as np

# Adjust for you screen size
width = 2048
height = 1152

def gen_rand_frame(w, h, pixel_ratio=2, resample=Image.BICUBIC):
    assert pixel_ratio >= 1
    small_w, small_h = w//pixel_ratio, h//pixel_ratio
    im = Image.fromarray((np.random.rand(small_h, small_w, 1) * 255).astype(np.uint8).repeat(3,2))
    im = im.resize((w, h), resample=resample)
    return pygame.image.fromstring(im.tobytes(), im.size, im.mode)


pygame.init()
resamples = cycle([
        Image.NEAREST, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS
        ])
resample = next(resamples)
# There can be anywhere from 1:1 pixel on screen vs in the image, up to only one big pixel for the whole image.
pixel_ratio_range = (1, min(height, width))
pixel_ratio = 5

screen = pygame.display.set_mode((width, height))
frame = gen_rand_frame(width, height, pixel_ratio, resample)
fpsClock = pygame.time.Clock()

running = True
paused = False

while running:
    if not paused:
        #screen.fill((0,0,50))
        screen.blit(frame, (0, 0))
        frame = gen_rand_frame(width, height, pixel_ratio, resample)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            paused = not paused

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                resample = next(resamples)
            elif event.button == 4:  # scroll up
                # We need the zoom "speed" to be proportional to the zoom level as
                # the pixel density increases/decreases quadratically (area is h x w)
                # hence if you zoom a lot, the steps will look like exponentials and it will
                # feel intuitive
                pixel_ratio += pixel_ratio//10 + 1
            elif event.button == 5:  # scroll down
                pixel_ratio -= pixel_ratio//10 + 1
            pixel_ratio = min(max(pixel_ratio_range[0], pixel_ratio), pixel_ratio_range[1])

    pygame.display.update()
    fpsClock.tick(30)

pygame.quit()