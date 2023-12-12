'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Moveable object for the game "Spacelancer".
'''
from sl_base_object import BaseObject
from sl_config import SCREEN_WIDTH
from sl_config import SCREEN_HEIGHT
from sl_config import GRAVITY_FACTOR
from pygame.math import Vector2

class MoveableObject(BaseObject):
    '''
    Movable object representation, derived from BaseObject.
    ----------
    Parameters
        image: str
            supports the following formats:
                JPG, PNG, GIF (non-animated), BMP, PCX, TGA (uncompressed), TIF, LBM, BPM, PGM, PPM, XPM
        position: 2 dim tuple (int,int)
            The position of the object on the screen.
        health: int (optional)
            The health of the object.
        energy: int (optional)
            The energy of the object.
    '''

    def __init__(self, image, position, health=False, energy=False):
        '''Create a movable object.'''
        super().__init__(image, position, health, energy)
        self.speed = Vector2(0, 0)
        self.position = Vector2(position)


    def movement(self, limit, gravity=False):
        '''
        Move the object image and its rect.
        ----------
        Parameters
            gravity: bool (optional)
                Turn gravity on or off for object. Default is False.
            limit: int
                Speed limit of object.
        '''
        if gravity is True:
            self.speed.y += GRAVITY_FACTOR

        self.screen_wrap()
        self.limit_speed(limit)

        self.position += self.speed                      #update vector
        self.rect.center = (self.position.x, self.position.y)    #update sprite/rect position


    def screen_wrap(self):
        '''Apply screen wrapping rules to object.'''
        if self.rect.centerx > SCREEN_WIDTH + (self.rect.width)/2:  #RS wrap
            self.position.x = 0 - (self.rect.width)/2
            self.rect.center = (self.position.x, self.position.y)

        if self.rect.centerx < 0 - (self.rect.width)/2:     #LS wrap
            self.position.x = SCREEN_WIDTH + (self.rect.width)/2
            self.rect.center = (self.position.x, self.position.y)

        if self.rect.centery < 0:   #TOP wrap
            self.speed.y *= -0.5
            self.position.y += 1 #push the object back onto the screen

        if self.rect.centery > SCREEN_HEIGHT:   #BOT wrap
            self.dead = True


    def limit_speed(self, limit):
        '''
        Apply a limiting method to speed of object.
        limit: positive int.
        '''
        if limit < 1:
            limit = 1

        if self.speed.x > limit:
            self.speed.x = limit
        if self.speed.x < -limit:
            self.speed.x = -limit
        if self.speed.y > limit:
            self.speed.y = limit
        if self.speed.y < -limit:
            self.speed.y = -limit
