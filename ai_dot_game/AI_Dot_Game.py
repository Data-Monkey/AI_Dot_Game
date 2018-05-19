import sys
import pygame
import operator  #add TUPLES
import random
from functools import reduce
from .dot import Dot
from .population import Population
from . import *


def draw_target():
    pygame.draw.circle(screen, GREEN,TARGET_XY, 8)
    

def initialise_game():
    """Initialises the game module and returns screen and population"""
    pygame.init()
    clockobject = pygame.time.Clock()
    clockobject.tick(1)
    return pygame.display.set_mode((HEIGHT, WIDTH)), Population(POPULATION_SIZE)


def play_game(screen, population):
    while population.alive():
        draw_target()
        population.show()
        population.update()
        pygame.display.flip()
        screen.fill(BLACK)


def end_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    screen, population = initialise_game()
    stop = False
    while not stop: 
        pygame.display.update()
        play_game(screen, population)
        population.calculate_fitness()
        print(f'Gen {population.generation} total fitness {population.total_fitness}')
        stop = population.stop_criteria()
        population = population.natural_selection()
    end_game()
