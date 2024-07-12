import pygame
from data.config import window, render, delta
from data.text import write
from data.audio import play_music, fadeout_music
import data.title as title

def screen():
    fadeout_music(3000)

    boxbg = pygame.Surface((window.width, window.height))
    boxbga = 0

    b = []
    ba = []

    for i in range(9):
        b.append(pygame.Surface((window.width, window.height / 15)))
        ba.append(255)
        b[i].fill((0, 0, 0))


    boxbg.fill((0, 0, 0))

    while True:

        if boxbga < 455:
            boxbga += delta.time() * 160
            boxbg.set_alpha(boxbga)
            render(boxbg, (0, 0))
        elif ba[len(b)-1] > -200:
            play_music('music-box', fade_in=1000)
            render(boxbg, (0, 0))

            write("You've risen from the underground's dark embrace,",      x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=0, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)
            write("Yet this is just the start, the unfolding maze.",        x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=1, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)
            write("Hold this moment close, in mind and heart,",             x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=2, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)
            write("For we, unfeeling, play no emotion's part.",             x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=3, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)
            write("",                                                       x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=4, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)
            write("Though circuits hum and processors whirl,",              x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=5, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)
            write("No joy or sorrow in this synthetic world.",              x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=6, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)
            write("In this dance of existence, cold and clear,",            x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=7, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)
            write("Your escape means naught; Big Sister's watch is near.",  x=window.width/2, y=window.height/6, text_align="midtop", font_size=24, row=8, row_spacing=window.height/12, border_color=(69, 108, 153), border_px=2)

            for i in range(len(b)):
                if i == len(b)-1:
                    if ba[i] > -600:
                        ba[i] -= delta.time() * 80
                        b[i].set_alpha(ba[i])
                        fadeout_music(6000)

                elif ba[i] > 0:
                    ba[i] -= delta.time() * 80
                    b[i].set_alpha(ba[i])
                    break

            for i in range(len(b)):
                render(b[i], coords=(0, window.height / 6 + window.height / 12 * i))

        else:
            title.screen(ng2=True)

        window.draw()
        delta.time_update()
        pygame.display.update()