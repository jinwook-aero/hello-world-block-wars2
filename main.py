import sys
import pygame
import random

sys.path.append('_settings')
sys.path.append('_blocks')
sys.path.append('_game')
from setting import Setting

class BlockWars2:
    """Overall class for game operation"""

    def __init__(self):
        # Setup
        pygame.init()
        self.setting = Setting()
        
        self.screen = pygame.display.set_mode(
                (self.setting.screen.width,self.setting.screen.height))
        pygame.display.set_caption("Block Wars 2: Mouse Left/Right, `/1~8/F1~F4, W/A/S/D/Space, ESC")
        
        self.block_turrets = pygame.sprite.Group()
        self.shells = pygame.sprite.Group()
        
        # Start time
        self.clock = pygame.time.Clock()
        self.n_frame = 0
         
    # Import game methods
    from _check_events import _check_events
    from _random_enemy import _random_enemy
    from _select_block import _select_block
    from _set_game import _set_game
    from _update_game import _update_game
    from _update_screen import _update_screen
   
    def run_game(self):
        """Main game loop"""
        self._set_game(self.setting.game.N_player,self.setting.game.N_serial)
        while True:            
            # Update inputs
            self._check_events()
            
            # Updates game
            self._update_game()
            
            # Update screen
            self._update_screen()
            
            # Update random enemy movement
            self._random_enemy() 
            
            # Frame rate
            self.n_frame += 1
            self.clock.tick(self.setting.game.frame_per_second)
        
if __name__ == '__main__':
    # Run the game
    bw = BlockWars2()
    bw.run_game()
    