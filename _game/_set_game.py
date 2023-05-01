from block_turret import BlockTurret

def _set_game(self,N_player,N_serial):
    block_turrets = []
    for n_player in range(N_player):
        for n_serial in range(N_serial):
            x_cur = self.screen.get_width()*((n_serial+1)/(N_serial+1))
            y_cur = self.screen.get_height()*(0.1+0.8*n_player)
            c_cur = self.setting.game.player_color[n_player]
            block_turret = BlockTurret(self, x_cur, y_cur, 90-180*n_player, c_cur, n_player, n_serial)
            block_turrets.append(block_turret)
        for block_turret in block_turrets:
            self.block_turrets.add(block_turret)