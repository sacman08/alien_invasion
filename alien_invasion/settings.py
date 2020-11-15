class Settings:
    """A class to store settings for game."""
    
    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (105, 105, 105)
        
        # TODO Add dots for stars
        self.bg_stars = (255, 255, 51)
        
        #TODO Add rain drops to fall to bottom
        
        #Ship Settings
        self.ship_speed = 1.5
        
        #Ammo settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        
        #Alien Settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # Direction set to 1 = right; -1 = left movement
        self.fleet_direction = 1