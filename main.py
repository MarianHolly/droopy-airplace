import pygame, sys, time 
from settings import *
from sprites import DA, Ground, Plane, Obstacle

class Droppy_Airplane:
    """Main game class that handles game setup and main loop"""
    def __init__(self):
        
        # initialize Pygame and create the game window
        pygame.init() 
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Droppy Airplane')
        self.clock = pygame.time.Clock() 
        self.active = True # game state flag

        # create sprite groups for rendering and collision detection
        self.all_stripes = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # calculate scale factor based on background image
        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # create initial game objects
        DA(self.all_stripes,self.scale_factor) # background
        Ground([self.all_stripes,self.collision_sprites],self.scale_factor) # ground
        self.plane = Plane(self.all_stripes,self.scale_factor / 1.7) # player plane
        
        # set up obstacle spawn timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # set up score display
        self.font = pygame.font.Font('graphics/font/BD_Cartoon_Shout.ttf',30)
        self.score = 0
        self.start_offset = 0
 
        # load menu image
        self.menu_surf = pygame.image.load('graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))
 
        # load and start background music 
        self.music = pygame.mixer.Sound('sounds/music.wav')
        self.music.play(loops = -1)

    def collisions(self):
        """Check for collisions between plane and obstacles/ground"""
        if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
        or self.plane.rect.top <= 0:
            # if collision detected, remove obstacles and end game
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()
    
    def display_score(self):
        """Display the current score"""
        if self.active:
            # calculate score based on survival time
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            # position score on menu screen when game is over
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)
 
        score_surf = self.font.render(str(self.score),True,'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
        self.screen.blit(score_surf,score_rect)

    def run(self):
        """Main game loop"""
        last_time = time.time()
        while True:
            # calculate delta time for smooth movement
            dt = time.time() - last_time
            last_time = time.time()
            # handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump() # make plane jump when clicked
                    else:
                        # reset game when clicked on menu screen
                        self.plane = Plane(self.all_stripes,self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                    
                if event.type == self.obstacle_timer and self.active:
                    # spawn new obstacle when timer triggers
                    Obstacle([self.all_stripes,self.collision_sprites],self.scale_factor * 1.1)
            
            # update game state
            self.screen.fill('black')
            self.all_stripes.update(dt)
            self.all_stripes.draw(self.screen)
            self.display_score()

            if self.active:
                self.collisions() # check for collisions during active gameplay
            else: 
                self.screen.blit(self.menu_surf,self.menu_rect) # show menu when game is over

            # update the display
            pygame.display.update()

if __name__ == '__main__':
    game = Droppy_Airplane()
    game.run()