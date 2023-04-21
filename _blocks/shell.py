import pygame
import random
import time
import numpy as np
import copy
from pygame.sprite import Sprite

class Shell(Sprite):
    """ Class to manage block """
    def __init__(self, cur_game, turret):
        # Initialize
        super().__init__()
        self.screen = cur_game.screen
        self.screen_rect = cur_game.screen.get_rect()
        self.setting = cur_game.setting
        self.game    = cur_game
        self.fps     = self.setting.game.frame_per_second
        self.damage  = self.setting.shell.damage
        self.health  = self.setting.shell.health
        
        # Color from turret
        new_clr    = [0, 0, 0]
        turret_clr = turret.color
        mix_clr    = [150, 150, 150]
        weight     = 0.4
        for n_index in range(3):
            new_clr[n_index] = turret_clr[n_index]*(1-weight)+mix_clr[n_index]*weight
        self.color = new_clr
        
        # Original coordinates and attitude from turret
        self.turret = turret
        
        self.x0 = self.turret.xTip
        self.y0 = self.turret.yTip
        
        self.theta0 = copy.copy(self.turret.theta)
        
        # Current coordinate, attitude, and flying distance
        self.x        = self.x0
        self.y        = self.y0
        self.theta    = self.theta0
        self.d_flight = 0
                
        # Create rectangle
        self.width  = self.setting.shell.width
        self.height = self.setting.shell.height
        self.image  = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        
        self.image0 = self.image # Reserved original image
        self.rect = self.image.get_rect(center = (int(self.x),self.setting.screen.height-int(self.y)-self.height/2))
        
        # Speed
        self.v0 = self.setting.shell.move_speed
        self.vx = self.v0*np.cos(self.theta*np.pi/180) 
        self.vy = self.v0*np.sin(self.theta*np.pi/180)
        
        # Ranges
        self.R_range = cur_game.setting.turret.R_range;

        # Serial number from turret
        self.n_player = turret.n_player
        self.n_serial = turret.n_serial
        
    def update(self):
        # Fly
        self.x += self.vx
        self.y += self.vy
        
        # Update distance
        dx = self.x - self.x0
        dy = self.y - self.y0
        self.d_flight = np.sqrt(np.square(dx) + np.square(dy))
        
        # Update rect
        rect_x = int(self.x)
        rect_y = self.setting.screen.height - int(self.y)
        
        # Rotate the original image to avoid degradation
        # [Note] Base image oritation is theta = 90
        self.image = pygame.transform.rotate(self.image0, self.theta-90)
        self.rect  = self.image.get_rect(center = (rect_x,rect_y))
        self.screen.blit(self.image, self.rect)
        
    def draw(self):            
        # Blit the image
        self.screen.blit(self.image, self.rect)
        
    def set_damage(self,damage):
        self.health -= damage