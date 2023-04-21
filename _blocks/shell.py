import pygame
import random
import time
import numpy as np
from pygame.sprite import Sprite

class Shell(Sprite):
    """ Class to manage block """

   def __init__(self, cur_game, turret, color, n_player, n_serial):
        # Initialize
        super().__init__()
        self.screen = cur_game.screen
        self.screen_rect = cur_game.screen.get_rect()
        self.setting = cur_game.setting
        self.game    = cur_game
        self.fps     = self.setting.game.frame_per_second
        
        # Original coordinates and attitude from turret
        xBase = copy.copy(self.turret.xBase)
        yBase = copy.copy(self.turret.xBase)
        
        xMid = copy.copy(self.turret.xMid)
        xMid = copy.copy(self.turret.xMid)
        
        self.x0 = xBase + (xBase-xMid)*2
        self.y0 = yBase + (yBase-yMid)*2
        
        self.theta0 = copy.copy(turret.theta)
        
        # Current coordinate and flying distance
        self.x = self.x0
        self.y = self.y0
        self.d = 0
                
        # Create rectangle
        self.width  = self.setting.shell.width
        self.height = self.setting.shell.height
        self.image  = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(color)
        
        self.image0 = self.image # Reserved original image
        self.rect = self.image.get_rect(center = (int(self.xMid),self.setting.screen.height-self.yMid-self.height/2))
        
        # Speed
        self.v0 = self.setting.shell.move_speed
        self.vx = self.v0*np.cos(self.theta*np.pi/180) 
        self.vy = self.v0*np.sin(self.theta*np.pi/180)
        
        # Ranges
        self.R_range = cur_game.setting.turret.R_range;

        # Serial number
        self.n_player = n_player
        self.n_serial = n_serial
        
    def update(self):
        # Fly
        self.x += self.vx
        self.y += self.vy
        
        # Update distance
        dx = self.x - self.x0
        dy = self.y - self.y0
        self.d = np.sqrt(np.square(dx) + np.square(dy))
        
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