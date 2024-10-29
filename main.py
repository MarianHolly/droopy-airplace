import pygame, sys, time 
from settings import *
from sprites import DA, Ground, Plane, Obstacle

class Droppy_Airplane:
    def __init__(self):
        
        # setup
        pygame.init() # initialize pygame
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # set the screen size
        pygame.display.set_caption('Droppy Airplane') # set the window title
        self.clock = pygame.time.Clock() # create a clock object
        self.active = True

        # sprite groups
        self.all_stripes = pygame.sprite.Group() # create a sprite group
        self.collision_sprites = pygame.sprite.Group() # create a sprite group

        # scale factor
        bg_height = pygame.image.load('graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprites setup
        DA(self.all_stripes,self.scale_factor)
        Ground([self.all_stripes,self.collision_sprites],self.scale_factor)
        self.plane = Plane(self.all_stripes,self.scale_factor / 1.7)
        
        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # text
        self.font = pygame.font.Font('graphics/font/BD_Cartoon_Shout.ttf',30)
        self.score = 0
        self.start_offset = 0
 
        # menu
        self.menu_surf = pygame.image.load('graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2))
 
        # music 
        self.music = pygame.mixer.Sound('sounds/music.wav')
        self.music.play(loops = -1)

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask)\
        or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()
    
    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)
 
        score_surf = self.font.render(str(self.score),True,'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH / 2,y))
        self.screen.blit(score_surf,score_rect)

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_stripes,self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                    
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)
            
            # game logic
            self.screen.fill('black')
            self.all_stripes.update(dt)
            self.all_stripes.draw(self.screen)
            self.display_score()

            if self.active:
                self.collisions()
            else: 
                self.screen.blit(self.menu_surf,self.menu_rect)

            pygame.display.update()
            # self.clock.tick(FRAMES_PER_SECOND)

if __name__ == '__main__':
    game = Droppy_Airplane()
    game.run()