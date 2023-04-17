import pygame
import random
import time
import numpy as np
import copy
from pygame.sprite import Sprite

#class Turret(Sprite):
class Turret:
    """ Class to manage turret """

    def __init__(self, cur_game, block, color, n_player, n_serial):
        # Initialize
        super().__init__()
        self.screen = cur_game.screen
        self.screen_rect = cur_game.screen.get_rect()
        self.setting = cur_game.setting
        self.game    = cur_game
        self.fps     = self.setting.game.frame_per_second
        
        # Link with block
        self.block = block

        # Coordinates
        self.xBase = copy.copy(self.block.x)
        self.yBase = copy.copy(self.block.y)
        
        self.xMid  = copy.copy(self.xBase)
        self.yMid  = copy.copy(self.yBase)
        
        # Attitude and target copied from block
        self.theta    = copy.copy(block.theta)
        self.x_target = copy.copy(block.x)
        self.y_target = copy.copy(block.y)
        
        # Create rectangle
        self.width  = self.setting.turret.width
        self.height = self.setting.turret.height
        self.image  = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(color)
        
        self.image0 = self.image # Reserved original image
        self.rect = self.image.get_rect(center = (int(self.xMid),self.setting.screen.height-self.yMid-self.height/2))
        
        # Speed
        self.omega  = 0   
        self.omega0 = self.setting.turret.rotate_speed     
        
        # Ranges
        T_SET = cur_game.setting.turret
        self.R_recog = T_SET.R_recog;
        self.R_range = T_SET.R_range;
                
        # Select
        self.is_selectable = False
        self.is_selected = False
        
        # Firing
        self.is_aligned = False
        self.is_firing = False
        self.t_last    = 0
        self.dt_reload = self.setting.turret.dt_reload
        self.dt_left   = 0

        # Serial number
        self.n_player = n_player
        self.n_serial = n_serial
        
        # Milisecond
        self.text_color = (255, 0, 0)
        self.font = pygame.font.SysFont(None, 12)
        
    def update(self):
        # Base sync with block position
        self.xBase = self.block.x
        self.yBase = self.block.y
        
        # Update angle
        self.theta += self.omega+self.block.omega
        self.theta %= 360 
            
        # Toward target
        dx = self.x_target - self.xBase
        dy = self.y_target - self.yBase     
        
        omega_dot = self.setting.turret.rotate_accel
        
        dist = np.sqrt(np.square(dx) + np.square(dy))
        
        # Accel
        if dist>=self.block.radius*0.05:
            dtheta = np.arctan2(dy,dx)*180/np.pi - self.theta
        else:
            self.v = 0
            dtheta = 0
        
        dtheta %= 360   
        tol = 1 # Rotation within 1 deg
        if dtheta>=tol and dtheta<=180:
            self.omega = min( self.omega0, self.omega + omega_dot)
        elif dtheta>180 and dtheta<360-tol:
            self.omega = max(-self.omega0, self.omega - omega_dot)
        else:
            self.omega = 0
            
        tol = 5 # Aim within 5 deg
        if dtheta>=tol and dtheta<=180:
            self.is_aligned = False
        elif dtheta>180 and dtheta<360-tol:
            self.is_aligned = False
        else:
            self.is_aligned = True
                
        # Coordinate and attitude
        self.xMid = self.xBase + np.cos(self.theta*np.pi/180)*self.height*0.5
        self.yMid = self.yBase + np.sin(self.theta*np.pi/180)*self.height*0.5
        
        rect_x = int(self.xMid)
        rect_y = self.setting.screen.height - int(self.yMid)
        
        # Rotate the original image to avoid degradation
        # [Note] Base image oritation is theta = 90
        self.image = pygame.transform.rotate(self.image0, self.theta-90)
        self.rect  = self.image.get_rect(center = (rect_x,rect_y))
        self.screen.blit(self.image, self.rect)
        
        # Firing counter
        t_cur = self.game.n_frame
        if self.is_firing:
            # Trigger when ready
            if (t_cur>=self.t_last + self.dt_reload): # Fire now
                self.t_last  = t_cur
                self.dt_left = self.dt_reload
            else:
                self.dt_left = self.dt_reload - (t_cur - self.t_last)
        else:
            self.dt_left = 0            
        sec_str = str(int(self.dt_left/self.fps*100)/100)
        self.sec_image = self.font.render(
                sec_str, True, self.text_color, self.setting.screen.background_color)

        # Display
        self.sec_rect = self.sec_image.get_rect()
        self.sec_rect.x = self.block.rect.x + self.block.width*1.5
        self.sec_rect.y = self.block.rect.y + self.block.height*0.2
        
    def draw(self):            
        # Blit the image
        self.screen.blit(self.image, self.rect)
        
        # Milisec only for player
        if self.n_player == 0:
            self.screen.blit(self.sec_image, self.sec_rect)
            
        # Selected info
        if self.is_selected:
            # Screen information
            scr_height = self.setting.screen.height
            
            # Target acquisition
            xy_target1 = (self.xBase   , scr_height-self.yBase   )
            xy_target2 = (self.x_target, scr_height-self.y_target)
            pygame.draw.line(self.screen, (200, 100, 100), xy_target1, xy_target2, 1)
            
            # Range line colors
            back_clr  = self.setting.screen.background_color
            range_clr = [255, 0, 0]
            recog_clr = [0, 255, 0]
            range_w = 0.1
            recog_w = 0.15
            
            range_clr_mix = [0, 0, 0]
            recog_clr_mix = [0, 0, 0]
            for n_index in range(3):
                range_clr_mix[n_index] = back_clr[n_index]*(1-range_w)+range_clr[n_index]*range_w
                recog_clr_mix[n_index] = back_clr[n_index]*(1-recog_w)+recog_clr[n_index]*recog_w
            
            # Ranges
            circlePos = (self.xBase,scr_height-self.yBase)
            pygame.draw.circle(self.screen, range_clr_mix, circlePos, self.R_range, 1)
            pygame.draw.circle(self.screen, recog_clr_mix, circlePos, self.R_recog, 1)

