import pygame.font

class Button:
    
    def __init__(self, ai_game, msg):
        #init button attribs
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        #set the size and prop of butotn
        self.width, self.height = 200, 50
        self.button_color = (0, 155, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        #Build the button rect and center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        #Prep the button msg once
        self._prep_msg(msg)
        
        
    def _prep_msg(self, msg):
        #Make the msg a rendered image
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        
    def draw_button(self):
        #Draw a button and put new msg on it
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)