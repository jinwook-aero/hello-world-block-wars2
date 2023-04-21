import sys
import time
import random
import pygame
import numpy as np

sys.path.append('_settings')
sys.path.append('_blocks')

from setting import Setting
from block_turret import BlockTurret
from shell import Shell

class BlockWars2:
    """Overall class for game operation"""

    def __init__(self):
        # Setup
        pygame.init()
        self.setting = Setting()
        
        self.screen = pygame.display.set_mode(
                (self.setting.screen.width,self.setting.screen.height))
        pygame.display.set_caption("Block Wars 2: Mouse Left/Right, `, 1~0, W, A, S, D, Space, ESC")
        
        self.block_turrets = pygame.sprite.Group()
        self.shells = pygame.sprite.Group()        
        
        
        # Start time
        self.clock = pygame.time.Clock()
        self.n_frame = 0
            
    def run_game(self):
        """Main game loop"""    
        self._set_game()        
        while True:            
            # Update inputs
            self._check_events()
            
            # Updates game
            self._update_game()
            
            # Update screen
            self._update_screen()
            
            # Frame rate
            self.n_frame += 1
            self.clock.tick(self.setting.game.frame_per_second)            
          
    def _set_game(self):
        block_turrets = []
        N_player = 2
        N_serial = 8
        for n_player in range(N_player):
            for n_serial in range(N_serial):
                x_cur = self.screen.get_width()*((n_serial+1)/(N_serial+1))
                y_cur = self.screen.get_height()*(0.1+0.8*n_player)
                c_cur = self.setting.game.player_color[n_player]
                block_turret = BlockTurret(self, x_cur, y_cur, 90-180*n_player, c_cur, n_player, n_serial)
                block_turrets.append(block_turret)
            for block_turret in block_turrets:
                self.block_turrets.add(block_turret)
        
    def _check_events(self):        
        # watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                
            # Left click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                self._select_block(mouse_pos)
                        
            # Right click
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                mouse_x = mouse_pos[0]
                mouse_y = self.screen.get_height() - mouse_pos[1]
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selected == True:
                        block_turret.x_dest = mouse_x
                        block_turret.y_dest = mouse_y                     
            
            # Keys kept-pressed
            IS_W = pygame.key.get_pressed()[pygame.K_w]
            IS_A = pygame.key.get_pressed()[pygame.K_a]
            IS_S = pygame.key.get_pressed()[pygame.K_s]
            IS_D = pygame.key.get_pressed()[pygame.K_d]
            
            if IS_W or IS_A or IS_S or IS_D:
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selected == True:
                        block_turret.x_dest = block_turret.x
                        block_turret.y_dest = block_turret.y
                        if IS_W:
                            block_turret.y_dest = block_turret.y + self.screen.get_height()
                        if IS_A:
                            block_turret.x_dest = block_turret.x - self.screen.get_width()
                        if IS_S:
                            block_turret.y_dest = block_turret.y - self.screen.get_height()
                        if IS_D:
                            block_turret.x_dest = block_turret.x + self.screen.get_width()
                    
            # Key down
            elif (event.type == pygame.KEYDOWN):
                # REF: https://www.pygame.org/docs/ref/key.html#pygame.key.name
                # Quit
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                    
                # Select/Deselect all
                if (event.key == pygame.K_BACKQUOTE):    
                    all_selected_already = True                
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selectable == True:
                            if block_turret.is_selected == False:
                                all_selected_already = False
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selectable == True:
                            if all_selected_already == True:
                                block_turret.is_selected = False
                            else:
                                block_turret.is_selected = True
                                    
                # Stop blocks
                if (event.key == pygame.K_SPACE):
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selected == True:
                            t_scale = self.setting.block.move_speed/self.setting.block.move_accel*0.5
                            block_turret.block.omega = 0
                            block_turret.x_dest = block_turret.x + block_turret.vx*t_scale
                            block_turret.y_dest = block_turret.y + block_turret.vy*t_scale
                
                # Select/Deselect each
                if ((event.key == pygame.K_1) or
                    (event.key == pygame.K_2) or
                    (event.key == pygame.K_3) or
                    (event.key == pygame.K_4) or
                    (event.key == pygame.K_5) or
                    (event.key == pygame.K_6) or
                    (event.key == pygame.K_7) or
                    (event.key == pygame.K_8) or
                    (event.key == pygame.K_9) or
                    (event.key == pygame.K_0)):
                    if (event.key == pygame.K_1):
                        n_cur = 1 - 1
                    elif (event.key == pygame.K_2):
                        n_cur = 2 - 1
                    elif (event.key == pygame.K_3):
                        n_cur = 3 - 1
                    elif (event.key == pygame.K_4):
                        n_cur = 4 - 1
                    elif (event.key == pygame.K_5):
                        n_cur = 5 - 1
                    elif (event.key == pygame.K_6):
                        n_cur = 6 - 1
                    elif (event.key == pygame.K_7):
                        n_cur = 7 - 1
                    elif (event.key == pygame.K_8):
                        n_cur = 8 - 1
                    elif (event.key == pygame.K_9):
                        n_cur = 9 - 1
                    elif (event.key == pygame.K_0):
                        n_cur = 10 - 1
                        
                    # Check if already selected
                    is_selected_already = False
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selectable == True:
                            if block_turret.n_serial == n_cur:
                                if block_turret.is_selected:
                                    is_selected_already = True
                    
                    # Flip selection at target and delect else
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selectable == True:
                            if block_turret.n_serial == n_cur:
                                block_turret.is_selected = not is_selected_already
                            else:
                                block_turret.is_selected = False
                
                # Select/Deselect group
                if ((event.key == pygame.K_F1) or
                    (event.key == pygame.K_F2) or
                    (event.key == pygame.K_F3) or
                    (event.key == pygame.K_F4)):
                    if (event.key == pygame.K_F1):
                        n_min = 1 - 1
                        n_max = 2 - 1
                    elif (event.key == pygame.K_F2):
                        n_min = 3 - 1
                        n_max = 4 - 1
                    elif (event.key == pygame.K_F3):
                        n_min = 5 - 1
                        n_max = 6 - 1
                    elif (event.key == pygame.K_F4):
                        n_min = 7 - 1
                        n_max = 8 - 1
                        
                    # Check if already selected
                    is_selected_already = False
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selectable == True:
                            if (block_turret.n_serial >= n_min) and (block_turret.n_serial <= n_max):
                                if block_turret.is_selected:
                                    is_selected_already = True
                    
                    # Flip selection at target and delect else
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selectable == True:
                            if (block_turret.n_serial >= n_min) and (block_turret.n_serial <= n_max):
                                block_turret.is_selected = not is_selected_already
                            else:
                                block_turret.is_selected = False
                            
    def _select_block(self,mouse_pos):
        for block_turret in self.block_turrets.sprites():
            if block_turret.is_selectable == True:
                if block_turret.rect.collidepoint(mouse_pos):
                    block_turret.is_selected = True
                else:
                    block_turret.is_selected = False
            
    def _update_game(self):
        # Collision between block-turrets
        for b1 in self.block_turrets:
            for b2 in self.block_turrets:
                if b1 != b2:
                    if pygame.sprite.collide_rect(b1,b2):
                        # Position vector from 1 to 2
                        dx = b2.x - b1.x
                        dy = b2.y - b1.y
                        nx = dx/np.sqrt(np.square(dx) + np.square(dy))
                        ny = dy/np.sqrt(np.square(dx) + np.square(dy))         

                        # Relative velocity of 2 from 1
                        dvx = b2.vx - b1.vx
                        dvy = b2.vy - b1.vy
                        nvx = dvx/np.sqrt(np.square(dvx) + np.square(dvy))
                        nvy = dvy/np.sqrt(np.square(dvx) + np.square(dvy))   
                        
                        # Is colliding further
                        if (nx*nvx+ny*nvy)<0:
                            # Colliding velocity substracted
                            # Sign of b2 does not make sense
                            # But only this setup works for a reason idk why
                            b1.set_velocity(b1.vx*(1-nx), b1.vy*(1-ny))
                            b2.set_velocity(b2.vx*(1-nx), b2.vy*(1-ny))
                            
                            # Rebounding to avoid diffusion into each other
                            b1.set_position(b1.x - nx*b1.block.radius*0.04,
                                            b1.y - ny*b1.block.radius*0.04)
                        
        # Collision with shells
        for bt in self.block_turrets:
            for sh in self.shells:
                if pygame.sprite.collide_rect(bt,sh):
                    bt.set_damage(sh.damage)
                    sh.set_damage(sh.damage)
            
        # Block destroyed
        for block_turret in self.block_turrets.copy():
            if block_turret.health <= 0:
                self.block_turrets.remove(block_turret)
                
        # Shell destroyed
        for shell in self.shells.copy():
            if shell.health <= 0:
                self.shells.remove(shell)
                
        # Block-turret motions
        for block_turret in self.block_turrets.sprites():
            block_turret.update()
        
        # Shell fired
        for block_turret in self.block_turrets.sprites():
            T = block_turret.turret
            if T.fire_now:
                shell = Shell(self, T)
                self.shells.add(shell)
            
        # Shell vaninshed
        for shell in self.shells.copy():
            if shell.d_flight >= shell.R_range:
                self.shells.remove(shell)
                
        # Shell motions
        for shell in self.shells.sprites():
            shell.update()
            
    def _update_screen(self):
        # Redraw screen
        self.screen.fill(self.setting.screen.background_color)
        
        # Draw block-turrets
        for block_turret in self.block_turrets.sprites():
            block_turret.draw()
            
        # Draw shells
        for shell in self.shells.sprites():
            shell.draw()

        # Display screen
        pygame.display.flip()
        
if __name__ == '__main__':
    # Run the game
    bw = BlockWars2()
    bw.run_game()
    