class SettingBlock:
    """ A class to store block settings """

    def __init__(self):
        self.move_speed   = 0.5 # pixel/frame
        self.rotate_speed = 1.0 # degree/frame
        
        self.move_accel   = 0.005 # speed increase/frame
        self.rotate_accel = 0.01# speed increase/frame
        
        self.height = 25 # pixel
        self.width = 20 # pixel


