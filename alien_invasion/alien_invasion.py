import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from ammo import Bullet
from alien import Alien
from random import randint


#TODO Add stars in the background (optional make random each game)
#TODO add rain that falls to bottom of screen
#TODO Store high score premanently to display each time game starts fresh.

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
        #Setup the scoreboard
        self.sb = Scoreboard(self)
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        #Make the play button
        self.play_button = Button(self, 'Play')
        
        
    def run_game(self):
        """Start the main loop"""
        while True:
            self._check_events()
            
            if self.stats.game_active:
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
        available_space_y = (self.settings.screen_height - (5 * alien_height) - ship_height)
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button(self, mouse_pos):
        #Start a game if mouse click on play button
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
                       
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            
            #Hide the mouse while playing
            pygame.mouse.set_visible(False)
                    
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
        if self.stats.ships_left > 0:
            
            #Reduce ship count
            self.stats.ships_left -= 1
            #Reduce ships left shown on screen
            self.sb.prep_ships()
        
            #Remove remaining aliens and ammo
            self.aliens.empty()
            self.bullets.empty()
        
            #Create a new fleet centered on ship
            self._create_fleet()
            self.ship.center_ship()
        
            #Wait to let comp process
            sleep(0.5)
            
        else:
            self.stats.game_active = False
            #Reshow the mouse once game ends
            pygame.mouse.set_visible(True)
        
    def _check_aliens_bottom(self):
        #Check if any aliens made to bottom without hitting ship
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #same results with aliens as if hitting ship
                self._ship_hit()
                break
            
            
    def _update_aliens(self):
        #Check alien position then update
        self._check_fleet_edges()
        #update where aliens are located
        self.aliens.update()
        
        #Look for the alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #Look for aliens getting to bottom without collision
        self._check_aliens_bottom()
        
        
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
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            
        if not self.aliens:
            #When all killed, destroy all ammo, make a new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            #Increase the level
            self.stats.level += 1
            self.sb.prep_level()
        
    def _update_screen(self):
        """Update image on screen, flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  
        self.aliens.draw(self.screen)
        
        #Draw the scoring information on screen
        self.sb.show_score()
        
        #Show the Play button from init while game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        # Make the draw screen viewable.        
        pygame.display.flip()
            

            
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()