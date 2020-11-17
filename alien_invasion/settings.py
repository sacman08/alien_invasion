class Settings:
    """A class to store settings for game."""
    
    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (0, 0, 0)
        
        # TODO Add dots for stars
        self.star_height = 1
        self.star_width = 1
        self.bg_stars = (255, 255, 51)
        
        #TODO Add rain drops to fall to bottom
        
        self.ship_limit = 2
        
        #Ammo settings
        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        
        #Alien Settings
        
        self.fleet_drop_speed = 10
        
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        #Ship Settings
        self.ship_speed = 2.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.5
        # Direction set to 1 = right; -1 = left movement
        self.fleet_direction = 1
        
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale