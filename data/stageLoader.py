'''
Esta classe agora contém os métodos de renderização da janela e criação do player.
Atenção: A primeira coordenada de spawnRight em mapInfo.json representa quantos pixels o jogador deve voltar em relação à borda da janela.
'''
from data.config import clock, fps, volume, quit_game
from data.stage import *
from data.player import *
import json

currentStageLine = 0
currentStageColumn = 0

player = Player('assets/Characters/2 Punk/Punk_idle.png', x=160, y=160, collision_offset=[7, 14], collision_dimensions=(15, 34))  #collision_offset=[2.5, 14], collision_dimensions=(20, 34))
player.anim.walk = player.anim.populate('assets/Characters/2 Punk/Walk.png', image_count=6)
player.anim.jump = player.anim.populate('assets/Characters/2 Punk/Punk_jump.png', image_count=4)
player.anim.run = player.anim.populate('assets/Characters/2 Punk/Punk_run.png', image_count=6)
player.anim.crouch = player.anim.populate('assets/Characters/2 Punk/Sitdown.png', image_count=3)
player.anim.hang = player.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
player.anim.h_crouch = player.anim.populate('assets/Characters/2 Punk/HCWalk.png', image_count=2)
player.anim.h_fall = player.anim.populate('assets/Characters/2 Punk/Happy.png', image_count=6)
player.anim.s_jump = player.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
#player.anim.h_jump = player.anim.populate('assets/Characters/2 Punk/Pullup.png', image_count=6, dimensions=(0, 41, 48, 48))
player.anim.h_walk = player.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
player.anim.h_c_walk = player.anim.populate('assets/Characters/2 Punk/HCWalk.png', image_count=2)
player.anim.h_jump = player.anim.populate('assets/Characters/2 Punk/Punk_doublejump.png', image_count=6)
player.anim.slide = player.anim.img('assets/Characters/2 Punk/Slide.png')

def generalRenderer(renderPlayer = True):
    if renderPlayer:
        stage.render(player)
        player.apply_gravity()
        player.allow_movement()
        player.update_collision()
        player.state_control()
        player.animate()
    else:
        stage.render(None)
    fps.render()

    window.draw()
    pygame.display.update()

    # UPDATE

    clock.tick(fps.max)
    volume.check_mute()
    delta.time_update()



def renderWindow():
    while True:
        #print(player.x,', ', player.y)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        generalRenderer()

def load(right=False, firstCall = False):

    mapPosition = str(currentStageLine)+'-'+str(currentStageColumn)
    filepath = 'assets/maps/tmx/'+mapPosition+'.tmx'
    file = open("assets/maps/mapInfo.JSON")
    jason = json.load(file)


    if not firstCall:
        if not right:
            stage.transition(filepath)
        else:
            stage.transition(filepath, True)
        stagex = 0
        while stagex < window.width:
            generalRenderer(False)
            player.x -= 2
            if not right:
                stagex = stage.move(window)
            else:
                stagex = -stage.move(window, True)
        stage.x = 0
        stage.remove_out_of_bounds_tiles(window)

    else:
        stage.load(filepath)
    stage.set_name(filepath)
    if right:
        playerSpawn = jason[mapPosition]["spawnRight"]
        player.x = window.width+playerSpawn[0]
        player.y = playerSpawn[1]
    else:
        playerSpawn = jason[mapPosition]["spawnLeft"]
        player.x = playerSpawn[0]
        player.y = playerSpawn[1]
    file.close()

def loadFrontMap():
    global currentStageColumn
    currentStageColumn += 1
    load()
def loadBackMap():
    global currentStageColumn
    currentStageColumn -= 1
    load(True)
def loadUpperMap():
    global currentStageLine
    currentStageLine -= 1
    load()
def loadLowerMap():
    global currentStageLine
    currentStageLine += 1
    load()
