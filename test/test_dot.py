"""
Test module for the Dot object.
"""
#import pygame
from ai_dot_game.AI_Dot_Game import START_XY
from ai_dot_game.dot import Dot


def create_a_dot():
    """ new dot with randomized instructions (Generation 1)
    """
    dot = Dot()
    dot.randomize_instructions()
    return dot


def test_new_dot():
    """ test a simple dot
    """
    dot = create_a_dot()
    assert dot.posXY == START_XY


def test_randomize_instructions():
    """ test randomizer
    """
    new_instructions = Dot().randomize_instructions()
    assert len(new_instructions) == 1000
    other_instructions = Dot().randomize_instructions()
    assert new_instructions != other_instructions


def test_mutate():
    """ test mutation (before vs after)
    """
    one_dot = create_a_dot()
    one_dot_instructions = one_dot.instructions[:]
    other_dot = create_a_dot()
    assert one_dot.instructions != other_dot.instructions
    one_dot.mutate()
    assert one_dot_instructions != one_dot.instructions


def test_fitness():
    """ initial fitness = 0
    """
    dot = create_a_dot()
    assert dot.fitness == 0.0
    first_fit = dot.calculate_fitness()
    assert first_fit > 0.0


def test_fitness_when_reaching_target():
    """ test fitness when reached target
    """
    dot = create_a_dot()
    dot.reached_goal = True
    dot.step = 1
    fit = dot.calculate_fitness()
    assert fit == (1.0/16.0 + 1000.0)


def test_move():
    """ test move
    """

    def move():
        dot.move()
        return dot.step

    dot = create_a_dot()
    # dot starts with step 0
    assert dot.step == 0
    # 1000 moves
    steps = [move() for step in range(1000)]
    assert steps == [step for step in range(1, 1001)]
