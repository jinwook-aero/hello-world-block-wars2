def _select_block(self,mouse_pos):
    for block_turret in self.block_turrets.sprites():
        if block_turret.is_selectable == True:
            if block_turret.rect.collidepoint(mouse_pos):
                block_turret.is_selected = True
            else:
                block_turret.is_selected = False