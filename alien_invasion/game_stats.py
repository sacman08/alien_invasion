
# Track stats for the game

class GameStats:
    
    def __init__(self, ai_game):
        #Initialize the stats
        self.settings = ai_game.settings
        self.reset_stats()
        
        #Make game inactive until they press play
        self.game_active = False
        
    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        