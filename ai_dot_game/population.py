from .dot import Dot
import random
from . import *


class Population:
    def __init__(self, pop_size=10):
        self.generation = 1
        self.total_fitness = 0
        self.best_steps = 1000
        self.dots = []
        # create the generation of dots
        [self.dots.append(Dot()) for i in range(pop_size)]
            
            
    def show(self, screen):
        [dot.show(screen) for dot in self.dots]
            
    def update(self):
        [dot.update(self.best_steps) for dot in self.dots]

    def calculate_fitness(self):
        self.total_fitness = sum([dot.calculate_fitness() for dot in self.dots])
        return self.total_fitness
            
    def alive(self):
        for dot in self.dots:
            if dot.alive():
                return True
        return False  # nobody alive
    
    def natural_selection(self):

        def __create_new_dot__():
            newDot = self.select_parent()
            newDot.mutate()
            return newDot

        nextGen = Population(len(self.dots))
        # find a parent for all new dots and mutate them
        nextGen.dots = [__create_new_dot__() for i in range(len(nextGen.dots))]
        # keep the winner!
        nextGen.dots[0] = self.best_dot()
        nextGen.best_steps = self.best_steps
        nextGen.generation = self.generation + 1
        return nextGen
    
    def best_dot(self):
        best = Dot()
        for dot in self.dots:
            if dot.fitness > best.fitness:
                best = dot
        
        if best.reached_goal:
            #update best steps
            self.best_steps = best.step
            print (f'best steps: {self.best_steps}')
            print (f'best fitness: {best.fitness}')
        
        #only take the instructions
        best = best.clone()
        best.winner = True
        return best

    def select_parent(self):
        multiplier = 100000
        rand = random.randint(0,int(self.total_fitness*multiplier))
        
        running_sum = 0.000        
        for dot in self.dots:
            running_sum += (dot.fitness*multiplier)
            if running_sum > rand:
                return dot.clone()
        
        # this should never happen
        return dot[1].clone()
            
    def stop_criteria(self):
        return self.total_fitness > 6