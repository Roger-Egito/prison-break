import pygame
import sys
import random

pygame.init()

class window:
    width = 800
    height = 448
    center_width = width / 2
    center_height = height / 2
    center = (center_width, center_height)
    display = pygame.display.set_mode((width, height))
    background_color = (10, 10, 10)

class delta:
    curr_time = 0
    last_time = 0

    @classmethod
    def time(cls):
        delta_time = (cls.curr_time - cls.last_time) / 1000

        return delta_time

    @classmethod
    def time_update(cls):
        cls.last_time = cls.curr_time
        cls.curr_time = pygame.time.get_ticks()

class fps:

    global clock

    @classmethod
    def get(cls):
        return int(clock.get_fps())

    max = 240           #random.randint(1, 10) * 100
    last_values = []
    max_samples = 5
    avg = 0
    show = True
    key_press_delay = 0.2

    font = pygame.font.Font(None, 32)
    color = 'lightsalmon'

    alignment = "topright"
    coords = (window.width - 16, 8)

    @classmethod
    def render(cls):
        global tick_counter

        tick_counter += delta.time()

        if tick_counter >= cls.key_press_delay and pygame.key.get_pressed()[pygame.K_f]:
            if cls.show:
                cls.show = False
                cls.tick_counter = 0
            else:
                cls.show = True
                cls.tick_counter = 0

        if cls.show:



            if loop_counter >= 100:

                cls.last_values.append(cls.get())

                if len(cls.last_values) >= cls.max_samples:
                   cls.avg = int(sum(cls.last_values) / len(cls.last_values))
                   cls.last_values.clear()
                cls.loop_counter = 0

            text = cls.font.render("FPS: " + str(cls.avg), 1, pygame.Color(cls.color))
            rect = text.get_rect()
            setattr(rect, cls.alignment, cls.coords)
            pygame.draw.rect(window.display, 'black', rect)
            render(text, rect)

            text2 = cls.font.render("Total Loops: " + str(total_loops), 1, pygame.Color(cls.color))
            rect2 = text2.get_rect()
            setattr(rect2, cls.alignment, (cls.coords[0], cls.coords[1]+50))
            pygame.draw.rect(window.display, 'black', rect2)
            render(text2, rect2)

            text3 = cls.font.render("Time: " + str(time), 1, pygame.Color(cls.color))
            rect3 = text3.get_rect()
            setattr(rect3, cls.alignment, (cls.coords[0], cls.coords[1]+100))
            pygame.draw.rect(window.display, 'black', rect3)
            render(text3, rect3)

            text4 = cls.font.render("Sec / Loop: " + str(spl), 1, pygame.Color(cls.color))
            rect4 = text4.get_rect()
            setattr(rect4, cls.alignment, (cls.coords[0], cls.coords[1]+150))
            pygame.draw.rect(window.display, 'black', rect4)
            render(text4, rect4)

            text5 = cls.font.render("Delta: " + str(delta.time()), 1, pygame.Color(cls.color))
            rect5 = text5.get_rect()
            setattr(rect5, cls.alignment, (cls.coords[0], cls.coords[1]+200))
            pygame.draw.rect(window.display, 'black', rect5)
            render(text5, rect5)

def render(img, coords=(0, 0)):
    window.display.blit(img, coords)


tick_counter = 0
loop_counter = 0

total_loops = 0

clock = pygame.time.Clock()


rectangles_size = 48

rect_30_x = 0
rect_60_x = 0
rect_120_x = 0
rect_240_x = 0

rect_30_x_direction = 1
rect_60_x_direction = 1
rect_120_x_direction = 1
rect_240_x_direction = 1

rect_30 = pygame.Rect(0, window.height / 2 - rectangles_size, 48, 48)
rect_60 = pygame.Rect(0, rect_30.y + rectangles_size * 1.5, 48, 48)
rect_120 = pygame.Rect(0, rect_60.y + rectangles_size * 1.5, 48, 48)
rect_240 = pygame.Rect(0, rect_120.y + rectangles_size * 1.5, 48, 48)

surface = pygame.Surface((48, 48))

# ----------------------------------------------------------------------------------------------------------------------

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(fps.max)
    time = int(pygame.time.get_ticks() / 1000)
    spl = int(pygame.time.get_ticks() / max(1, total_loops)) / 1000 # SECONDS PER LOOP. AVERAGE.
    # DELTA TIME IS HOW MANY SECONDS TOOK THIS LOOP
    loop_counter += 1
    total_loops += 1

    delta.time_update()

    rect_30_x += (rect_30_x_direction / (240/30)) * delta.time() * 240
    rect_60_x += (rect_60_x_direction / (240/60)) * delta.time() * 240
    rect_120_x += (rect_120_x_direction / (240/120)) * delta.time() * 240
    rect_240_x += (rect_240_x_direction / (240/240)) * delta.time() * 240



    if rect_30_x + rect_30.width >= window.width:
        rect_30_x = window.width - rect_30.width
        rect_30_x_direction = -1
    elif rect_30_x <= 0:
        rect_30_x = 0
        rect_30_x_direction = 1
    if rect_60_x + rect_60.width >= window.width:
        rect_60_x = window.width - rect_60.width
        rect_60_x_direction = -1
    elif rect_60_x <= 0:
        rect_60_x = 0
        rect_60_x_direction = 1
    if rect_120_x + rect_120.width >= window.width:
        rect_120_x = window.width - rect_120.width
        rect_120_x_direction = -1
    elif rect_120_x <= 0:
        rect_120_x = 0
        rect_120_x_direction = 1
    if rect_240_x + rect_240.width >= window.width:
        rect_240_x = window.width - rect_240.width
        rect_240_x_direction = -1
    elif rect_240_x <= 0:
        rect_240_x = 0
        rect_240_x_direction = 1


    rect_30.x = round(rect_30_x)
    rect_60.x = round(rect_60_x)
    rect_120.x = round(rect_120_x)
    rect_240.x = round(rect_240_x)

    pygame.draw.rect(window.display, 'black', pygame.Rect(0, 0, window.width, window.height))

    pygame.draw.rect(window.display, 'white', rect_30)
    pygame.draw.rect(window.display, 'white', rect_60)
    pygame.draw.rect(window.display, 'white', rect_120)
    pygame.draw.rect(window.display, 'white', rect_240)

    delta.time_update()
    fps.render()
    pygame.display.update()
