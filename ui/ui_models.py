from models import Horse, Track
import pygame
from colors import *
import time


class UIHorse(Horse):
    def __init__(self, y_pos, color, windowSurface):
        self.y_pos = y_pos
        self.color = color
        self.windowSurface = windowSurface
        pygame.draw.circle(windowSurface, color, (self.get_screen_pos(), self.y_pos), 16, 0)

        pygame.display.update()

    def get_screen_pos(self):
        if self.position == 0:
            return 0
        else:
            return int(self.position * self.windowSurface.get_width() / Track.FINISH_POSITION)

    def update_ui(self, windowSurface, color):
        pygame.draw.circle(windowSurface, color, (self.get_screen_pos(), self.y_pos), 16, 0)
        pygame.display.update()

    def erase_self(self, windowSurface):
        pygame.draw.circle(windowSurface, WHITE, (self.get_screen_pos(), self.y_pos), 16, 0)
        pygame.display.update()

    def step(self):
        self.erase_self(self.windowSurface)
        super(UIHorse, self).step()
        self.update_ui(self.windowSurface, self.color)
        pygame.time.delay(5)

