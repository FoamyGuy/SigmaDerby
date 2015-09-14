from models import Track
from sim.GameSimulator import GameSimulator
from ui.ui_models import UIHorse
import pygame, sys
import time
from pygame.locals import *

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)




class UIGameSimulator(GameSimulator):

    windowSurface = None

    @staticmethod
    def init_screen():
        # set up pygame
        pygame.init()

        # set up the window
        UIGameSimulator.windowSurface = pygame.display.set_mode((500, 400), 0, 32)
        pygame.display.set_caption('Hello world!')

        # set up fonts
        basicFont = pygame.font.SysFont(None, 48)

        # set up the text
        text = basicFont.render('Hello world!', True, WHITE, BLUE)
        textRect = text.get_rect()
        textRect.centerx = UIGameSimulator.windowSurface.get_rect().centerx
        textRect.centery = UIGameSimulator.windowSurface.get_rect().centery

        # draw the white background onto the surface
        UIGameSimulator.windowSurface.fill(WHITE)


        # draw the window onto the screen
        pygame.display.update()



    @staticmethod
    def make_horses(weighted_powers):
        horses = []

        # Make 5 horses
        for h in range(1, 6):
            new_horse = UIHorse(40*h, BLUE, UIGameSimulator.windowSurface)                     # Create a horse
            new_horse.power = weighted_powers[h-1]  # Set its power
            new_horse.number = h                    # Set its number
            horses.append(new_horse)                  # Add to the track
        return horses

    @staticmethod
    def play(weighted_powers):
        t = Track() # Make a new Track.
        t.reset()

        new_horses = UIGameSimulator.make_horses(weighted_powers)

        # Add 5 horses to it
        for h in new_horses:
            t.add_horse(h)                  # Add to the track

        # Run the race and return results.
        return t.run_race()
