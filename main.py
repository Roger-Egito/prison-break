import pygame
from data.config import *
from data.stage import *
#import data.stage as stage
import data.game as game
import data.title as title
#from data.renderer import *

#TODO: Fix fuckin' double jumpin' when low FPS
#TODO: Fix stupid hanging glitch when low FPS
#TODO: Title
#TODO: Ending
#TODO: Items
#TODO: Stages
#TODO: Drone

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Prison Break - Escape Big Sister')

if testing:
    #title.menu()
        game.loop()
    #stage.renderWindow()

else:
    print("Testing is set as False, but the menu isn't ready yet")
