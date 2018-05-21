"""
Test module for the Population object.
"""
#import pygame
#from ai_dot_game.AI_Dot_Game import START_XY
from ai_dot_game.population import Population


def create_a_population():
    """ new small population of 5 dots
    """
    pop = Population(5)
    pop.randomize_instructions(8)
    return pop


def test_new_population():
    """ test a simple population
    """
    pop = Population(5)
    assert len(pop.dots) == 5
    # test default values
    assert pop.generation == 1
    assert pop.best_steps == 1000
    assert pop.total_fitness == 0
    # all dots are the same / empty
    assert len(pop.dots[1].instructions) == 0
    assert pop.dots[1].instructions == pop.dots[2].instructions

def test_randomize_instructions():
    """ test randomize_instructions
    """
    pop = create_a_population()
    assert len(pop.dots[1].instructions) == 8
    assert pop.dots[1].instructions != pop.dots[2].instructions
    
def test_best_dot():
    """ test the best dot is returned
    """
    pop = create_a_population()
    pop.dots[3].fitness = 0.123
    best = pop.best_dot()
    assert best.instructions == pop.dots[3].instructions
    # istructions are copied but everything else is reset
    assert best.winner == True
    assert best.fitness == 0
    assert best.step == 0
    
def test_stop_evolution():
    """ test evolution
    """
    pop = create_a_population()
    assert pop.stop_evolution() == False
    pop.total_fitness = 7
    assert pop.stop_evolution() == True
    
    
def test_select_parent():
    """parent is selcted by range of fitness.
       when there is only one parent with a fitness it is the only option
    """
    pop = create_a_population()
    pop.dots[3].fitness = 1
    pop.total_fitness = 1
    dot = pop.select_parent()
    assert dot.instructions == pop.dots[3].instructions
    
    