import pygame
import random
import time
import numpy as np
from pygame.sprite import Sprite

class Block:
    """ Class to manage block """

    def __init__(self, cur_game, x, y, theta, color, n_player, n_serial):
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
        self.color  = color
        self.width  = self.setting.block.width
        self.height = self.setting.block.height
        self.radius = np.sqrt(np.square(self.width)+np.square(self.height))/2
        self.image  = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        
        self.image0 = self.image # Reserved original image
        self.rect = self.image.get_rect(center = (int(self.x),self.setting.screen.height-self.y))
        
        # Health
        self.health = self.setting.block.health
        
        # Speed        
        self.v0 = self.setting.block.move_speed
        self.omega0 = self.setting.block.rotate_speed     
        
        self.v     = 0
        self.vx    = 0
        self.vy    = 0
        
        # Accel
        self.v_dot = self.setting.block.move_accel
        self.omega_dot = self.setting.block.rotate_accel
        
        # Destiation
        self.x_dest = self.x
        self.y_dest = self.y
        
        # Select
        if n_player == 0:            
            self.is_selectable = True
        else:        
            self.is_selectable = False
        self.is_selected = False
        
        # Serial number
        self.n_player = n_player
        self.n_serial = n_serial
        
        self.text_serial_color = (255, 255, 255)
        self.text_health_color = (50, 255, 50)
        self.font = pygame.font.SysFont(None, 24)
                
    def update(self):
        # Accel toward destination
        dx = self.x_dest - self.x
        dy = self.y_dest - self.y
        
        dist_stop = np.square(self.v)/(2*self.v_dot)+0.1*self.width
        dist_cur  = np.sqrt(np.square(dx) + np.square(dy))
        
        # Accel
        if dist_cur>=dist_stop:
            self.v = min(self.v0,self.v+self.v_dot)
            dtheta = np.arctan2(dy,dx)*180/np.pi - self.theta
        else:
            if self.v>0.2*self.v0:
                self.v = max(0,self.v-self.v_dot)
                dtheta = np.arctan2(dy,dx)*180/np.pi - self.theta
            else:
                self.v = 0
                dtheta = 0
        
        dtheta %= 360            
        if dtheta>=1 and dtheta<=180:
            self.omega = min( self.omega0, self.omega + self.omega_dot)
        elif dtheta>180 and dtheta<360-1:
            self.omega = max(-self.omega0, self.omega - self.omega_dot)
        else:
            self.omega = 0
        
        self.vx = self.v*np.cos(self.theta*np.pi/180)
        self.vy = self.v*np.sin(self.theta*np.pi/180)
        
        # Coordinate and attitude
        self.x += self.vx
        self.y += self.vy
        self.theta += self.omega
        self.theta %= 360 
        
        # Coordinate limit
        xMin = self.radius
        xMax = self.setting.screen.width-self.radius
        yMin = self.height
        yMax = self.setting.screen.height-self.radius
        self.x = min(xMax,max(self.x,xMin))
        self.y = min(yMax,max(self.y,yMin))
        
        # Rectangle position
        rect_x = int(self.x)
        rect_y = self.setting.screen.height - int(self.y)
        
        # Rotate the original image to avoid degradation
        # [Note] Base image oritation is theta = 90
        self.image = pygame.transform.rotate(self.image0, self.theta-90)
        self.rect  = self.image.get_rect(center = (rect_x,rect_y))
        self.screen.blit(self.image, self.rect)
        
        # Serial number
        # [NOTE] Displayed after +1
        n_serial_str = str(self.n_serial+1)
        self.n_serial_image = self.font.render(
                n_serial_str, True, self.text_serial_color, self.setting.screen.background_color)
                
        # health
        health_str = str(self.health)
        self.health_image = self.font.render(
                health_str, True, self.text_health_color, self.setting.screen.background_color)

        # Display
        self.n_serial_rect = self.n_serial_image.get_rect()
        self.n_serial_rect.x = self.rect.x - self.width*0.7
        self.n_serial_rect.y = self.rect.y - self.height*0.5
        
        self.health_rect   = self.health_image.get_rect()
        self.health_rect.x = self.rect.x + self.width*1.5
        self.health_rect.y = self.rect.y - self.height*0.5
        
    def draw(self):
        # Screen height
        scr_height = self.setting.screen.height
        
        # Blit the image
        self.screen.blit(self.image, self.rect)
        
        # Serial number and life only for player
        if self.n_player == 0:
            self.screen.blit(self.n_serial_image, self.n_serial_rect)
            self.screen.blit(self.health_image, self.health_rect)
        
        # Circle base
        circleRad = self.width*0.45
        circlePos = (self.x,scr_height-self.y)
        pygame.draw.circle(self.screen, (0, 0, 0), circlePos, circleRad, 3)
        
        if self.is_selected:            
            # Circle
            circleRad = self.radius*1.2
            circlePos = (self.x,scr_height-self.y)
            pygame.draw.circle(self.screen, (0, 255, 0), circlePos, circleRad, 1)
            
            # Destination line
            xy_dest1 = (self.x     , scr_height-self.y)
            xy_dest2 = (self.x_dest, scr_height-self.y_dest)
            pygame.draw.line(self.screen, (100, 200, 100), xy_dest1, xy_dest2, 1)
    
