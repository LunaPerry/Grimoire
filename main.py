import pygame as pyg
from settings import *
from sprites import *
from os import path
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
        # Matches font
        self.font_name = pyg.font.match_font(F_NAME)
        # High score
        self.dir = path.dirname(__file__)

        with open(path.join(self.dir, "score.txt"), 'r+') as file:
            # Shout out to Guzzy for helping me with this
            # If try has an error it will text hs to 0 instead
            try:
                self.hs = int(file.read())
            except:
                self.hs = 0

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
        self.score = 0

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
        self.text_io(str(self.score), 26, WHITE, W2, 20)
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

        # Game over condition
        if self.player.rect.bottom > HEIGHT:
            # Moves platforms down if player falls off screen and kills platforms
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 6)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        # Once all platforms are killed, end the game
        if len(self.platforms) == 0:
            self.playing = False

        # Handle camera movement
        # Camera Up
        if self.player.rect.top <= HEIGHT * 0.25:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    # Gain random score when platforms fall off the screen
                    self.score += random.randrange(10, 30)
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

    def key_wait(self):
        """ Checks events for a keypress """
        wait = True
        while wait:
            # Run loop at fps
            self.clock.tick(FPS)
            # Check events
            for event in pyg.event.get():
                # If quit, quit
                if event.type == pyg.QUIT:
                    wait = False
                    self.running = False
                # Any other event, wait is over
                if event.type == pyg.KEYUP:
                    wait = False

    def start_screen(self):
        """ Print Directions and Title, wait for key input to start game """
        # Fill screen and print title/directions
        self.screen.fill(BLACK)

        self.text_io("Grimoire", 40, WHITE, W2, HEIGHT * 0.10)
        self.text_io("Highscore: " + str(self.hs), 40, WHITE, W2, HEIGHT * 0.25)
        self.text_io("Arrows for movement", 30, WHITE, W2, HEIGHT * 0.40)
        self.text_io("Space for jump", 30, WHITE, W2, HEIGHT * 0.60)
        self.text_io("Press a key to start", 30, WHITE, W2, HEIGHT * 0.80)

        pyg.display.flip()
        # Wait for keypress function
        self.key_wait()

    def text_io(self, text, size, color, x, y):
        """ 
        Draw text to screen 
        
        Inputs: (Text to pass, Font Size, Font color, x location, y location)

        """
        # Set font size and color
        font = pyg.font.Font(self.font_name, size)
        # Create the surface with text, font and color. True is antialiasing
        text_surface = font.render(text, True, color)
        # Make it a rectangle
        text_rect = text_surface.get_rect()
        # Place the rectangle
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def game_over(self):
        """ Game Over Screen """
        # Fill screen and print end screen
        self.screen.fill(BLACK)

        self.text_io("You died", 50, WHITE, W2, HEIGHT * 0.20)
        self.text_io("Your score: " + str(self.score), 40, WHITE, W2, HEIGHT * 0.40)
        self.text_io("Press a key to play again", 40, WHITE, W2, HEIGHT * 0.80)

        if self.score > self.hs:
            self.hs = self.score
            self.text_io("Woot, new high score!", 50, WHITE, W2, HEIGHT * 0.60)
            with open(path.join(self.dir, "score.txt"), 'r+') as file:
                file.write(str(self.score))
        else:
            self.text_io("Highscore: " + str(self.hs), 35, WHITE, W2, HEIGHT * 0.60)

        pyg.display.flip()
        # Wait for keypresss function
        self.key_wait()


g = Game()
# Shows starting Screen
g.start_screen()

while g.running:
    g.newGame()
    g.game_over()

pyg.quit()