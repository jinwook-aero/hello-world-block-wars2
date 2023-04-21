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
        self.game   = cur_game
        self.screen = cur_game.screen
        block_color = color
        turrent_color = [int(color[0]*0.7), int(color[1]*0.7), int(color[2]*0.7)]
        self.block  = Block(cur_game, x, y, theta, color, n_player, n_serial)
        self.turret = Turret(cur_game, self.block, turrent_color, n_player, n_serial)
                
        # Coordinates
        self.rect = self.block.rect
        
        self.x = self.block.x
        self.y = self.block.y
        
        self.x_dest = self.block.x
        self.y_dest = self.block.y
        
        self.x_target = self.turret.x_target
        self.y_target = self.turret.y_target
        
        # Speed
        self.vx = 0
        self.vy = 0
        
        # Ranges
        T_SET = cur_game.setting.turret
        self.R_recog = T_SET.R_recog;
        self.R_range = T_SET.R_range;
        
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
        
        # Fire
        self.is_firing = False

    def update(self):
        # Nearest target
        d_list = []
        x_list = []
        y_list = []
        n_indx = 0
        for block_turret in self.game.block_turrets.sprites():
            if (block_turret.n_player >= 0) and (block_turret.n_player != self.n_player):
                n_indx += 1
                d_cur = np.sqrt(np.square(block_turret.x-self.x)+np.square(block_turret.y-self.y))
                d_list.append(d_cur)
                x_list.append(block_turret.x)
                y_list.append(block_turret.y)
        
        # Acquire target
        self.turret.x_target = self.block.x + np.cos(self.block.theta*np.pi/180)*self.block.radius*0.1
        self.turret.y_target = self.block.y + np.sin(self.block.theta*np.pi/180)*self.block.radius*0.1
        self.is_firing = False
        if len(d_list)>0:
            n_min = np.argmin(d_list)
            d_min = d_list[n_min]
            x_min = x_list[n_min]
            y_min = y_list[n_min]                
            if d_min <= self.R_recog:
                self.turret.x_target = x_min
                self.turret.y_target = y_min
                if (d_min <= self.R_range) and (self.turret.is_aligned):
                    self.is_firing = True
        
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
        self.block.is_selected  = self.is_selected
        self.turret.is_selected = self.is_selected
        
        # Firing
        self.turret.is_firing = self.is_firing
        
        # Coordinates
        self.block.x_dest = self.x_dest
        self.block.y_dest = self.y_dest
        
    def set_velocity(self,vx_new,vy_new):
        self.vx       = vx_new
        self.vy       = vy_new
        self.block.vx = vx_new
        self.block.vy = vy_new
        self.block.v  = np.sqrt(np.square(vx_new) + np.square(vy_new))
    
    def set_position(self,x_new,y_new):
        self.x       = x_new
        self.y       = y_new
        self.block.x = x_new
        self.block.y = y_new
        
    def draw(self):
        self.block.draw()
        self.turret.draw()
        
    
