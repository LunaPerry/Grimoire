import pygame as pyg
from settings import *
vect = pyg.math.Vector2

class Player(pyg.sprite.Sprite):

    def __init__(self, game):
        """ Initialize Player Sprite """
        pyg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pyg.Surface((30,40))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.center = (W2, H2)

        # Position / Velocity / Acceleration
        self.pos = vect(W2, H2)
        self.vel = vect(0, 0)
        self.acc = vect(0, 0)

    def update(self):
        """ Updates Player Sprite """
        self.acc = vect(0, P_GRAVITY)
        keys = pyg.key.get_pressed()

        # Changes Acceleration left/right
        if keys[pyg.K_LEFT]:
            self.acc.x = -P_ACC
        if keys[pyg.K_RIGHT]:
            self.acc.x = P_ACC

        # Accounts for Friction
        self.acc.x += self.vel.x * P_FRICTION
        
        # Adds acceleration to Velocity
        # Changes Position
        self.vel += self.acc
        self.pos += self.vel + (0.5 * self.acc)

        # Wrap around the sides of the screen for testing purposes
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        #Sets sprite to new position
        self.rect.midbottom = self.pos
    
    def jump(self):
        """ Jump only if on a platform """
        self.rect.x += 1
        collision = pyg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if collision:
            self.vel.y = -20

class Platform(pyg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pyg.sprite.Sprite.__init__(self)
        # Create Image
        self.image = pyg.Surface((w, h))
        self.image.fill(WHITE)
        # Place rectangle
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y