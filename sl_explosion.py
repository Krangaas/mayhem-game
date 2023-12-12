'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Explosion object for the game "Spacelancer".
'''
from sl_base_object import BaseObject

class Explosion(BaseObject):
    '''
    Explosion object representation, derived from MoveableObject.
    ----------
    Parameters
        image: str
            supports the following formats:
            JPG, PNG, GIF (non-animated), BMP, PCX, TGA (uncompressed), TIF, LBM, BPM, PGM, PPM, XPM
        position: 2 dim tuple (int,int)
            The position of the object on the screen.
        rotate_factor: int
            The rate at which the object rotates.
    '''

    def __init__(self, image, position, energy, rotate_factor):
        '''create an explosion.'''
        super().__init__(image, position, energy=energy)
        self.rotate_factor = rotate_factor


    def update(self):
        '''Update Explosion behaviour.'''

        self.rotate(self.rotate_factor)
        #self.movement()

        if self.energy <= 0:
            self.dead = True
        else:
            self.energy -= 1
