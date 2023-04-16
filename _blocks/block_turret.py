import pygame
import random
import time
import numpy as np
from pygame.sprite import Sprite

from block import Block
from turret import Turret

class BlockTurret(Sprite):
    """ Class to manage block+turret assy """
    def __init__(self, cur_game, x=-1, y=-1, theta=90, color=(100,100,100), n_player=0, n_serial=0):
        # Initialize
        super().__init__()
        self.screen = cur_game.screen
        self.block  = Block(cur_game, x, y, theta, color, n_player, n_serial)
        self.turret = Turret(cur_game, self.block, color)
                
        # Coordinates
        self.rect = self.block.rect
        
        self.x = self.block.x
        self.y = self.block.y
        
        self.x_dest = self.block.x
        self.y_dest = self.block.y
        
        self.x_target = self.block.x
        self.y_target = self.block.y + np.sin(theta)*self.screen.get_height()
        
        # Speed
        self.vx = 0
        self.vy = 0
        
        # Serial number
        self.n_player = n_player
        self.n_serial = n_serial
        
        # Select
        if n_player == 0:
            self.is_selectable = True
        else: # Cannot select other player's unit
            self.is_selectable = False
        self.is_selected = False
        
        # Serial number
        self.n_player = n_player
        self.n_serial = n_serial

    def update(self):
        # Element update
        self.block.update()
        self.turret.update()
        
        # Merge back to block_turret
        self.x    = self.block.x
        self.y    = self.block.y
        self.vx   = self.block.vx
        self.vy   = self.block.vy
        self.rect = self.block.rect
        
        # Selected
        self.block.is_selected = self.is_selected
        
        # Coordinates
        self.block.x_dest = self.x_dest
        self.block.y_dest = self.y_dest

        self.block.x_target = self.x_target
        self.block.y_target = self.y_target
        
        self.turret.x_target = self.x_target
        self.turret.y_target = self.y_target
        
    def draw(self):
        self.block.draw()
        self.turret.draw()
        
    
