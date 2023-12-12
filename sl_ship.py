'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Ship object for the game "Spacelancer".
'''
import pygame
import numpy as np
from sl_moveable_object import MoveableObject
from sl_config import SHIP_INFO
from sl_lance import Lance
from sl_sword import Sword
from sl_thrust import Thrust


class Ship(MoveableObject):
    '''
    Spaceship object representation, derived from MoveableObject.
    ----------
    Parameters
        image: str
            supports the following formats:
            JPG, PNG, GIF (non-animated), BMP, PCX, TGA (uncompressed), TIF, LBM, BPM, PGM, PPM, XPM
        position: 2 dim tuple (int,int)
            The position of the object on the screen.
        player: int
            The affiliation of the object, must be either 1 or 2.
        controls: dict
            Control scheme of the player.
        health: int
            The health of the object.
        energy: int
            The energy of the object.
        score: int
            The accumulated score of the player.
    '''

    def __init__(self, image, position, player, controls, health, energy, score):
        '''Create a spaceship.'''
        super().__init__(image, position, health, energy)
        self.controls = controls
        self.player = player
        self.score = score
        self.lance = pygame.sprite.GroupSingle()
        self.sword = pygame.sprite.GroupSingle()
        self.thrust_image = Thrust("thrust.png", self.rect.center, self.angle, self.player)
        self.thrust_on = False
        self.swords_deployed = False
        self.attack_tick = 0


    def control_ship(self):
        '''User input handler.'''
        key = pygame.key.get_pressed()

        if key[self.controls["Thrust"]]:
            if self.energy > 0.0:
                self.thrust_on = True
                self.speed.x -= SHIP_INFO["acceleration_factor"] * np.sin(np.radians(self.angle))
                self.speed.y -= SHIP_INFO["acceleration_factor"] * np.cos(np.radians(self.angle))
                self.energy -= SHIP_INFO["energy_burn_factor"]
        else:
            self.thrust_on = False

        if key[self.controls["Left"]]:
            self.rotate(SHIP_INFO["rotation_factor"])

        if key[self.controls["Right"]]:
            self.rotate(-(SHIP_INFO["rotation_factor"]))

        if key[self.controls["Lance"]]:
            self.shoot_lance()

        if key[self.controls["Sword"]]:
            self.deploy_swords()


    def shoot_lance(self):
        '''Create a Missile object with same position and orientation as ship.'''
        if not self.lance and self.energy >= 5: #check if sprite group is empty
            self.lance.add(Lance("lance.png", self.rect.center, self.angle, self.player))
            self.energy -= 5


    def deploy_swords(self):
        '''Create a Sword object with same position and orientation as ship.'''
        if not self.sword and self.attack_tick == 0:
            self.sword.add(Sword("sword.png", self.rect.center, self.angle, self.player))
            self.sword.sprites()[0].rotate(0)
            self.attack_tick = SHIP_INFO["attack_timer"]
            self.swords_deployed = True
            return

        if self.sword and self.attack_tick == 0:
            self.sword.sprites()[0].dead = True
            self.attack_tick = SHIP_INFO["attack_timer"]
            self.swords_deployed = False
            return


    def limit_speed(self, limit):
        '''
        Apply a limiting method to speed of object.
        limit: positive int.
        '''
        if self.swords_deployed is True:
            limit = limit - 2

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


    def update(self):
        '''Update Ship behaviour.'''
        self.control_ship()
        self.movement(SHIP_INFO["speed_limit"], SHIP_INFO["gravity"])

        if self.attack_tick > 0:
            self.attack_tick -= 1

        if self.health <= 0:
            self.dead = True

        if self.health > SHIP_INFO["health"]:
            self.health = SHIP_INFO["health"]

        if self.energy > SHIP_INFO["energy"]:
            self.energy = SHIP_INFO["energy"]

        if self.swords_deployed and self.energy > 0.0:
            self.energy -= 0.1
