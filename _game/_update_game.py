import pygame
import numpy as np
from shell import Shell
from block_turret import BlockTurret

def _update_game(self):
    # Collision between block-turrets
    for b1 in self.block_turrets:
        for b2 in self.block_turrets:
            if b1 != b2:
                if pygame.sprite.collide_rect(b1,b2):
                    # Position vector from 1 to 2
                    dx = b2.x - b1.x
                    dy = b2.y - b1.y
                    nx = dx/np.sqrt(np.square(dx) + np.square(dy))
                    ny = dy/np.sqrt(np.square(dx) + np.square(dy))         

                    # Relative velocity of 2 from 1
                    dvx = b2.vx - b1.vx
                    dvy = b2.vy - b1.vy
                    nvx = dvx/np.sqrt(np.square(dvx) + np.square(dvy))
                    nvy = dvy/np.sqrt(np.square(dvx) + np.square(dvy))   
                    
                    # Is colliding further
                    if (nx*nvx+ny*nvy)<0:
                        # Colliding velocity substracted
                        # Sign of b2 does not make sense
                        # But only this setup works for a reason idk why
                        b1.set_velocity(b1.vx*(1-nx), b1.vy*(1-ny))
                        b2.set_velocity(b2.vx*(1-nx), b2.vy*(1-ny))
                        
                        # Rebounding to avoid diffusion into each other
                        b1.set_position(b1.x - nx*b1.block.radius*0.04,
                                        b1.y - ny*b1.block.radius*0.04)
                    
    # Collision with shells
    for bt in self.block_turrets:
        for sh in self.shells:
            if pygame.sprite.collide_rect(bt,sh):
                bt.set_damage(sh.damage)
                sh.set_damage(sh.damage)
        
    # Block destroyed
    for block_turret in self.block_turrets.copy():
        if block_turret.health <= 0:
            self.block_turrets.remove(block_turret)
            
    # Shell destroyed
    for shell in self.shells.copy():
        if shell.health <= 0:
            self.shells.remove(shell)
            
    # Block-turret motions
    for block_turret in self.block_turrets.sprites():
        block_turret.update()
    
    # Shell fired
    for block_turret in self.block_turrets.sprites():
        T = block_turret.turret
        if T.fire_now:
            shell = Shell(self, T)
            self.shells.add(shell)
        
    # Shell vaninshed
    for shell in self.shells.copy():
        if shell.d_flight >= shell.R_range:
            self.shells.remove(shell)
            
    # Shell motions
    for shell in self.shells.sprites():
        shell.update()