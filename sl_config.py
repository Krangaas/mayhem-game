'''
                             ##  Assignment 3  ##
                                ## INF-1400 ##
                              ##  Magus Kanck ##
                                ##  mka080  ##

Config file for the game "Spacelancer".
'''
import pygame.font


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_SIZE = SCREEN_WIDTH,SCREEN_HEIGHT
FPS = 60

#Ship attributes
SHIP_INFO =  {
             "speed_limit": 5,
             "rotation_factor": 5,
             "acceleration_factor": 0.2,
             "health": 100,
             "energy": 500,
             "energy_burn_factor": 0.25,
             "attack_timer": 60,
             "gravity": True
             }

#Lance attributes
LANCE_INFO = {
             "speed_limit": 15,
             "acceleration_factor": 0.25,
             "energy": 100,
             "gravity": True
             }

#Gravitation
GRAVITY_FACTOR = 0.02

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Player 1 Constants
P1_INFO = {
           "image":"P1.png",
           "pos":(200,SCREEN_HEIGHT-200),
           "player": 1,
           "controls": {
                       "Thrust":pygame.K_w,
                       "Left":pygame.K_a,
                       "Right":pygame.K_d,
                       "Brake":pygame.K_s,
                       "Lance":pygame.K_1,
                       "Sword":pygame.K_2
                       },
           "health": SHIP_INFO["health"],
           "energy": SHIP_INFO["energy"],
           "base": "P1_platform.png"
          }

#Player 2 Constants
P2_INFO = {
          "image":"P2.png",
          "pos":(SCREEN_WIDTH-200,SCREEN_HEIGHT-200),
          "player": 2,
          "controls": {
                      "Thrust":pygame.K_UP,
                      "Left":pygame.K_LEFT,
                      "Right":pygame.K_RIGHT,
                      "Brake":pygame.K_DOWN,
                      "Lance":pygame.K_m,
                      "Sword":pygame.K_n
                      },
          "health": SHIP_INFO["health"],
          "energy": SHIP_INFO["energy"],
          "base": "P2_platform.png"
          }


#Fonts
pygame.font.init()
SMALL_FONT = pygame.font.SysFont("Arial", 20)
MEDIUM_FONT = pygame.font.SysFont("Arial", 30)
LARGE_FONT = pygame.font.SysFont("Arial", 50)
