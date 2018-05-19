"""
Dot Object
"""
import random
import pygame
import operator  #add TUPLES
from . import *


def random_vector():
    X = random.randint(VECTOR_LEN*(-1),VECTOR_LEN)
    Y = random.randint(VECTOR_LEN*(-1),VECTOR_LEN)
    return [X,Y]


def generate_instructions(num = 1000):
    return [random_vector() for i in range(num)]


class Dot:
    def __init__(self):
        self.instructions = generate_instructions(1000)
        self.posXY = START_XY
        self.dead = False
        self.reached_goal = False
        self.winner = False
        self.step= 0
        self.fitness =0.00

    def _distance(self, posA=(0,0), posB=(0,0)):
        dx = abs(posA[0] - posB[0])
        dy = abs(posA[1] - posB[1])
        return int((dx**2 + dy**2)**0.5)     

    def show(self, screen):
        if self.winner:
            pygame.draw.circle(screen, BLUE, self.posXY,3)            
        elif self.reached_goal:
            pygame.draw.circle(screen, RED, self.posXY,1)
        else:
            pygame.draw.circle(screen, WHITE, self.posXY,1)
        
    def move(self, move_limit=1000):
        if min(len(self.instructions), move_limit) > self.step:
            #still instructions left to do
            self.posXY = tuple(map(operator.add, self.posXY, self.instructions[self.step]))
            self.step += 1
        else:
            self.dead = True
            
    def update(self, move_limit=1000):
        # move the dot if it is still alive
        if self.alive() :
            self.move(move_limit)
        # check if that move killed the dot
        if (self.posXY[0]<3 or self.posXY[1]<3 or 
           self.posXY[0]>WIDTH-3 or self.posXY[1]>HEIGHT-3):
            self.dead = True
        # or has the dot reached the target?
        elif self._distance(self.posXY,TARGET_XY) < 5 :
            self.reached_goal = True
            
            
    def calculate_fitness(self):
        # fitness is a function of distance to target
        # if target reached it is a function of steps taken
        
        if self.reached_goal:
            #self.fitness = 1.0/16.0 
            self.fitness = 1.0/160.0 + 10000.00/float(self.step**2);
            #print(f'steps {self.step} / fitness {self.fitness*1000}')
        else:
            dist = self._distance(self.posXY, TARGET_XY)
            if dist == 0.0:
                self.fitness = 0.0
            else:
                self.fitness = 1.00 / (dist**2)
            
            #print(f'distance {dist} / fitness {float(self.fitness*1000)} / steps {self.step}')
        return self.fitness
    
    def alive(self):
        return not (self.reached_goal or self.dead)
    
    def clone(self):
         clone = Dot()
         clone.instructions = self.instructions[:]
         return clone

    def mutate(self):

        def __no_mutation__():
            return random.random() < MUTATE_RATIO

        self.instructions = [inst if __no_mutation__() else random_vector() for inst in self.instructions]