import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ A class for the alien on the field"""
    
    def __init__(self, ai_game):
        """Initialize and start alien"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        """ Load the image and set react """
        self.image = pygame.image.load('images/alien_t.PNG')
        self.rect = self.image.get_rect()
        
        #Start new alien at top left of screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        
        #Store the alien horizontal position
        self.x = float(self.rect.x)
        
    def check_edges(self):
        #Tell me true if hit edge
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True    
        
    def update(self):
        #March the aliens
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        
        
    
        
        