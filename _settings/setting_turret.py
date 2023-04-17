class SettingTurret:
    """ A class to store turret settings """

    def __init__(self):
        self.rotate_speed = 1.50 # rad/frame
        self.rotate_accel = 0.01 # speed increase/frame
        
        self.height = 22 # pixel
        self.width = 3 # pixel
        
        self.R_recog = 250
        self.R_range = 200
        
        self.dt_reload = 300 # frame



