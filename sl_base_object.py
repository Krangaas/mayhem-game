'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Base object for the game "Spacelancer".
'''
import pygame
from pygame.math import Vector2

class BaseObject(pygame.sprite.Sprite):
    '''
    Base object representation, derived from pygame Sprite class.
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
        '''Create a static object.'''
        super().__init__()      #super() finds next class in search list
        #pygame rotate is destructive, we lose data on transforms.
        #perform transforms on original_image and save to image
        self.original_image = pygame.image.load(image) #image to transform
        self.image = self.original_image #image to show
        self.mask = pygame.mask.from_surface(self.image) #get mask from image
        self.rect = self.image.get_rect() #get rect from image
        self.rect.center = position
        self.angle = 0 % 360
        self.energy = energy
        self.health = health
        self.dead = False


    def rotate(self, theta):
        '''
        Rotate the object image and its rect.
        ----------
        Parameters
            theta: int
                Amount in degrees that the object will rotate.
        '''
        self.angle = (self.angle + theta) % 360 #increment the angle
        self.image = pygame.transform.rotate(self.original_image, self.angle) #rotate image counterclockwise
        self.rect = self.image.get_rect(center=self.rect.center) #get new rect from rotated image
