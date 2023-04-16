import pygame
import random
import time
import numpy as np
from pygame.sprite import Sprite

class Block(Sprite):
    """ Class to manage block """

    def __init__(self, cur_game, x=-1, y=-1, theta=90, color=(100,100,100)):
        # Initialize
        super().__init__()
        self.screen = cur_game.screen
        self.screen_rect = cur_game.screen.get_rect()
        self.setting = cur_game.setting

        # Coordinate and attitude
        self.x     = float(x)
        self.y     = float(y)
        self.theta = float(theta)
        
        # Create rectangle
        self.width  = self.setting.block.width
        self.height = self.setting.block.height
        self.image  = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(color)
        
        self.image0 = self.image # Reserved original image
        self.rect = self.image.get_rect(center = (int(self.x),self.setting.screen.height-self.y))
        
        # Speed
        self.v     = 0
        self.omega = 0
        
        # Destiation
        self.x_dest = self.x
        self.y_dest = self.y

        # Target
        self.x_target = self.x
        self.y_target = self.y
                
        # Select
        self.is_selectable = True
        self.is_selected = False

    def update(self):
        # Accel toward destination
        dx = self.x_dest - self.x
        dy = self.y_dest - self.y        
        
        v0 = self.setting.block.move_speed
        omega0 = self.setting.block.rotate_speed
        
        v_dot = self.setting.block.move_accel
        omega_dot = self.setting.block.rotate_accel
        
        dist = np.sqrt(np.square(dx) + np.square(dy))
        
        # Accel
        if dist>=self.width:
            self.v = min(v0,self.v+v_dot)
            dtheta = np.arctan2(dy,dx)*180/np.pi - self.theta
        elif dist<self.width*3 and self.v>0.1*v0:
            v_dot2 = -np.square(self.v)/(2*dist)
            self.v = max(0,self.v+v_dot2)
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
        
        vx = self.v*np.cos(self.theta*np.pi/180)
        vy = self.v*np.sin(self.theta*np.pi/180)
        
        # Coordinate and attitude
        self.x += vx
        self.y += vy
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
        # Screen height
        scr_height = self.setting.screen.height
        
        # Blit the image
        self.screen.blit(self.image, self.rect)
        
        # Circle base
        circleRad = self.width*0.45
        circlePos = (self.x,scr_height-self.y)
        pygame.draw.circle(self.screen, (0, 0, 0), circlePos, circleRad, 3)
        
        if self.is_selected:            
            # Circle
            circleRad = self.width
            circlePos = (self.x,scr_height-self.y)
            pygame.draw.circle(self.screen, (0, 255, 0), circlePos, circleRad, 1)
            
            # Destination line
            xy_dest1 = (self.x     , scr_height-self.y)
            xy_dest2 = (self.x_dest, scr_height-self.y_dest)
            pygame.draw.line(self.screen, (100, 200, 100), xy_dest1, xy_dest2, 1)
            
            # Target line
            xy_target1 = (self.x       , scr_height-self.y)
            xy_target2 = (self.x_target, scr_height-self.y_target)
            pygame.draw.line(self.screen, (200, 100, 100), xy_target1, xy_target2, 1)
        
    
