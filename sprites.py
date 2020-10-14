import pygame as pyg
from settings import *
vect = pyg.math.Vector2

class Player(pyg.sprite.Sprite):
    def __init__(self):
        """ Initialize Player Sprite """
        pyg.sprite.Sprite.__init__(self)
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
        self.acc = vect(0, 0)
        keys = pyg.key.get_pressed()

        # Changes Acceleration left/right
        if keys[pyg.K_LEFT]:
            self.acc.x = -P_ACC
        if keys[pyg.K_RIGHT]:
            self.acc.x = P_ACC

        # Accounts for Friction
        self.acc += self.vel * P_FRICTION
        
        # Adds acceleration to Velocity
        # Changes Position
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # Wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        #Sets sprite to new position
        self.rect.center = self.pos