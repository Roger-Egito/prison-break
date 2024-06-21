import pygame
from data.config import *
from data.testing import *
from data.stageLoader import *

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Prison Break - Escape Big Sister')

if testing:
    load(firstCall=True)
    renderWindow()

else:
    print("Testing is set as False, but the menu isn't ready yet")
