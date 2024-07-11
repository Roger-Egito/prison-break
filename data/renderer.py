from data.config import window, clock, fps, volume, quit_game
from data.stage import *
from data.config import delta
import numpy as np
from PIL import Image


def generate_noise(img_num=20, pixel_ratio=5, alpha=5, resample=Image.NEAREST):
    assert pixel_ratio >= 1
    small_w, small_h = window.width // pixel_ratio, window.height // pixel_ratio
    imgs = []
    for i in range(img_num):
        img = Image.fromarray((np.random.rand(small_h, small_w, 1) * 255).astype(np.uint8).repeat(3, 2))
        img = img.resize((window.width, window.height), resample=resample)
        img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)
        img = img.convert_alpha()
        img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        imgs.append(img)
    return imgs

#def update_noise_alpha(img_list, alpha):
#    for img in img_list:
#        img.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
#    return img_list

class noise:
    imgs = generate_noise(alpha=5)
    imgs_strong = generate_noise(alpha=150)
    strong = False
    alpha = 5
    frame_counter = 0
    on = True

    #@classmethod
    #def update(cls, alpha):
    #    if alpha != cls.alpha:
    #        cls.imgs = generate_noise(alpha=alpha)
    #        cls.alpha = alpha

    @classmethod
    def render(cls):
        if cls.frame_counter >= len(cls.imgs):
            cls.frame_counter = 0

        if window.gm_tick_counter >= window.gm_tick_delay:
            window.gm_tick_counter = window.gm_tick_delay
            if pygame.key.get_pressed()[pygame.K_1]:
                window.gm_tick_counter = 0
                if cls.on:
                    cls.on = False
                else:
                    cls.on = True

        if noise.on:
            if noise.strong:
                render(cls.imgs_strong[cls.frame_counter])
            else:
                render(cls.imgs[cls.frame_counter])
            cls.frame_counter += 1





def render_game(player, renderPlayer = True):
    if renderPlayer:
        stage.background_render(player)
    else:
        stage.background_render(None)

    noise.render()
    fps.render()
    window.draw()
    pygame.display.update()

    # UPDATE

    clock.tick(fps.max)
    stage.update(player)
    volume.check_mute()
    delta.time_update()