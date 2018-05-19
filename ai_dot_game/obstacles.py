"""
Obstacles - a collection of Obstacle
"""

import random
from .obstacle import Obstacle
from . import *

class Obstacles:
    """ collection of Obstacle
    """
    def __init__(self, mode='none'):
        self.mode = mode
        self.obstacles = []
        self.create_obstacles()

    def create_obstacles(self):
        """ create a set of obstacles depending on mode
        """
        if self.mode == 'simple':
            self.obstacles.append(Obstacle((300, 400), 400, 20))
        elif self.mode == 'medium':
            self.obstacles.append(Obstacle((100, 500), 300, 10))
        elif self.mode == 'hard':
            self.obstacles.append(Obstacle((300, 300), 500, 10))
            self.obstacles.append(Obstacle((0, 400), 500, 10))
        elif self.mode == 'rand':
            for i in range(random.randint(3, 5)):
                X = random.randint(0, WIDTH-10)
                Y = random.randint(50, HEIGHT-50)
                W = random.randint(10, WIDTH-X)
                H = random.randint(10, 20)
                self.obstacles.append(Obstacle((X, Y), W, H))

    def show(self):
        """ ask all obstacles to show themselves
        """
        return [obst.show() for obst in self.obstacles]

    def collision(self, dotXY):
        """ ask all obstacles in the dot collided
        """
        return (True in [obst.collision(dotXY) for obst in self.obstacles])
    