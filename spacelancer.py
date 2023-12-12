'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Game engine for the game Spacelancer. Run this module to play the game.

'''
import time
import random
import pygame
from sl_base_object import BaseObject
from sl_explosion import Explosion
from sl_platform import Platform
from sl_ship import Ship
from sl_config import *


class Engine:
    '''Spacelancer engine.'''

    def __init__(self):
        '''Initialize pygame, display and sprite Groups. Create title object and ground object.'''
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.all_ships = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_platforms = pygame.sprite.Group()
        self.all_lances = pygame.sprite.Group()
        self.all_swords = pygame.sprite.Group()
        self.all_explosions = pygame.sprite.Group()
        self.all_active_sprites = pygame.sprite.Group()
        self.ground = pygame.sprite.GroupSingle()
        self.ground.add(BaseObject("ground.png", ((SCREEN_WIDTH/2), SCREEN_HEIGHT-100)))
        self.title = pygame.sprite.GroupSingle()
        self.title.add(BaseObject("Title.png", ((SCREEN_WIDTH/2), 150)))


    def give_score(self, hit_player, score_increment):
        '''
        Increment the score attribute of the player that made a successful attack.
        ----------
        Parameters
            hit_player: int
                The affiliation of the player that got hit.
            score_increment: int
                The amount the score should be iIncremented.
        '''
        for ship in self.all_ships:
            if ship.player != hit_player:
                ship.score += score_increment


    def spawn_explosion(self, pos):
        '''
        Create three explosion objects on the screen.
        ----------
        Parameters
            pos: 2 dim tuple (int,int)
                Position on the screen where the object should spawn.
        '''
        for _ in range(3):
            position = (pos[0]+(random.choice([0, 5, 10])*random.choice([-1, 1])), pos[1]+random.choice([0, 5, 10])*random.choice([-1, 1]))
            explosion = Explosion("explosion.png", position, random.randint(50, 60), random.choice([1, 2, 3])*random.choice([-1, 1]))
            self.all_sprites.add(explosion)


    def spawn_ship(self, pinfo, score=0):
        '''
        Create a ship object on the screen.
        ----------
        Parameters
            pinfo: dict
                Dictionary containing player info, controls, health, etc.
            score: int (optional)
                Score accumulated by the player.
        '''

        #create a ship and add it to groups
        spaceship = Ship(pinfo["image"], pinfo["pos"], pinfo["player"], pinfo["controls"], pinfo["health"], pinfo["energy"], score)
        self.all_ships.add(spaceship)
        self.all_sprites.add(self.all_ships)


    def spawn_platform(self, pinfo):
        '''
        Create a platform object on the screen.
        ----------
        Parameters
            pinfo: dict
                Dictionary containing player info, controls, health, etc.
        '''
        platform = Platform(pinfo["base"], pinfo["pos"], pinfo["player"])
        self.all_platforms.add(platform)
        self.all_sprites.add(self.all_platforms)


    def despawn_objects(self, sprite):
        '''
        Destroy in-game objects.
        ----------
        Parameters
            sprite: class
                Derived from pygame.Sprite
        '''
        if sprite.__class__.__name__ == "Lance":
            self.spawn_explosion(sprite.position) #spawn Explosion object
            sprite.kill() #destroy object/remove sprite from all sprite groups
            return

        if sprite.__class__.__name__ == "Sword":
            sprite.kill() #destroy object/remove sprite from all sprite groups
            return

        if sprite.__class__.__name__ == "Ship":
            for _ in sprite.sword.sprites(): #if swords are deployed, destroy the object
                _.kill()
            sprite.thrust_image.kill()  #destroy thrust image
            sprite.score -= 10
            self.give_score(sprite.player, 50)
            self.spawn_explosion(sprite.position) #spawn Explosion object

            if sprite.player == 1:
                sprite.kill() #destroy object/remove sprite from all sprite groups
                self.spawn_ship(P1_INFO, sprite.score) #spawn new ship
                return

            if sprite.player == 2:
                sprite.kill() #destroy object/remove sprite from all sprite groups
                self.spawn_ship(P2_INFO, sprite.score) #spawn new ship
                return

        if sprite.__class__.__name__ == "Explosion":
            sprite.kill() #destroy object/remove sprite from all sprite groups
            return


    def object_collision(self, sprite, other):
        '''
        Handle collisions between objects.
        ----------
        Parameters
            sprite: class
                Must be a Sprite object or derived from pygame Sprite class
            other: class
                Must be a Sprite object or derived from pygame Sprite class
        '''
        if pygame.sprite.collide_rect(sprite, other) == 1:
            sprite.mask = pygame.mask.from_surface(sprite.image)
            #no need to generate a new mask for the object if it is static
            if self.all_active_sprites.has(other) is True:
                other.mask = pygame.mask.from_surface(other.image)

            if pygame.sprite.collide_mask(sprite, other):
                return True

        return False


    def ship_logic(self, ship):
        '''
        Handle ship logic such as collisions between ships and game objects, refueling, etc.
        ----------
        Parameters
            ship: class
                Must be a Ship object
        '''
        #check if a lance has been shot/check if sprite group is not empty
        if ship.lance.sprites():
            #pygame checks if the sprite is already part of a group automatically,
            #if true it doesn't add the sprite again
            self.all_lances.add(ship.lance)
            self.all_active_sprites.add(self.all_lances)
            self.all_sprites.add(self.all_active_sprites)

        if ship.sword.sprites(): #check if swords are deployed/check if sprite group is not empty
            #make sword position and angle mirror its ship position and angle
            ship.sword.sprites()[0].position = ship.position
            ship.sword.sprites()[0].angle = ship.angle

            #pygame checks if the sprite is already part of a group automatically,
            #if true it doesn't add the sprite again
            self.all_swords.add(ship.sword)
            self.all_active_sprites.add(self.all_swords)
            self.all_sprites.add(self.all_active_sprites)

        #make thrust image mirror its ship behaviour
        ship.thrust_image.position = ship.position
        ship.thrust_image.angle = ship.angle

        #create thrust visualization when thrusting
        if ship.thrust_on is True:
            self.all_sprites.add(ship.thrust_image)

        #remove visualization when not thrusting
        if self.all_sprites.has(ship.thrust_image) is True and ship.thrust_on is False:
            ship.thrust_image.remove(self.all_sprites)

        #ship and ship collision
        for other in self.all_ships:
            if ship.player != other.player:
                if self.object_collision(ship, other) is True:
                    ship.speed.x *= -1
                    ship.speed.y *= -1

        #ship and platform collision
        for other in self.all_platforms:
            if self.object_collision(ship, other) is True:
                ship.speed = ship.speed.reflect(ship.speed)
                ship.speed.scale_to_length(0.05)
                ship.position.y -= 1
                if ship.player == other.player:
                    ship.energy += 5

        #sword and ship collision
        for other in self.all_swords:
            if ship.player != other.player:
                if self.object_collision(ship, other) is True:
                    ship.health -= 1
                    self.give_score(ship.player, 1)

        #ground and ship collision
        for other in self.ground:
            if self.object_collision(ship, other) is True:
                ship.health -= 10
                ship.speed.x *= -0.7
                ship.speed.y *= -0.7


    def lance_logic(self, lance):
        '''
        Handle lance object logic such as colliding with static objects.
        ----------
        Parameters
            lance: class
                Must be a Lance object
        '''
        #lance and ship collision
        for other in self.all_ships:
            if  lance.player != other.player:
                if self.object_collision(lance, other) is True:
                    other.health -= 10
                    lance.dead = True
                    self.give_score(other.player, 10)

        #collision between lances and platforms
        for other in self.all_platforms:
            if self.object_collision(lance, other) is True:
                lance.dead = True

        #collision between lances and swords
        for other in self.all_swords:
            if lance.player != other.player:
                if self.object_collision(lance, other) is True:
                    lance.player = other.player
                    lance.speed = lance.speed.reflect(lance.speed)
                    lance.rotate(180)

        #collision between lances and the ground
        for other in self.ground:
            if self.object_collision(lance, other) is True:
                lance.dead = True


    def main_screen(self):
        '''Intro screen, displays control scheme.'''
        intro = True

        while intro is True:
            start = LARGE_FONT.render("Press SPACE to have at thee, foul knave!", False, WHITE)
            control1 = MEDIUM_FONT.render("Player 1 Controls: Thrust: W | Rotate: A, D | Deploy Swords: 2 | Lance: 1 ", False, WHITE)
            control2 = MEDIUM_FONT.render("Player 2 Controls: Thrust: UP | Rotate: LEFT, RIGHT | Deploy Swords: N | Lance: M ", False, WHITE)
            rules1 = MEDIUM_FONT.render("Accumulate score by hitting the opponent with swords and lances,", False, WHITE)
            rules2 = MEDIUM_FONT.render("but beware; abusing your arsenal will drain your energy levels very fast!", False, WHITE)
            rules3 = MEDIUM_FONT.render("The serfs will refuel your ship if you land on your platform.", False, WHITE)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        intro = False

            self.title.draw(self.screen)
            self.screen.blit(start, (((SCREEN_WIDTH)/2)-350, (SCREEN_HEIGHT/2)+60))
            self.screen.blit(rules1, (((SCREEN_WIDTH)/2)-350, (SCREEN_HEIGHT/2)-130))
            self.screen.blit(rules2, (((SCREEN_WIDTH)/2)-350, (SCREEN_HEIGHT/2)-100))
            self.screen.blit(rules3, (((SCREEN_WIDTH)/2)-350, (SCREEN_HEIGHT/2)-70))
            self.screen.blit(control1, (10, (SCREEN_HEIGHT/2)+300))
            self.screen.blit(control2, (10, (SCREEN_HEIGHT/2)+360))
            pygame.display.flip()


    def scoreboard(self):
        '''Update scoreboard on screen.'''
        for ship in self.all_ships:
            if ship.player == 1:
                player1_info1 = SMALL_FONT.render("Player: 1", False, WHITE)
                player1_info2 = SMALL_FONT.render("Score: %s | Energy: %2.f | Health: %s" %(ship.score, ship.energy, ship.health), False, WHITE)
                self.screen.blit(player1_info1, (0, 0))
                self.screen.blit(player1_info2, (0, 20))

            if ship.player == 2:
                player2_info1 = SMALL_FONT.render("Player: 2", False, WHITE)
                player2_info2 = SMALL_FONT.render("Score: %s | Energy: %2.f | Health: %s" %(ship.score, ship.energy, ship.health), False, WHITE)
                self.screen.blit(player2_info1, (SCREEN_WIDTH-290, 0))
                self.screen.blit(player2_info2, (SCREEN_WIDTH-290, 20))


    def play(self):
        '''Starts the game loop.'''

        self.spawn_ship(P1_INFO)
        self.spawn_platform(P1_INFO)
        self.spawn_ship(P2_INFO)
        self.spawn_platform(P2_INFO)
        self.all_active_sprites.add(self.all_ships)
        self.all_sprites.add(self.all_active_sprites)
        self.all_sprites.add(self.ground)
        self.all_sprites.add(self.all_platforms)
        self.main_screen() #access the main screen

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        #exits game when pressing ESC
                        pygame.quit()

            #kill dead objects
            for sprite in self.all_sprites:
                if sprite.dead is True:
                    self.despawn_objects(sprite)

            for lance in self.all_lances:
                self.lance_logic(lance)

            for ship in self.all_ships:
                self.ship_logic(ship)

            #update objects, draw and display
            self.screen.fill(BLACK)
            self.all_sprites.update()
            self.all_sprites.draw(self.screen)
            self.scoreboard()
            self.clock.tick(FPS)
            pygame.display.flip()


if __name__ == "__main__":
    Engine.play(Engine())
