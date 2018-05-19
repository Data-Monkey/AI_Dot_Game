"""
Dot Object
"""
import random
import operator  # addition of TUPLES
import pygame
from . import *




#def generate_instructions(num=1000):
#    return [random_vector() for i in range(num)]

def random_vector():
    """ generate a random vector
    """
    X = random.randint(VECTOR_LEN*(-1), VECTOR_LEN)
    Y = random.randint(VECTOR_LEN*(-1), VECTOR_LEN)
    return [X, Y]

def distance(posA=(0, 0), posB=(0, 0)):
    """ calculate distance between dots
        use pytagoras ...
    """
    dx = abs(posA[0] - posB[0])
    dy = abs(posA[1] - posB[1])
    return int((dx**2 + dy**2)**0.5)

# -------------------------------------------------------------
class Dot:
    """ give me a dot 
    """
    def __init__(self):
        self.instructions = []
        self.posXY = START_XY
        self.dead = False
        self.reached_goal = False
        self.winner = False
        self.step = 0
        self.fitness = 0.00

    def randomize_instructions(self, size=1000):
        """ give me some random instructions
            only used for first generation
        """
        for i in range(size):
            XY = random_vector()
            self.instructions.append(XY)
        return self.instructions

    def show(self, screen):
        """ draw dot on screen
        """
        if self.winner:
            pygame.draw.circle(screen, BLUE, self.posXY, 3)
        elif self.reached_goal:
            pygame.draw.circle(screen, RED, self.posXY, 1)
        else:
            pygame.draw.circle(screen, WHITE, self.posXY, 1)

    def move(self, move_limit=1000):
        """ if there are more instructions left, calculate new position
        """
        if min(len(self.instructions), move_limit) > self.step:
            #still instructions left to do
            self.posXY = tuple(map(operator.add, self.posXY, self.instructions[self.step]))
            self.step += 1
        else:
            self.dead = True

    def update(self, obstacles, move_limit=1000):
        """ check if the dot is still alive and move if appropriate
        """
        if self.alive():
            self.move(move_limit)
        # check if that move killed the dot
        if (self.posXY[0] < 3 or self.posXY[1] < 3 or
            self.posXY[0] > WIDTH-3 or self.posXY[1] > HEIGHT-3):
            self.dead = True
        # or hit an abstacle
        elif obstacles.collision(self.posXY):
            self.dead = True
        # or has the dot reached the target?
        elif distance(self.posXY, TARGET_XY) < 4:
            self.reached_goal = True

    def calculate_fitness(self):
        """ fitness is a function of distance to target
            if target reached it is a function of steps taken
        """
        dist = distance(self.posXY, TARGET_XY)
        if self.reached_goal:
            self.fitness = 1.0/16.0 + 1000.0/self.step
        else:
            self.fitness = 1.00 / (dist**2)
        return self.fitness

    def alive(self):
        """ am I alive?
        """
        return not (self.reached_goal or self.dead)

    def clone(self):
        """ just return the instructions as a clone
        """
        clone = Dot()
        clone.instructions = self.instructions[:]
        return clone

    def mutate(self):
        """ make some random changes to the instructions
        """
        def __no_mutation__():
            """ determine if a mutation is in order
            """
            return random.random() < MUTATE_RATIO

        self.instructions = [inst if __no_mutation__() else random_vector() for inst in self.instructions]
