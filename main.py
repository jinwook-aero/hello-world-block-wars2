import sys
import time
import random
import pygame
import numpy as np

sys.path.append('_settings')
sys.path.append('_blocks')

from setting import Setting
from block_turret import BlockTurret

class BlockWars2:
    """Overall class for game operation"""

    def __init__(self):
        # Setup
        pygame.init()
        self.setting = Setting()
        
        self.screen = pygame.display.set_mode(
                (self.setting.screen.width,self.setting.screen.height))
        pygame.display.set_caption("Block Wars 2: Mouse Left/Right, `, 1~4, W, A, S, D, Space")
        
        self.block_turrets = pygame.sprite.Group()        
        self.cannons = pygame.sprite.Group()
        
        
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
        N_serial = 4
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
                    
            # Key down
            elif (event.type == pygame.KEYDOWN):
                # REF: https://www.pygame.org/docs/ref/key.html#pygame.key.name
                # Quit
                if event.key == pygame.K_q:
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
                                    
                # Control start
                if ((event.key == pygame.K_w) or
                    (event.key == pygame.K_a) or
                    (event.key == pygame.K_s) or
                    (event.key == pygame.K_d) or
                    (event.key == pygame.K_SPACE)):
                    
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selectable and block_turret.is_selected:
                            if (event.key == pygame.K_w):
                                block_turret.y_dest = block_turret.y + self.screen.get_height()
                            if (event.key == pygame.K_a):
                                block_turret.x_dest = block_turret.x - self.screen.get_width()
                            if (event.key == pygame.K_s):
                                block_turret.y_dest = block_turret.y - self.screen.get_height()
                            if (event.key == pygame.K_d):
                                block_turret.x_dest = block_turret.x + self.screen.get_width()
                            elif (event.key == pygame.K_SPACE):
                                block_turret.x_dest = block_turret.x+block_turret.vx*self.setting.game.frame_per_second*0.5
                                block_turret.y_dest = block_turret.y+block_turret.vy*self.setting.game.frame_per_second*0.5
                
                # Select/Deselect each
                if ((event.key == pygame.K_1) or
                    (event.key == pygame.K_2) or
                    (event.key == pygame.K_3) or
                    (event.key == pygame.K_4)):
                    if (event.key == pygame.K_1):
                        n_cur = 1 - 1
                    elif (event.key == pygame.K_2):
                        n_cur = 2 - 1
                    elif (event.key == pygame.K_3):
                        n_cur = 3 - 1
                    elif (event.key == pygame.K_4):
                        n_cur = 4 - 1
                        
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
                                
            # Key up
            elif (event.type == pygame.KEYUP):   
                # Control end
                if ((event.key == pygame.K_w) or
                    (event.key == pygame.K_a) or
                    (event.key == pygame.K_s) or
                    (event.key == pygame.K_d) or
                    (event.key == pygame.K_SPACE)):
                    
                    for block_turret in self.block_turrets.sprites():
                        if block_turret.is_selectable and block_turret.is_selected:
                            if (event.key == pygame.K_w) or (event.key == pygame.K_s):
                                block_turret.y_dest = block_turret.y
                            if (event.key == pygame.K_a) or (event.key == pygame.K_d):
                                block_turret.x_dest = block_turret.x
    
    def _select_block(self,mouse_pos):
        for block_turret in self.block_turrets.sprites():
            if block_turret.is_selectable == True:
                if block_turret.rect.collidepoint(mouse_pos):
                    block_turret.is_selected = True
                else:
                    block_turret.is_selected = False
            
    def _update_game(self):
        # Object motions
        for block_turret in self.block_turrets.sprites():
            block_turret.update()     
                
    def _update_screen(self):
        # Redraw screen
        self.screen.fill(self.setting.screen.background_color)
        for block_turret in self.block_turrets.sprites():
            block_turret.draw()

        # Display screen
        pygame.display.flip()
        
if __name__ == '__main__':
    # Run the game
    bw = BlockWars2()
    bw.run_game()