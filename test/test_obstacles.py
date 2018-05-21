"""
Test module for the ObstacleS object.
"""
from ai_dot_game.obstacles import Obstacles

def create_obstacles():
    """ new obstacle
    """
    return Obstacles()


def test_new_obstacles():
    """ test a simple population
    """
    obst = Obstacles('none')
    assert len(obst.obstacles) == 0
    obst = Obstacles('simple')
    assert len(obst.obstacles) == 1
    obst = Obstacles('hard')
    assert len(obst.obstacles) == 2
    obst = Obstacles('rand')
    assert len(obst.obstacles) >= 3
    assert len(obst.obstacles) <= 5
    
    
def test_collision():
    """ test if a collision is detected
    """
    obst = Obstacles('none')
    # all dot outside obstacle
    assert obst.collision((5, 5)) == False
    obst = Obstacles('hard')
    # inside obstacles
    assert obst.collision((305, 305)) == True
    assert obst.collision((10, 405)) == True
