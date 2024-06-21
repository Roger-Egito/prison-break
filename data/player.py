from data.sprite import Sprite
from data.config import window, delta
from data.stage import *
from data.hearing import *
import pygame


class Player(Sprite):
    slide_tick_counter = 0
    slide_delay = 0.5
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
        if beyond_border or self.can_move is False:
            if stage.name == 'Screenshot1':
                if self.can_move is True:
                    stage.transition('assets/maps/tmx/Screenshot2.tmx')
                if stage.x > -window.width:
                    stage.move()
                    #self.x -= 3.84
                    self.update_rect_x()
                    self.can_move = False
                    self.affected_by_gravity = False
                    self.t_right = True
                else:
                    stage.set_name('assets/maps/tmx/Screenshot2.tmx')
                    self.can_move = True
                    self.affected_by_gravity = True
                    self.t_right = False
                    stage.x = 0
                #self.set_left(0)
            else:
                self.set_right(window.width)
        return beyond_border

    def block_left_border(self):
        beyond_border = self.collision.left <= 0
        if beyond_border or self.can_move is False:
            #if stage.name == 'Screenshot2':
            #    stage.load('assets/maps/tmx/Screenshot1.tmx')
            #    stage.set_name('assets/maps/tmx/Screenshot1.tmx')
            #    self.set_right(window.width)
            #else:
            if stage.name == 'Screenshot2':
                if self.can_move is True:
                    stage.transition('assets/maps/tmx/Screenshot1.tmx')
                if stage.x < window.width:
                    stage.move()
                    self.x += 3.84
                    self.update_rect_x()
                    self.can_move = False
                    self.affected_by_gravity = False
                    self.t_left = True
                else:
                    stage.set_name('assets/maps/tmx/Screenshot1.tmx')
                    self.can_move = True
                    self.affected_by_gravity = True
                    self.t_left = False
                    stage.x = 0
                #self.set_left(0)
            else:
                self.set_left(0)

        return beyond_border

    def state_control(self):
        s = self.States
        st = self.state
        crouching = self.crouching
        sprinting = self.sprinting
        hanging = self.hanging
        airborne = self.airborne
        #flying = self.flying
        walking = self.vector_x != 0
        jumping = self.vector_y < 0  # and airborne and not flying
        falling = self.vector_y > 0

        if crouching and (self.last_state != 'HC_WALKING' or hanging):
            if hanging:
                self.state = s.H_CROUCHING
                if walking:
                    self.state = s.HC_WALKING
            elif airborne:
                if sprinting:
                    self.state = s.F_BACKFLIP
                else:
                    self.state = s.C_FALLING
            else:
                self.state = s.CROUCHING

        elif jumping:
            if st == 'H_JUMPING':
                self.state = s.H_JUMPING
            elif (st == 'S_JUMPING' or st == 'H_FALLING') and self.vector_x == 0:
                self.state = s.S_JUMPING
            else:
                self.state = s.JUMPING

        elif hanging:
            self.state = s.HANGING
            if self.vector_x != 0:
                self.state = s.H_WALKING

        elif falling:  # self.vector_y > 0 or (airborne and not hanging):
            if st == 'H_FALLING' or st == 'S_JUMPING' or self.last_state == 'H_CROUCHING':
                self.state = s.H_FALLING
            elif st == 'HJ_FALLING' or st == 'H_JUMPING':
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

        if st == 'FALLING':
            if self.last_state == 'HANGING':
                self.last_state = self.state
                self.state = s.H_FALLING
                self.stored_state = self.state
            elif self.last_state == 'H_JUMPING':
                self.last_state = self.state
                self.state = s.HJ_FALLING
                self.stored_state = self.state

        elif st == 'JUMPING':
            if self.last_state == 'IDLE':
                self.last_state = self.state
                self.state = s.S_JUMPING
                self.stored_state = self.state
            elif self.last_state in ('HANGING', 'H_WALKING', 'H_CROUCHING', 'HC_WALKING'):
                self.last_state = self.state
                self.state = s.H_JUMPING
                self.stored_state = self.state

    def slide(self, dist=0):
        if self.crouching:
            if not self.sliding and not self.on_wall:#self.state != 'IDLE':
                self.slide_fx()
                Sound_sphere(origin=self.collision.rect.center, groups=self.sound_spheres, max_radius=100)

            if dist:
                self.sliding = dist

            self.on_wall = self.move(hor_speed = self.speed * self.sliding)

            if self.on_wall:
                self.crash_fx()
                Sound_sphere(origin=self.on_wall[0].center, groups=self.sound_spheres)

            # Boing boing ~
            #if collision:
            #    self.sliding *= -1
            #    self.vector_x = self.speed * self.sliding

            self.block_right_border()
            self.block_left_border()

            self.slide_tick_counter += delta.time()

            if (self.slide_tick_counter >= 0.3 and not self.airborne) or self.vector_x == 0 or self.hanging:
                self.stand()
                self.can_crouch = False
                self.sliding = False
                self.slide_tick_counter = 0


    def allow_movement(self):
        if self.can_move:
            pressing_right = (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d])
            pressing_left = (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a])
            pressing_up = pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_w]
            pressing_down = pygame.key.get_pressed()[pygame.K_DOWN] or (pygame.key.get_mods() & pygame.KMOD_CTRL) or pygame.key.get_pressed()[pygame.K_s]
            pressing_shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
            pressing_z = pygame.key.get_pressed()[pygame.K_z]

            self.sprinting = pressing_shift
            crouching = self.crouching
            hanging = self.hanging
            self.airborne = self.vector_y != 0 and not hanging
            airborne = self.airborne
            sprinting = self.sprinting
            sliding = self.sliding
            flying = self.flying
            affected_by_gravity = self.affected_by_gravity


            idle = not pressing_right and not pressing_left and not pressing_up and not pressing_down and (not airborne or flying)

            if not airborne:
                self.vector_y = 0
            if not crouching:
                self.cramped = False

            if not affected_by_gravity and not pressing_up and not pressing_down:
                self.vector_y = 0
            if idle:
                self.vector_x = 0
                self.vector_y = 0
            if sliding:
                self.slide()
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
                    self.on_wall = self.move_right(speed)

                self.block_right_border()
            elif pressing_left and not pressing_right:
                speed = self.speed
                if sprinting:
                    speed *= 2
                if not sliding:
                    if crouching and not airborne:
                        speed *= 0.7
                    self.on_wall = self.move_left(speed)

                self.block_left_border()
            else:
                self.vector_x = 0
                self.step_tick_counter = 0

            if self.vector_x and not (airborne or sliding or crouching or self.on_wall):
                self.step_tick_counter += delta.time()
                step_tick_counter = self.step_tick_counter
                step_delay = self.step_delay / 2 if sprinting else self.step_delay

                if step_tick_counter >= step_delay:
                    Sound_sphere(origin=self.collision.rect.center, groups=self.sound_spheres, max_radius=abs(self.vector_x/2))
                    self.step_tick_counter = 0

            # ----------------------------------------------------------------------------------------------------------
            # JUMP
            if pressing_up:
                if flying:
                    speed = self.speed / 100
                    self.move_up(speed)
                elif hanging:
                    hit_ceiling = self.jump(5)
                    if not hit_ceiling:
                        self.hanging = False
                elif crouching  and self.last_y_direction != -1 and not (airborne or sliding):
                    cramped = self.stand()
                    if not cramped:
                        self.can_jump = False
                    elif self.can_jump:
                        self.airborne = True
                        hit_ceiling = self.jump()
                        if hit_ceiling:
                            self.hanging = True
                            self.airborne = False
                elif not airborne and self.can_jump:
                    self.airborne = True
                    hit_ceiling = self.jump()
                    if hit_ceiling:
                        self.hanging = True
                        self.airborne = False
            else:
                self.hanging = False
                self.can_jump = True
            # ----------------------------------------------------------------------------------------------------------
            # CROUCH / SLIDE

            if pressing_down:
                if not flying and not sliding:
                    if self.can_crouch:
                        self.crouch()
                    else:
                        self.stand()
                else:
                    speed = self.speed / 100
                    self.move_down(speed)
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
            else:
                self.affected_by_gravity = True
                self.has_collision = True
                self.flying = False
        else:
            if self.t_right:
                self.block_right_border()
            elif self.t_left:
                self.block_left_border()