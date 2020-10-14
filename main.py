import pygame as pyg
from settings import *
from sprites import *
import random

class Game:
    def __init__(self):
        """ Initialize Game Window etc """
        pyg.init()
        # Initialize mixer for sounds
        pyg.mixer.init() 
        # Create Window
        self.screen = pyg.display.set_mode((WIDTH, HEIGHT))
        # Handles speed
        self.clock = pyg.time.Clock()
        # Set running for while loop
        self.running = True

    def run(self):
        """ Main Game Loop """
        self.playing = True
        while self.playing:
            # Game clock
            self.clock.tick(FPS)
            # Checks for events
            self.events()
            # Updates
            self.update()
            # Draws to screen
            self.draw()
        
    def newGame(self):
        """ Starts a new game """
        # Group Sprites
        self.all_sprites = pyg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()

    def draw(self):
        """ Draws to Screen """
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pyg.display.flip()

    def update(self):
        """ Updates Game """
        self.all_sprites.update()

    def events(self):
        """ Checks for Events """
        for event in pyg.event.get():
            # Checks if x is pressed, quits game
            if event.type == pyg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def start_screen(self):
        """ Starting Screen """
        pass

    def game_over(self):
        """ Game Over Screen """
        pass

g = Game()
# Shows starting Screen
g.start_screen()

while g.running:
    g.newGame()
    g.game_over()

pyg.quit()