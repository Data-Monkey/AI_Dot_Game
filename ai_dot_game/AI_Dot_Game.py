import sys
import pygame
from .population import Population
from .obstacles import Obstacles
from . import *


def draw_target():
    pygame.draw.circle(screen, GREEN, TARGET_XY, 8)
    

def initialise_game():
    """Initialises the game module and
       returns screen and population and obstacles
    """
    pygame.init()
    clockobject = pygame.time.Clock()
    clockobject.tick(1)
    pop = Population(POPULATION_SIZE)
    pop.randomize_instructions()
    obst = Obstacles(OBSTACLE_MODE)
    return pygame.display.set_mode((HEIGHT, WIDTH)), pop, obst


def play_game(screen, population, obstacles):
    while population.alive():
        draw_target()
        obstacles.show(screen)
        population.show(screen)
        population.update(obstacles=obstacles)
        pygame.display.flip()
        screen.fill(BLACK)


def end_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    screen, population, obstacles = initialise_game()
    stop = False
    while not stop: 
        pygame.display.update()
        play_game(screen, population, obstacles)
        population.calculate_fitness()
        print(f'Gen {population.generation} total fitness {population.total_fitness}')
        stop = population.stop_evolution()
        population = population.natural_selection()
    end_game()