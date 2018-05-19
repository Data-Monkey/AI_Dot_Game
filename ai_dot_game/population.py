"""
Population
"""

import random
from .dot import Dot
from . import *

class Population:
    """ Population of dots
    """
    def __init__(self, pop_size=10):
        self.generation = 1
        self.total_fitness = 0.0
        self.best_steps = 1000
        self.dots = [Dot() for i in range(pop_size)]
        # create the generation of dots
        #[self.dots.append(Dot()) for i in range(pop_size)]

#    def show_stats(self, screen):
#        screen.blit(font.render(f'Generation: {self.generation+1}', True, (255,0,0)), (10, 10))
#        pygame.display.update()
#
    def show(self, screen):
        """ ask all dots to show themselves
        """
        return [dot.show(screen) for dot in self.dots]

    def update(self):
        """ ask all dots to update themselves
        """
        return [dot.update(self.best_steps) for dot in self.dots]

    def calculate_fitness(self):
        """ get total fitness from all dots
        """
        self.total_fitness = sum([dot.calculate_fitness() for dot in self.dots])
        return self.total_fitness

    def randomize_instructions(self, size=1000):
        """ ask all dots to randomize
        """
        return [dot.randomize_instructions(size) for dot in self.dots]

    def alive(self):
        """ check if any dot is still alive
        """
        return (True in [dot.alive() for dot in self.dots])

    def natural_selection(self):
        """ create a new generation of dots
            find a parent to clone from for each dot
            the best dot of the current pop gets copied to new pop
        """

        def __create_new_dot__():
            """ make new dot, clone from parent, mutate
            """
            new_dot = self.select_parent()
            new_dot.mutate()
            return new_dot

        next_gen = Population(len(self.dots))
        # find a parent for all new dots and mutate them
        next_gen.dots = [__create_new_dot__() for i in range(len(next_gen.dots))]
        # keep the winner!
        next_gen.dots[0] = self.best_dot()
        next_gen.best_steps = self.best_steps
        next_gen.generation = self.generation + 1
        return next_gen

    def best_dot(self):
        """ find the best dot in the pop and clone it
        """
        best = Dot()
        for dot in self.dots:
            if dot.fitness > best.fitness:
                best = dot

        if best.reached_goal:
            #update best steps
            self.best_steps = best.step

        #only take the instructions
        best = best.clone()
        best.winner = True
        return best

    def select_parent(self):
        """ the fitness of each parent determines the likelyhood
            of being chosen to have babies (each baby only has 1 parent)
        """
        rand = random.uniform(0, self.total_fitness)
        running_sum = 0.0
        for dot in self.dots:
            running_sum += dot.fitness
            if running_sum >= rand:
                return dot.clone()
         # this should never happen
        return None

    def stop_evolution(self):
        """ if the population reached the goal
            stop the evolution
        """
        return self.total_fitness > 6
