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
        self.platforms = pyg.sprite.Group()
        # Reference
        self.player = Player(self)

        self.all_sprites.add(self.player)
        for plat in PL_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.run()

    def draw(self):
        """ Draws to Screen """
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pyg.display.flip()

    def update(self):
        """ Updates Game """
        self.all_sprites.update()
        # Check for collision with platform if falling
        if self.player.vel.y > 0:
            collision = pyg.sprite.spritecollide(self.player, self.platforms, False)
            if collision:
                self.player.pos.y = collision[0].rect.top + 1
                self.player.vel.y = 0
        # Handle camera movement
        # Camera Up
        if self.player.rect.top <= HEIGHT * 0.25:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()

        # New platform spawns
        while len(self.platforms) < 7:
            width = random.randrange(45, 85)
            p = Platform(random.randrange(0, WIDTH-width), random.randrange(-75, -35), width, 20)

            self.platforms.add(p)
            self.all_sprites.add(p)


    def events(self):
        """ Checks for Events """
        for event in pyg.event.get():
            # Checks if x is pressed, quits game
            if event.type == pyg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            # Checks for space key to jump
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_SPACE:
                    self.player.jump()

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