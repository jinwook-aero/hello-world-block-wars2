import pygame
import random
import time
import numpy as np
from pygame.sprite import Sprite

class Turret(Sprite):
    """ Class to manage turret """

    def __init__(self, cur_game, block, color):
        # Initialize
        super().__init__()
        self.screen = cur_game.screen
        self.screen_rect = cur_game.screen.get_rect()
        self.setting = cur_game.setting
        
        # Link with block
        self.block = block

        # Coordinate and attitude
        self.x     = block.x
        self.y     = block.y
        self.theta = block.theta
        
        # Create rectangle
        self.width  = self.setting.turret.width
        self.height = self.setting.turret.height
        self.image  = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(color)
        
        self.image0 = self.image # Reserved original image
        self.rect = self.image.get_rect(center = (int(self.x),self.setting.screen.height-self.y-self.height/2))
        
        # Speed
        self.omega = 0
        
        # Target
        self.x_target = block.x_target
        self.y_target = block.y_target
                
        # Select
        self.is_selectable = False
        self.is_selected = False

    def update(self):
        # Toward target
        dx = self.x_target - self.x
        dy = self.y_target - self.y        
        
        omega0 = self.setting.turret.rotate_speed
        omega_dot = self.setting.turret.rotate_accel
        
        dist = np.sqrt(np.square(dx) + np.square(dy))
        
        # Accel
        if dist>=self.block.width:
            dtheta = np.arctan2(dy,dx)*180/np.pi - self.theta
        else:
            self.v = 0
            dtheta = 0
        
        dtheta %= 360            
        if dtheta>=1 and dtheta<=180:
            self.omega = min( omega0, self.omega + omega_dot)
        elif dtheta>180 and dtheta<360-1:
            self.omega = max(-omega0, self.omega - omega_dot)
        else:
            self.omega = 0
                
        # Coordinate and attitude
        self.x = self.block.x + np.cos(self.theta*np.pi/180)*self.height/2
        self.y = self.block.y + np.sin(self.theta*np.pi/180)*self.height/2
        self.theta += self.omega
        self.theta %= 360 
        
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
