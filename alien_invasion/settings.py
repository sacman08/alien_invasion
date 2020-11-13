class Settings:
    """A class to store settings for game."""
    
    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (255, 255, 255)
        
        #Ship Settings
        self.ship_speed = 1.5
        
        #Ammo settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5