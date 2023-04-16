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
        
        self.objs = pygame.sprite.Group()
        self._set_game()
        
        # Start time
        self.clock = pygame.time.Clock()
        self.n_frame = 0
            
    def run_game(self):
        """Main game loop"""
        while True:            
            # Update inputs
            self._check_events()
            
            # Updates game
            self._update_game()
            
            # Update screen
            self._update_screen()
            
            # Frame rate
            self.clock.tick(self.setting.game.frame_per_second)            
          
    def _set_game(self):
        block_turrets = []
        N = 4
        for n in range(N):
            block_turret = BlockTurret(self, self.screen.get_width()*((n+1)/(N+1)), self.screen.get_height()*0.2,
                                90, (0,100,0), 0, n+1)
            block_turrets.append(block_turret)
        for block_turret in block_turrets:
            self.objs.add(block_turret)            
        
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
                for obj in self.objs.sprites():
                    if obj.is_selected == True:
                        obj.x_dest = mouse_x
                        obj.y_dest = mouse_y                     
                        
            elif event.type == pygame.KEYDOWN:
                # REF: https://www.pygame.org/docs/ref/key.html#pygame.key.name
                # Quit
                if event.key == pygame.K_q:
                    sys.exit()
                    
                # Select/Deselect all
                if (event.key == pygame.K_BACKQUOTE):    
                    all_selected_already = True                
                    for obj in self.objs.sprites():
                        if obj.is_selectable == True:
                            if obj.is_selected == False:
                                all_selected_already = False
                    for obj in self.objs.sprites():
                        if obj.is_selectable == True:
                            if all_selected_already == True:
                                obj.is_selected = False
                            else:
                                obj.is_selected = True
                                    
                # Control all
                if ((event.key == pygame.K_w) or
                    (event.key == pygame.K_a) or
                    (event.key == pygame.K_s) or
                    (event.key == pygame.K_d) or
                    (event.key == pygame.K_SPACE)):
                    
                    for obj in self.objs.sprites():
                        if obj.is_selectable and obj.is_selected:
                            if (event.key == pygame.K_w):
                                obj.x_dest = obj.x
                                obj.y_dest = obj.y+self.screen.get_height()
                            elif (event.key == pygame.K_a):
                                obj.x_dest = obj.x-self.screen.get_width()
                                obj.y_dest = obj.y
                            elif (event.key == pygame.K_s):
                                obj.x_dest = obj.x
                                obj.y_dest = obj.y-self.screen.get_height()
                            elif (event.key == pygame.K_d):
                                obj.x_dest = obj.x+self.screen.get_width()
                                obj.y_dest = obj.y
                            elif (event.key == pygame.K_SPACE):
                                obj.x_dest = obj.x+obj.vx*self.setting.game.frame_per_second*0.5
                                obj.y_dest = obj.y+obj.vy*self.setting.game.frame_per_second*0.5
                
                # Select each
                if ((event.key == pygame.K_1) or
                    (event.key == pygame.K_2) or
                    (event.key == pygame.K_3) or
                    (event.key == pygame.K_4)):
                    if (event.key == pygame.K_1):
                        n_cur = 1
                    elif (event.key == pygame.K_2):
                        n_cur = 2
                    elif (event.key == pygame.K_3):
                        n_cur = 3
                    elif (event.key == pygame.K_4):
                        n_cur = 4
                    for obj in self.objs.sprites():
                        if obj.is_selectable == True:
                            if obj.n_serial == n_cur:
                                obj.is_selected = True
                            else:
                                obj.is_selected = False
    
    def _select_block(self,mouse_pos):
        for obj in self.objs.sprites():
            if obj.is_selectable == True:
                if obj.rect.collidepoint(mouse_pos):
                    obj.is_selected = True
                else:
                    obj.is_selected = False
            
    def _update_game(self):
        # Object motions
        for obj in self.objs.sprites():
            obj.update()
        #self.objs.update()            
                
    def _update_screen(self):
        # Redraw screen
        self.screen.fill(self.setting.screen.background_color)
        for obj in self.objs.sprites():
            obj.draw()

        # Display screen
        pygame.display.flip()
        
if __name__ == '__main__':
    # Run the game
    bw = BlockWars2()
    bw.run_game()
