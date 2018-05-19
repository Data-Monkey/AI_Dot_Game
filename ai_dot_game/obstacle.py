"""
an obstacle to make it harder for the dots.
draws a rectangle on the screen
checks if dot is inside the rect
"""

import pygame
from . import *

class Obstacle:
    """ the obstacle
    """
    def __init__(self, tlXY=(300, 400), width=100, height=20):
        self.tlXY = tlXY
        self.width = width
        self.height = height
        self.color = RED
        self.rect = [*self.tlXY, self.width, self.height]

    def show(self, screen):
        """ draw the obstacle on the screen
        """
        return pygame.draw.rect(screen, self.color, self.rect, 2)

    def collision(self, dotXY=(0, 0)):
        """ detect a collision
        """
        if (dotXY[0] >= self.tlXY[0] and
                dotXY[0] <= self.tlXY[0]+self.width and
                dotXY[1] >= self.tlXY[1] and
                dotXY[1] <= self.tlXY[1]+self.height):
            return True
        return False
