import pygame
import sys

def _check_events(self):      
    # watch for keyboard and mouse events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
        # Left click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            self._select_block(mouse_pos)
                    
        # Right click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]
            mouse_y = self.screen.get_height() - mouse_pos[1]
            
            sum_x = 0
            sum_y = 0
            count_n = 0
            for block_turret in self.block_turrets.sprites():
                if block_turret.is_selected == True:
                    count_n += 1
                    sum_x += block_turret.x
                    sum_y += block_turret.y
            if count_n > 0:
                avg_x = sum_x/count_n
                avg_y = sum_y/count_n
            else:
                avg_x = 0
                avg_y = 0
                    
            for block_turret in self.block_turrets.sprites():
                if block_turret.is_selected == True:
                    cur_dx = (block_turret.x - avg_x)/2
                    cur_dy = (block_turret.y - avg_y)/2
                    
                    block_turret.x_dest = cur_dx + mouse_x
                    block_turret.y_dest = cur_dy + mouse_y
        
        # Keys kept-pressed
        IS_W = pygame.key.get_pressed()[pygame.K_w]
        IS_A = pygame.key.get_pressed()[pygame.K_a]
        IS_S = pygame.key.get_pressed()[pygame.K_s]
        IS_D = pygame.key.get_pressed()[pygame.K_d]
        
        if IS_W or IS_A or IS_S or IS_D:
            for block_turret in self.block_turrets.sprites():
                if block_turret.is_selected == True:
                    block_turret.x_dest = block_turret.x
                    block_turret.y_dest = block_turret.y
                    if IS_W:
                        block_turret.y_dest = block_turret.y + self.screen.get_height()
                    if IS_A:
                        block_turret.x_dest = block_turret.x - self.screen.get_width()
                    if IS_S:
                        block_turret.y_dest = block_turret.y - self.screen.get_height()
                    if IS_D:
                        block_turret.x_dest = block_turret.x + self.screen.get_width()
                
        # Key down
        elif (event.type == pygame.KEYDOWN):
            # REF: https://www.pygame.org/docs/ref/key.html#pygame.key.name
            # Quit
            if event.key == pygame.K_ESCAPE:
                sys.exit()
                
            # Select/Deselect all
            if (event.key == pygame.K_BACKQUOTE):    
                all_selected_already = True                
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selectable == True:
                        if block_turret.is_selected == False:
                            all_selected_already = False
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selectable == True:
                        if all_selected_already == True:
                            block_turret.is_selected = False
                        else:
                            block_turret.is_selected = True
                                
            # Stop blocks
            if (event.key == pygame.K_SPACE):
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selected == True:
                        t_scale = self.setting.block.move_speed/self.setting.block.move_accel*0.5
                        block_turret.block.omega = 0
                        block_turret.x_dest = block_turret.x + block_turret.vx*t_scale
                        block_turret.y_dest = block_turret.y + block_turret.vy*t_scale
            
            # Select/Deselect each
            if ((event.key == pygame.K_1) or
                (event.key == pygame.K_2) or
                (event.key == pygame.K_3) or
                (event.key == pygame.K_4) or
                (event.key == pygame.K_5) or
                (event.key == pygame.K_6) or
                (event.key == pygame.K_7) or
                (event.key == pygame.K_8) or
                (event.key == pygame.K_9) or
                (event.key == pygame.K_0)):
                if (event.key == pygame.K_1):
                    n_cur = 1 - 1
                elif (event.key == pygame.K_2):
                    n_cur = 2 - 1
                elif (event.key == pygame.K_3):
                    n_cur = 3 - 1
                elif (event.key == pygame.K_4):
                    n_cur = 4 - 1
                elif (event.key == pygame.K_5):
                    n_cur = 5 - 1
                elif (event.key == pygame.K_6):
                    n_cur = 6 - 1
                elif (event.key == pygame.K_7):
                    n_cur = 7 - 1
                elif (event.key == pygame.K_8):
                    n_cur = 8 - 1
                elif (event.key == pygame.K_9):
                    n_cur = 9 - 1
                elif (event.key == pygame.K_0):
                    n_cur = 10 - 1
                    
                # Check if already selected
                is_selected_already = False
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selectable == True:
                        if block_turret.n_serial == n_cur:
                            if block_turret.is_selected:
                                is_selected_already = True
                
                # Flip selection at target and delect else
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selectable == True:
                        if block_turret.n_serial == n_cur:
                            block_turret.is_selected = not is_selected_already
                        else:
                            block_turret.is_selected = False
            
            # Select/Deselect group
            if ((event.key == pygame.K_F1) or
                (event.key == pygame.K_F2) or
                (event.key == pygame.K_F3) or
                (event.key == pygame.K_F4)):
                if (event.key == pygame.K_F1):
                    n_min = 1 - 1
                    n_max = 2 - 1
                elif (event.key == pygame.K_F2):
                    n_min = 3 - 1
                    n_max = 4 - 1
                elif (event.key == pygame.K_F3):
                    n_min = 5 - 1
                    n_max = 6 - 1
                elif (event.key == pygame.K_F4):
                    n_min = 7 - 1
                    n_max = 8 - 1
                    
                # Check if already selected
                is_selected_already = False
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selectable == True:
                        if (block_turret.n_serial >= n_min) and (block_turret.n_serial <= n_max):
                            if block_turret.is_selected:
                                is_selected_already = True
                
                # Flip selection at target and delect else
                for block_turret in self.block_turrets.sprites():
                    if block_turret.is_selectable == True:
                        if (block_turret.n_serial >= n_min) and (block_turret.n_serial <= n_max):
                            block_turret.is_selected = not is_selected_already
                        else:
                            block_turret.is_selected = False