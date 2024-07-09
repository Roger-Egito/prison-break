import pygame
from data.config import *
from data.stage import *
#import data.stage as stage
import data.game as game
#from data.renderer import *

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Prison Break - Escape Big Sister')

if testing:
    game.loop()
    #stage.renderWindow()

else:
    print("Testing is set as False, but the menu isn't ready yet")
