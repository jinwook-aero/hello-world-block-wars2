class SettingGame:
    """ A class to store game settings """

    def __init__(self):
        ## Frame
        self.frame_per_second = 60
        
        ## Player colors
        self.player_color = []
        
        # Counts
        self.N_player = 2
        self.N_serial = 6
        
        # Player 1 green
        self.player_color.append((50,150,50))
        
        # Player 2 red
        self.player_color.append((150,50,50))
                
        ## Flags
        # Game status
        self.is_active = False


