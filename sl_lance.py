'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Lance object for the game "Spacelancer".
'''
import numpy as np
from sl_moveable_object import MoveableObject
from sl_config import LANCE_INFO
from sl_config import SCREEN_WIDTH
from sl_config import SCREEN_HEIGHT

class Lance(MoveableObject):
    '''
    Lance object representation, derived from MoveableObject.
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
        '''Create a lance/missile.'''
        super().__init__(image, position, energy=LANCE_INFO["energy"])
        self.angle = angle %360
        self.player = player

    def screen_wrap(self):
        '''Apply screen wrapping rules to object.'''
        super().screen_wrap() #apply screen wrapping method defined in parent class

        #destroy lance if it hits roof or floor
        if self.rect.centery < 0:   #TOP wrap
            self.dead = True
        if self.rect.centery > SCREEN_HEIGHT:   #BOT wrap
            self.dead = True


    def update(self):
        '''Update Lance behaviour.'''
        if self.energy <= 0:
            self.dead = True
        else:
            self.energy -= 1

        self.rotate(0)

        self.speed.x -= LANCE_INFO["acceleration_factor"] * np.sin(np.radians(self.angle))
        self.speed.y -= LANCE_INFO["acceleration_factor"] * np.cos(np.radians(self.angle))
        self.movement(LANCE_INFO["speed_limit"], LANCE_INFO["gravity"])
