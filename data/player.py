from data.sprite import Sprite
from data.config import window, delta
from data.stage import *
import pygame


class Player(Sprite):
    slide_tick_counter = 0
    slide_delay = 0.5
    can_slide = True
    can_move = True
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
                    self.x -= 1.92
                    self.update_rect_x()
                    self.can_move = False
                    self.t_right = True
                else:
                    stage.set_name('assets/maps/tmx/Screenshot2.tmx')
                    self.can_move = True
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
                    self.x += 1.92
                    self.update_rect_x()
                    self.can_move = False
                    self.t_left = True
                else:
                    stage.set_name('assets/maps/tmx/Screenshot1.tmx')
                    self.can_move = True
                    self.t_left = False
                    stage.x = 0
                #self.set_left(0)
            else:
                self.set_left(0)

        return beyond_border

    #TODO: Clean this mess
    def state_control(self):
        if self.crouching:
            if self.airborne:
                if (self.sprinting or self.state == 'JUMPING' or self.state == 'S_JUMPING' or self.state == 'C_FALLING') and not self.hanging:
                    self.state = self.States.C_FALLING
                else:
                    self.state = self.States.H_CROUCHING
                    if self.vector_x != 0:
                        self.state = self.States.H_C_WALKING
            else:
                self.state = self.States.CROUCHING
        elif self.vector_y < 0:
            if self.state == 'H_JUMPING':
                self.state = self.States.H_JUMPING
            elif (self.state == 'S_JUMPING' or self.state == 'H_FALLING') and self.vector_x == 0:
                self.state = self.States.S_JUMPING
            else:
                self.state = self.States.JUMPING
        elif self.vector_y == 0 and self.hanging:
            self.state = self.States.HANGING
            if self.vector_x != 0:
                self.state = self.States.H_WALKING
        elif self.vector_y > 0 or (self.airborne and not self.hanging):
            if self.state == 'H_FALLING' or self.state == 'S_JUMPING' or self.last_state == 'H_CROUCHING':
                self.state = self.States.H_FALLING
            elif self.state == 'H_J_FALLING' or self.state == 'H_JUMPING':
                self.state = self.States.H_J_FALLING
            else:
                self.state = self.States.FALLING
        elif self.vector_x != 0:
            #if self.state == 'HANGING' or self.state == 'H_WALKING':
            #    self.state = self.States.H_WALKING
            #else:
                if self.sprinting:
                    self.state = self.States.RUNNING
                else:
                    self.state = self.States.WALKING
        else:
            self.state = self.States.IDLE
        if self.state != self.stored_state and self.state_change_counter == 1:
            self.last_state = self.stored_state
            self.stored_state = self.state
            self.state_change_counter = 0
        elif self.state != self.last_state and self.state_change_counter == 0:
            self.stored_state = self.state
            self.state_change_counter = 1

        if self.state == 'FALLING':
            if self.last_state == 'HANGING':
                self.last_state = self.state
                self.state = self.States.H_FALLING
                self.stored_state = self.state
            elif self.last_state == 'H_JUMPING':
                self.last_state = self.state
                self.state = self.States.H_J_FALLING
                self.stored_state = self.state
        elif self.state == 'JUMPING':
            if self.last_state == 'IDLE' or self.last_state == 'CROUCHING':
                self.last_state = self.state
                self.state = self.States.S_JUMPING
                self.stored_state = self.state
            if self.last_state == 'HANGING' or self.last_state == 'H_WALKING' or self.last_state == 'H_CROUCHING' or self.last_state == 'H_C_WALKING':
                self.last_state = self.state
                self.state = self.States.H_JUMPING
                self.stored_state = self.state

    def allow_movement(self):
        if self.can_move:
            pressing_right = (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d])
            pressing_left = (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a])
            pressing_up = pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_w]
            pressing_down = pygame.key.get_pressed()[pygame.K_DOWN] or (pygame.key.get_mods() & pygame.KMOD_CTRL) or pygame.key.get_pressed()[pygame.K_s]
            pressing_shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
            pressing_z = pygame.key.get_pressed()[pygame.K_z]

            self.sprinting = pressing_shift
            self.airborne = self.vector_y != 0

            airborne = self.airborne
            crouching = self.crouching
            hanging = self.hanging
            crawling = crouching and (not airborne or hanging)
            sprinting = self.sprinting
            sliding = self.sliding
            can_slide = self.can_slide
            flying = self.flying
            affected_by_gravity = self.affected_by_gravity


            idle = (not pressing_right and not pressing_left and not pressing_up and not pressing_down and (not airborne or flying))

            if not affected_by_gravity and not pressing_up and not pressing_down:
                self.vector_y = 0
            if idle:
                self.vector_x = 0
                self.vector_y = 0

                if self.state == 'CROUCHING':
                    self.stand()
                #elif self.last_state == 'FALLING' or self.last_state == 'H_FALLING':
                #    self.crouch()
            else:
                # ----------------------------------------------------------------------------------------------------------
                # DIRECTIONS

                if pressing_right and not pressing_left:
                    speed = self.speed
                    if sprinting:
                        speed *= 2
                    if crawling:
                        speed *= 0.7
                    self.move_right(speed)
                    self.block_right_border()

                elif pressing_left and not pressing_right:
                    speed = self.speed
                    if sprinting:
                        speed *= 2
                    if crawling:
                        speed *= 0.7
                    self.move_left(speed)
                    self.block_left_border()

                else:
                    self.vector_x = 0

                # ----------------------------------------------------------------------------------------------------------
                # JUMP

                if pressing_up:
                    if not flying:
                        if not airborne and not hanging:
                            self.airborne = True
                            hit = self.jump()
                            if hit:
                                self.hanging = True
                        elif hanging:
                            hit = self.jump()
                            if not hit:
                                self.hanging = False
                    else:
                        speed = self.speed / 100
                        self.move_up(speed)
                else:
                    self.hanging = False

                # ----------------------------------------------------------------------------------------------------------
                # CROUCH / SLIDE
                # TODO: Change crouch from hold to toggle in order to not necessitate the player to hold 3 buttons
                # TODO: FIX: HCJump is higher than HJump
                # TODO: Transfer slide to right/left movement in order to make Vector_X accurate (Low prio)
                if pressing_down:
                    if not flying:
                        self.crouch()
                        if airborne:
                            self.vector_y += self.speed * 8 * delta.time()
                        elif sprinting and can_slide and not hanging:
                            if pressing_right or sliding == 1:
                                if not sliding:
                                    self.slide_fx()
                                #self.slide(1)
                                self.sliding = 1
                                self.move_right(self.speed * 2)
                                self.block_right_border()
                                self.slide_tick_counter += delta.time()
                            elif pressing_left or sliding == -1:
                                if not sliding:
                                    self.slide_fx()
                                #self.slide(-1)
                                self.sliding = -1
                                self.move_left(self.speed * 2)
                                self.block_left_border()
                                self.slide_tick_counter += delta.time()
                            else:
                                self.can_slide = False
                            if self.slide_tick_counter >= 0.3:
                                self.can_slide = False
                                self.sliding = False
                                #self.stop_slide()
                                self.slide_tick_counter = 0
                        else:
                            self.can_slide = False
                    else:
                        speed = self.speed / 100
                        self.move_down(speed)

                else:
                    self.can_slide = True
                    #if self.sliding:
                    #    self.stop_slide()
                    self.sliding = False
                    self.stand()
                    self.slide_tick_counter = 0

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