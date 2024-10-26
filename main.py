import pygame, sys, time 
from settings import *
from sprites import DA, Ground

class Droppy_Airplane:
    def __init__(self):
        # setup
        pygame.init() # initialize pygame
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEAIGHT)) # set the screen size
        pygame.display.set_caption('Droppy Airplane') # set the window title
        self.clock = pygame.time.Clock() # create a clock object

        # sprite groups
        self.all_stripes = pygame.sprite.Group() # create a sprite group
        self.collision_sprites = pygame.sprite.Group() # create a sprite group

        # scale factor
        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEAIGHT / bg_height

        # sprites setup
        DA(self.all_stripes,self.scale_factor)
        Ground(self.all_stripes,self.scale_factor)
        
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
            self.screen.fill('black')
            self.all_stripes.update(dt)
            self.all_stripes.draw(self.screen)

            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)

if __name__ == '__main__':
    game = Droppy_Airplane()
    game.run()