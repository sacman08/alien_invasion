import pygame


class Ship:
    
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        
        #Start at bottom middle
        self.rect.midbottom = self.screen_rect.midbottom
        
        #Store a value for horizontal position
        self.x = float(self.rect.x)
        
        #Movement Flags
        self.moving_right = False
        self.moving_left = False
        
        
    def update(self):
        """Update based on movement flag"""
        #Update the ship x value, not a constant rect decimal
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
            
        # Now update the rect object from x value
        self.rect.x = self.x
        
        
    def blitme(self):
        self.screen.blit(self.image, self.rect)