from data.sprite import Sprite
from data.config import window, delta
from data.stage import *
from data.hearing import *
#from data.game import game_over, stage_restart
import pygame


class Player(Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.anim.walk = self.anim.populate('assets/Characters/2 Punk/Walk.png', image_count=6)
        self.anim.jump = self.anim.populate('assets/Characters/2 Punk/Punk_jump.png', image_count=4)
        self.anim.run = self.anim.populate('assets/Characters/2 Punk/Punk_run.png', image_count=6)
        self.anim.crouch = self.anim.populate('assets/Characters/2 Punk/Sitdown.png', image_count=3)
        self.anim.hang = self.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
        self.anim.h_crouch = self.anim.populate('assets/Characters/2 Punk/HCWalk.png', image_count=2)
        self.anim.h_fall = self.anim.populate('assets/Characters/2 Punk/Happy.png', image_count=6)
        self.anim.s_jump = self.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
        #self.anim.pullup = self.anim.populate('assets/Characters/2 Punk/Pullup.png', image_count=6, dimensions=(0, 41, 48, 48))
        self.anim.c_walk = self.anim.populate('assets/Characters/2 Punk/CWalking3.png', image_count=4)
        self.anim.h_walk = self.anim.populate('assets/Characters/2 Punk/Fall.png', image_count=4)
        self.anim.hc_walk = self.anim.populate('assets/Characters/2 Punk/HCWalk.png', image_count=2)
        self.anim.h_jump = self.anim.populate('assets/Characters/2 Punk/Punk_doublejump.png', image_count=6)
        #self.anim.walk = self.anim.populate('assets/Characters/2 Punk/Roll.png', image_count=4)
        self.anim.slide = self.anim.img('assets/Characters/2 Punk/Slide.png')
        # self.anim.slide = self.anim.img('assets/Characters/Soldier_1/Temp.png')
        self.anim.idle2 = self.anim.populate('assets/Characters/2 Punk/Talk.png', image_count=6)
        self.anim.idle3 = self.anim.populate('assets/Characters/2 Punk/Use.png', image_count=6)
        self.anim.idle4 = self.anim.populate('assets/Characters/2 Punk/Happy.png', image_count=6)
        self.anim.idle5 = self.anim.populate('assets/Characters/2 Punk/Idle2.png', image_count=4)
        self.anim.roll = self.anim.populate('assets/Characters/2 Punk/Roll.png', image_count=4)

    slide_tick_counter = 0
    slide_delay = 0.5
    whistle_tick_counter = 0
    can_move = True
    can_crouch = True
    can_jump = True
    cramped = False
    t_right = False  # Transition Right. Temp
    t_left = False   # Transition Left.  Temp

    transition_counter = 0
    transition_target = 1

    def block_right_border(self):
        beyond_border = self.collision.right >= window.width
        if beyond_border or stage.in_transition:
            self.sound_spheres.empty()
            #self.force_stop_slide()
            stage.transition_right(self)
        return beyond_border

    def block_left_border(self):
        beyond_border = self.collision.left <= 0
        if beyond_border or stage.in_transition:
            self.sound_spheres.empty()
            #self.force_stop_slide()
            stage.transition_left(self)
        return beyond_border

    def state_control(self):
        s = self.States
        st = self.state
        crouching = self.crouching
        sprinting = self.sprinting
        hanging = self.hanging
        airborne = self.airborne
        sliding = self.sliding
        #flying = self.flying
        walking = self.vector_x != 0
        jumping = self.vector_y < 0 and airborne  # and not flying
        falling = self.vector_y > 0 or airborne

        if st == 'ROLLING':
            if self.anim.animation_is_over(self.anim.roll):
                self.rolling = False

        if self.rolling:
          self.state = s.ROLLING


        elif crouching and (self.last_state != 'HC_WALKING' or hanging):
            if hanging:
                self.state = s.H_CROUCHING
                if walking:
                    self.state = s.HC_WALKING
            elif walking and not sliding:
                self.state = s.C_WALKING
                if sprinting:
                    self.state = s.C_RUNNING
            elif airborne:
                if sprinting:
                    self.state = s.F_BACKFLIP
                else:
                    self.state = s.C_FALLING
            else:
                self.state = s.CROUCHING

        elif jumping:
            if self.state == 'H_JUMPING':
                self.state = s.H_JUMPING
            elif (self.state == 'S_JUMPING' or self.state == 'H_FALLING') and self.vector_x == 0:
                self.state = s.S_JUMPING
            else:
                self.state = s.JUMPING

        elif hanging:
            self.state = s.HANGING
            if self.vector_x != 0:
                self.state = s.H_WALKING

        elif falling:  # self.vector_y > 0 or (airborne and not hanging):
            if self.state == 'H_FALLING' or self.state == 'S_JUMPING' or self.last_state == 'H_CROUCHING':
                self.state = s.H_FALLING
            elif self.state == 'HJ_FALLING' or self.state == 'H_JUMPING':
                self.state = s.HJ_FALLING
            else:
                self.state = s.FALLING

        elif walking:
            if sprinting:
                self.state = s.RUNNING
            else:
                self.state = s.WALKING

        else:
            self.state = s.IDLE

        # ---

        if self.state != self.stored_state and self.state_change_counter == 1:
            self.last_state = self.stored_state
            self.stored_state = self.state
            self.state_change_counter = 0
        elif self.state != self.last_state and self.state_change_counter == 0:
            self.stored_state = self.state
            self.state_change_counter = 1

        if self.state == 'FALLING':
            if self.last_state == 'HANGING':
                #self.last_state = self.state
                self.state = s.H_FALLING
                self.stored_state = self.state
            elif self.last_state == 'H_JUMPING':
                #self.last_state = self.state
                self.state = s.HJ_FALLING
                self.stored_state = self.state

        elif self.state == s.JUMPING:#'JUMPING':
            if self.last_state == 'IDLE':
                #self.last_state = self.state
                self.state = s.S_JUMPING
                self.stored_state = self.state
            elif self.last_state in ('HANGING', 'H_WALKING', 'H_CROUCHING', 'HC_WALKING'):
                #self.last_state = self.state
                self.state = s.H_JUMPING
                self.stored_state = self.state

    def slide(self, dist=0):
        if self.crouching:
            if not self.sliding and not self.on_wall:#self.state != 'IDLE':
                self.slide_fx()
                Sound_sphere(origin=self.collision.rect.center, groups=self.sound_spheres, max_radius=100)

            if dist:
                self.sliding = dist

            self.on_wall = self.move(hor_speed=self.speed * self.sliding)
            print(self.vector_x)

            #if self.vector_x > 0:
            #    self.block_right_border()
            #elif self.vector_x < 0:
            #    self.block_left_border()

            if self.on_wall:
                self.crash_fx()
                if self.on_wall[0].hca:
                    Sound_sphere(origin=self.on_wall[0].collision.rect.center, groups=self.sound_spheres)
                else:
                    Sound_sphere(origin=self.on_wall[0].rect.center, groups=self.sound_spheres)

            # Boing boing ~
            #if collision:
            #    self.sliding *= -1
            #    self.vector_x = self.speed * self.sliding


            #self.block_right_border()
            #self.block_left_border()

            self.slide_tick_counter += delta.time()

            if (self.slide_tick_counter >= 0.3 and not self.airborne) or self.vector_x == 0 or self.hanging:
                self.stand()
                self.can_crouch = False
                self.sliding = False
                self.slide_tick_counter = 0

    def force_stop_slide(self):
        self.sliding = False
        self.slide_tick_counter = 0
        self.can_move = True

    def allow_movement(self):
        if self.can_move and not stage.in_transition:
            pressing_right = (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d])
            pressing_left = (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a])
            pressing_up = pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_w]
            pressing_down = pygame.key.get_pressed()[pygame.K_DOWN] or (pygame.key.get_mods() & pygame.KMOD_CTRL) or pygame.key.get_pressed()[pygame.K_s]
            pressing_shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
            pressing_z = pygame.key.get_pressed()[pygame.K_z]
            pressing_r = pygame.key.get_pressed()[pygame.K_r]
            pressing_g = pygame.key.get_pressed()[pygame.K_g]
            pressing_q = pygame.key.get_pressed()[pygame.K_q]

            self.sprinting = pressing_shift
            crouching = self.crouching
            hanging = self.hanging
            if self.vector_y > 0 and not hanging:
                self.airborne = True
            airborne = self.airborne
            sprinting = self.sprinting
            sliding = self.sliding
            flying = self.flying
            affected_by_gravity = self.affected_by_gravity
            self.close_to_interactive = False

            idle = not pressing_right and not pressing_left and not pressing_up and not pressing_down and (not airborne or flying or sliding)

            if not airborne:
                self.vector_y = 0
            if not crouching:
                self.cramped = False

            if not affected_by_gravity and not pressing_up and not pressing_down:
                self.vector_y = 0
            if sliding:
                self.slide()
            elif idle:
                self.vector_x = 0
                self.vector_y = 0
                if self.last_x_direction == 1:
                    hits = self.check_collision_right(stage.interactive_group)
                else:
                    hits = self.check_collision_left(stage.interactive_group)
                if len(hits):
                    self.close_to_interactive = True
                #if not len(hits):



            if pressing_down and airborne and not sliding:
                self.vector_y += self.speed * 8 * delta.time()
            if sprinting:
                if pressing_down and self.can_crouch and not (sliding or airborne or hanging):
                    if not self.flipped:
                        self.slide(3)
                    else:
                        self.slide(-3)

            # ----------------------------------------------------------------------------------------------------------
            # DIRECTIONS

            if pressing_right and not pressing_left:
                speed = self.speed
                if sprinting:
                    speed *= 2
                if not sliding:
                    if crouching and not airborne:
                        speed *= 0.7

                    hits = self.move_right(speed)
                    if hits:
                        for hit in hits:
                            if not self.close_to_interactive:
                                for hit in hits:
                                    if hit.interactive:
                                        self.close_to_interactive = True
                                        break

                        self.on_wall = True
                        if len(hits) == 1:
                                if hits[0].hca:
                                    hit = hits[0].collision.rect
                                else:
                                    hit = hits[0].rect

                                if self.vector_y == 0: # Bumping on 1x1 while on the floor. Vault over!
                                    if hit.top <= self.collision.bottom - (self.collision.height / 3) and self.collision.top < hit.top and not hanging:
                                            play_sfx('fall', volume=0.1)
                                            self.set_midbottom(hit.midtop)
                                            self.crouch()
                                            self.stand()
                                            self.rolling = True
                                elif self.vector_y >= 0: # Bumping on a ledge while falling. Vault over!
                                    if hit.top <= self.collision.bottom - (self.collision.height / 3) and self.collision.top < hit.top and hit.top > self.collision.bottom - (self.collision.height / 2) and not hanging:
                                            play_sfx('fall', volume=0.1)
                                            self.set_midbottom(hit.midtop)
                                            self.crouch()
                                            self.stand()
                                            self.rolling = True
                    else:
                        self.on_wall = False


                #self.block_right_border()
            elif pressing_left and not pressing_right:

                speed = self.speed
                if sprinting:
                    speed *= 2
                if not sliding:
                    if crouching and not airborne:
                        speed *= 0.7

                    hits = self.move_left(speed)
                    if hits:
                        if not self.close_to_interactive:
                            for hit in hits:
                                if hit.interactive:
                                    self.close_to_interactive = True
                                    break
                        self.on_wall = True
                        if len(hits) == 1:
                                if hits[0].hca:
                                    hit = hits[0].collision.rect
                                else:
                                    hit = hits[0].rect

                                if self.vector_y == 0: # Bumping on 1x1 while on the floor. Vault over!
                                    if hit.top <= self.collision.bottom - (self.collision.height / 3) and self.collision.top < hit.top and not hanging:
                                            play_sfx('fall', volume=0.1)
                                            self.set_midbottom(hit.midtop)
                                            self.crouch()
                                            self.stand()
                                            self.rolling = True
                                elif self.vector_y >= 0: # Bumping on a ledge while falling. Vault over!
                                    if hit.top <= self.collision.bottom - (self.collision.height / 3) and self.collision.top < hit.top and hit.top > self.collision.bottom - (self.collision.height / 2) and not hanging:
                                            play_sfx('fall', volume=0.1)
                                            self.set_midbottom(hit.midtop)
                                            self.crouch()
                                            self.stand()
                                            self.rolling = True
                    else:
                        self.on_wall = False

                #self.block_left_border()
            else:
                if not sliding:
                    self.vector_x = 0
                self.step_tick_counter = 0
                self.rolling = False

            if self.vector_x and not (airborne or sliding or crouching or self.on_wall):
                self.step_tick_counter += delta.time()
                step_tick_counter = self.step_tick_counter
                step_delay = self.step_delay / 2 if sprinting else self.step_delay

                if step_tick_counter >= step_delay and not hanging:
                    play_sfx('walk-4', volume=0.7)
                    Sound_sphere(origin=self.collision.rect.center, groups=self.sound_spheres, max_radius=abs(self.vector_x/2))
                    self.step_tick_counter = 0

            # ----------------------------------------------------------------------------------------------------------
            # JUMP
            if pressing_up:
                if flying:
                    if self.vector_y > 0:
                        self.vector_y = 0
                    #speed = self.speed / 10
                    speed = self.speed
                    self.airborne = True
                    if sprinting:
                        speed *= 2
                    self.force_move(ver_speed=-speed)
                    #self.move_up(speed)
                elif airborne:
                    hit_ceiling = self.jump(0)
                    if hit_ceiling:
                        if not self.close_to_interactive:
                            for hit in hit_ceiling:
                                if hit.interactive:
                                    self.close_to_interactive = True
                                    break
                        self.hanging = True
                        self.airborne = False
                        print('airborne:', self.airborne)
                elif hanging:
                # TODO: Make backflip happen more consistently. Weird bug.
                    #self.affected_by_gravity = False
                    #self.force_move(ver_speed=-self.vector_y - (5 / delta.time()))
                    hit_ceiling = self.jump(5)#+1 * delta.time())
                    #hit_ceiling = self.check_collision_up(stage.collision_group)
                    if hit_ceiling:
                        if not self.close_to_interactive:
                            for hit in hit_ceiling:
                                if hit.interactive:
                                    self.close_to_interactive = True
                                    break
                    else:
                        self.hanging = False
                        self.airborne = True
                elif crouching and self.last_y_direction != -1 and not (airborne or sliding):
                    self.cramped = self.stand()
                    if not self.cramped:
                        self.can_jump = False
                    elif self.can_jump:
                        self.airborne = True
                        hit_ceiling = self.jump()
                        if hit_ceiling:
                            if not self.close_to_interactive:
                                for hit in hit_ceiling:
                                    if hit.interactive:
                                        self.close_to_interactive = True
                                        break
                            self.hanging = True
                            self.airborne = False
                elif not airborne and self.can_jump:
                    hit_ceiling = self.jump()

                    if hit_ceiling:
                        if not self.close_to_interactive:
                            for hit in hit_ceiling:
                                if hit.interactive:
                                    self.close_to_interactive = True
                                    break
                        self.hanging = True
                        self.airborne = False

                    else:
                        self.airborne = True
            else:
                if self.hanging:
                    self.hanging = False
                    self.airborne = True
                self.can_jump = True
                if self.vector_y < 0 and airborne and not flying:
                    self.vector_y += self.speed * 8 * delta.time()
            # ----------------------------------------------------------------------------------------------------------
            # CROUCH / SLIDE

            if pressing_down:
                if flying:
                    if self.vector_y < 0:
                        self.vector_y = 0
                    speed = self.speed
                    if sprinting:
                        speed *= 2
                    self.force_move(ver_speed=speed)
                elif not sliding:
                    if self.can_crouch:
                        self.crouch()
                    else:
                        self.stand()
            else:
                if crouching and not airborne:
                    self.can_crouch = False
                else:
                    self.can_crouch = True
            # ----------------------------------------------------------------------------------------------------------
            # DEBUG NO COLLISION
            if pressing_z:
                self.affected_by_gravity = False
                self.has_collision = False
                self.flying = True
                self.immortal = True
            else:
                self.affected_by_gravity = True
                self.has_collision = True
                self.flying = False
                self.immortal = False

            if pressing_q:
                if self.whistle_tick_counter >= 0.5:
                    play_sfx('whistle', volume=0.2)
                    Sound_sphere(origin=self.collision.rect.center, groups=self.sound_spheres, max_radius=200)
                    self.whistle_tick_counter = 0
            else:
                self.whistle_tick_counter += 1 * delta.time()
                if self.whistle_tick_counter >= 0.5:
                    self.whistle_tick_counter = 0.5

            if pressing_r:
                self.affected_by_gravity = False
                from data.game import stage_restart
                stage_restart()

            if pressing_g:
                self.affected_by_gravity = False
                from data.game import game_over
                game_over()


            if self.vector_x > 0:
                self.block_right_border()
            elif self.vector_x < 0:
                self.block_left_border()

        else:
            if self.t_right:
                self.block_right_border()
            elif self.t_left:
                self.block_left_border()