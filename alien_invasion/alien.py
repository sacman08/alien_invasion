import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """ A class for the alien on the field"""
    
    def __init__(self, ai_game):
        """Initialize and start alien"""
        super().__init__()
        self.screen = ai_game.screen
        
        """ Load the image and set react """
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        #Start new alien at top left of screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        
        #Store the alien horizontal position
        self.x = float(self.rect.x)
        
        