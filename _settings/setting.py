from setting_screen import SettingScreen
from setting_game import SettingGame
from setting_block import SettingBlock
from setting_turret import SettingTurret
from setting_bullet import SettingBullet

class Setting:
    """ A class to store all settings """

    def __init__(self):
        self.screen = SettingScreen()
        self.game = SettingGame()
        self.block = SettingBlock()
        self.turret = SettingTurret()
        self.bullet = SettingBullet()


