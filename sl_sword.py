'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Sword object for the game "Spacelancer".
'''
from sl_moveable_object import MoveableObject
from sl_config import SHIP_INFO

class Sword(MoveableObject):
    '''
    Sword object representation, derived from MoveableObject.
    ----------
    Parameters
        image: str
            supports the following formats:
            JPG, PNG, GIF (non-animated), BMP, PCX, TGA (uncompressed), TIF, LBM, BPM, PGM, PPM, XPM
        position: 2 dim tuple (int,int)
            The position of the object on the screen.
        angle: int
            The orientation of the object.
        player: int
            The affiliation of the object, must be either 1 or 2.
    '''

    def __init__(self, image, position, angle, player):
        '''Create a sword.'''
        super().__init__(image, position)
        self.angle = angle
        self.player = player


    def update(self):
        '''Update Sword behaviour.'''
        self.rotate(0)
        self.movement(SHIP_INFO["speed_limit"])
