"""
Test module for the Obstacle object.
"""
from ai_dot_game.obstacle import Obstacle
from ai_dot_game.AI_Dot_Game import RED,GREEN

def create_an_obstacle():
    """ new obstacle
    """
    return Obstacle((10, 20), 30, 40)


def test_new_obstacle():
    """ test a simple population
    """
    obst = create_an_obstacle()
    assert obst.rect == [10,20,30,40]
    assert obst.tlXY == (10,20)
    assert obst.width == 30
    assert obst.height == 40
    assert obst.color == RED
    
def test_collision():
    """ test if a collision is detected
    """
    obst = create_an_obstacle()
    # dot outside obstacle
    assert obst.collision((5,5)) == False
    # dot inside obstacle
    assert obst.collision((25,25)) == True
    