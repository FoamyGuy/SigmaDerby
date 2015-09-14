import pygame, sys
import time
from pygame.locals import *
from ui.UIGameSimulator import UIGameSimulator

WHITE = (255, 255, 255)

UIGameSimulator.init_screen()
# run the game loop
while True:
    payouts = UIGameSimulator.generate_payouts()
    weights = UIGameSimulator.get_weighted_powers(payouts)
    results = UIGameSimulator.play(weights)

    print(results)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.time.delay(1000)


    UIGameSimulator.windowSurface.fill(WHITE)
    pygame.display.update()
