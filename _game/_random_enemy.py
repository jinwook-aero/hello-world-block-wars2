import pygame
import random

def _random_enemy(self):
    fps = self.setting.game.frame_per_second
    scr_width = self.screen.get_width()
    scr_height = self.screen.get_height()
    
    # Player group box
    N_player = self.setting.game.N_player
    x_min = [0]*N_player
    x_max = [0]*N_player
    y_min = [0]*N_player
    y_max = [0]*N_player
    for n_player in range(N_player):
        x_min[n_player] = scr_width/2
        x_max[n_player] = scr_width/2
        y_min[n_player] = scr_height/2
        y_max[n_player] = scr_height/2
        
    for block_turret in self.block_turrets.sprites():
        for n_player in range(N_player):
            if block_turret.n_player == n_player:
                x_min[n_player] = min(x_min[n_player],block_turret.x)
                x_max[n_player] = max(x_max[n_player],block_turret.x)
                
                y_min[n_player] = min(y_min[n_player],block_turret.y)
                y_max[n_player] = max(y_max[n_player],block_turret.y)
    
    for block_turret in self.block_turrets.sprites():
        if block_turret.n_player != 0: # Enemy block
            n_player = 0 # Aim player's blocks
            x1 = x_min[n_player]
            x2 = x_max[n_player]
            y1 = y_min[n_player]
            y2 = y_max[n_player]
            if self.n_frame<(fps*3):
                block_turret.x_dest = block_turret.x
                block_turret.y_dest = (y1+y2)/2
            elif (self.n_frame-fps*block_turret.n_serial) % (fps*4) == 0:
                if random.random()>0.25:
                    r1 = random.random()
                    r2 = random.random()
                    r3 = random.random()
                    r4 = random.random()
                    block_turret.x_dest = x1 + (x2-x1)*r1 + (r2-0.5)*scr_width*0.5
                    block_turret.y_dest = y1 + (y2-y1)*r3 + (r4-0.5)*scr_height*0.5