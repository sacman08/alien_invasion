import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ Class to manage the ammo"""
    
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        # Create an ammo rect and position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        
        # Store the ammo position as a value
        self.y = float(self.rect.y)
        
        
    def update(self):
        """ move the ammo up the screen"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Draw the ammo on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)