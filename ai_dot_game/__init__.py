"""
Init
"""

WIDTH, HEIGHT = 800, 800

BLACK = 0, 0, 0
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
WHITE = 255, 255, 255

MUTATE_RATIO = 0.5

TARGET_XY = (int(WIDTH/2), 5)
START_XY = (int(WIDTH/2), HEIGHT-5)  # start at the bottom centre
VECTOR_LEN = 10
POPULATION_SIZE = 1000
OBSTACLE_MODE = ('none', 'simple', 'medium', 'hard', 'rand')[3]
