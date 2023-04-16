import sys
import time
import random
import pygame

sys.path.append('_settings')
sys.path.append('_blocks')

from setting import Setting
from block import Block
from turret import Turret

class BlockWars2:
    """Overall class for game operation"""

    def __init__(self):
        # Setup
        pygame.init()
        self.setting = Setting()
        
        self.screen = pygame.display.set_mode(
                (self.setting.screen.width,self.setting.screen.height))
        pygame.display.set_caption("Block Wars 2")
        
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
        block = Block(self, self.screen.get_width()/2, self.screen.get_height()/2, 90, (0,100,0))
        turret = Turret(self, block, (0,100,0))
        self.objs.add(block) 
        self.objs.add(turret) 
        
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
                # Quit
                if event.key == pygame.K_q:
                    sys.exit()
    
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
