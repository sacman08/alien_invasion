
# Track stats for the game

class GameStats:
    
    def __init__(self, ai_game):
        #Initialize the stats
        self.settings = ai_game.settings
        self.reset_stats()
        #Make game active with stats
        self.game_active = True
        
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        