"""
Test module for the Dot object.
"""
import pygame
from ai_dot_game.AI_Dot_Game import Dot, START_XY
from ai_dot_game.dot import generate_instructions


def create_a_dot():
    return Dot()


def test_new_dot():
    dot = create_a_dot()
    assert dot.posXY == START_XY


def test_generate_instructions():
    new_instructions = generate_instructions()
    assert len(new_instructions) == 1000
    other_instructions = generate_instructions()
    assert new_instructions != other_instructions


def test_mutate():
    one_dot = create_a_dot()
    one_dot_instructions = one_dot.instructions[:]
    other_dot = create_a_dot()
    assert one_dot.instructions != other_dot.instructions
    one_dot.mutate()
    assert one_dot_instructions != one_dot.instructions


def test_fitness():
    dot = create_a_dot()
    assert dot.fitness == 0.0
    first_fit = dot.calculate_fitness()
    assert first_fit > 0.0


def test_fitness_when_reaching_target():
    dot = create_a_dot()
    dot.reached_goal = True
    dot.step = 1
    fit = dot.calculate_fitness()
    assert fit == 10000.00625


def test_move():

    def move():
        dot.move()
        return dot.step

    dot = create_a_dot()
    assert dot.step == 0
    steps = [move() for step in range(1000)]
    assert steps == [step for step in range(1, 1001)]