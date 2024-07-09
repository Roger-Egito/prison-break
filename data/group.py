import pygame

class Group(pygame.sprite.Group):

    def render(self):
        for member in pygame.sprite.Group.sprites(self):
            member.render()

    def move(self, hor=0, ver=0, speed=0):
        if hor:
            for member in pygame.sprite.Group.sprites(self):
                member.move(hor=hor, ver=ver, speed=speed)

    def force_move(self, hor=0, ver=0, speed=0):
        if hor:
            for member in pygame.sprite.Group.sprites(self):
                member.force_move(hor_speed=hor * speed, ver_speed=ver * speed)

    def hide(self):
        for member in pygame.sprite.Group.sprites(self):
            member.hide()

    def unhide(self):
        for member in pygame.sprite.Group.sprites(self):
            member.unhide()

    def animate(self):
        for member in pygame.sprite.Group.sprites(self):
            member.animate()

    def state_control(self):
        for member in pygame.sprite.Group.sprites(self):
            member.state_control()

    def update_collision(self):
        for member in pygame.sprite.Group.sprites(self):
            member.update_collision()

    def update_vision(self):
        for member in pygame.sprite.Group.sprites(self):
            member.update_vision()

    def ai_control(self, player):
        for member in pygame.sprite.Group.sprites(self):
            member.ai_control(player)

    def alert(self):
        for member in pygame.sprite.Group.sprites(self):
            member.alert = True

    def render_spheres(self):
        for member in pygame.sprite.Group.sprites(self):
            member.sound_spheres.update()

    def apply_gravity(self):
        for member in pygame.sprite.Group.sprites(self):
            member.apply_gravity()

    #def __init__(self, members=[], offset=[0,0]):
    #    self.members = members
    #    self.offset = offset

    #def __iter__(self):
    #    yield self.members
#
    #def add(self, item):
    #    self.members.append(item)
#
    #def append(self, item):
    #    self.members.append(item)
#
    #def remove(self, item):
    #    self.members.remove(item)
#
    #def clear(self, item):
    #    self.members.clear()
#
    #def render(self):
    #    for member in self.members:
    #        member.render()
#
    #def move(self, speed):
    #    for member in self.members:
    #        member.move(speed=speed)