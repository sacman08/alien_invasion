import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from ammo import Bullet
from alien import Alien
from random import randint


#TODO Add stars in the background (optional make random each game)
#TODO add rain that falls to bottom of screen

class AlienInvasion:
    """Overall class to manage the game."""
    
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((1200, 720))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        #Setup instance for stats for each game
        self.stats = GameStats(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        
    def run_game(self):
        """Start the main loop"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_ammo()
            self._update_aliens()
            self._update_screen()
            
    def _create_fleet(self):
        """Do the fleet!"""
        #Find alien rows with proper spacing
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        #Calc num of rows to fit on screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (7 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        #Create full fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
            
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        
    def _check_fleet_edges(self):
        #Check edges and changing alien movement as needed
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        #Drop one row, then change direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1            
                   
    def _check_events(self):
        """Respond to any key and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)  
                    
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                    
    def _check_keydown_events(self, event):
        """Responding to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_ammo()
            
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_ammo(self):
        """Create a new laser and add it to the group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_ammo = Bullet(self)
            self.bullets.add(new_ammo)
            
    def _ship_hit(self):
        #Responses to ship being hit by aliens
        #Reduce ship count
        self.stats.ships_left -= 1
        
        #Remove remaining aliens and ammo
        self.aliens.empty()
        self.ammo.empty()
        
        #Create a new fleet centered on ship
        self._create_fleet()
        self.ship.center_ship()
        
        #Wait to let comp process
        sleep(0.5)
            
            
    def _update_aliens(self):
        #Check alien position then update
        self._check_fleet_edges()
        #update where aliens are located
        self.aliens.update()
        
        #Look for the alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            #print("Your ship is hit!!!")
            
    def _update_ammo(self):
        #remove ammo as needed, add any new
        self.bullets.update()
    
        #Remove ammo past edge of top screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
        self._check_ammo_alien_collision()
        
    def _check_ammo_alien_collision(self):
        #Check to see if any rounds hit aliens; remove alien and ammo
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            #When all killed, destroy all ammo, make a new fleet
            self.bullets.empty()
            self._create_fleet()        
        
    def _update_screen(self):
        """Update image on screen, flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  
        self.aliens.draw(self.screen)
        
        # Make the draw screen viewable.        
        pygame.display.flip()
            

            
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()