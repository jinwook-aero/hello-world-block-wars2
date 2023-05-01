class SettingShell:
    """ A class to store shell settings """

    def __init__(self):
        self.move_speed = 2 # pixel/frame
        self.height = 5 # pixel
        self.width  = 2 # pixel
        
        self.health = 1 # Can penetrate up to health/damage
        self.damage = 1 # Damage to both enemy and shell itself


