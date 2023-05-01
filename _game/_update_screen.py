import pygame

def _update_screen(self):
    # Redraw screen
    self.screen.fill(self.setting.screen.background_color)
    
    # Draw block-turrets
    for block_turret in self.block_turrets.sprites():
        block_turret.draw()
        
    # Draw shells
    for shell in self.shells.sprites():
        shell.draw()

    # Display screen
    pygame.display.flip()