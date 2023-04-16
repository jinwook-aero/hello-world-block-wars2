class SettingGame:
    """ A class to store game settings """

    def __init__(self):
        ## Frame
        self.frame_per_second = 60
        
        ## Player colors
        self.player_color = []
        
        # Player 1 green
        self.player_color.append((100,200,100))
        
        # Player 2 red
        self.player_color.append((200,150,150))
        
        ## 
        
        ## Flags
        # Game status
        self.is_active = False


