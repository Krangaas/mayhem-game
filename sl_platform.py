'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Platform object for the game "Spacelancer".
'''
from sl_base_object import BaseObject

class Platform(BaseObject):
    '''
    Recharging platform representation, derived from baseObject.
    ----------
    Parameters
        image: str
            supports the following formats:
            JPG, PNG, GIF (non-animated), BMP, PCX, TGA (uncompressed), TIF, LBM, BPM, PGM, PPM, XPM
        position: 2 dim tuple (int,int)
            The position of the object on the screen.
        player: int
            The affiliation of the object, must be either 1 or 2.
    '''

    def __init__(self, image, position, player):
        '''Create a platform.'''
        super().__init__(image, position)
        self.player = player
