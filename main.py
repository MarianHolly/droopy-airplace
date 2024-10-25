import pygame, sys, time 
from settings import *

class Bird_Game:
    def __init__(self):
        # setup
        pygame.init() # initialize pygame
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEAIGHT)) # set the screen size
        pygame.display.set_caption('Flappy Bird') # set the window title
        self.clock = pygame.time.Clock() # create a clock object

        # sprite groups
        self.all_stripes = pygame.sprite.Group() # create a sprite group
        self.colliion_stripes = pygame.sprite.Group() # create a sprite group

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # game logic
            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)

if __name__ == '__main__':
    game = Bird_Game()
    game.run()