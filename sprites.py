import pygame
from settings import *
from random import choice, randint

class DA(pygame.sprite.Sprite):
    """Background class that creates an infinitely scrolling background effect"""
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        # load and scale the background image
        bg_image = pygame.image.load('graphics/environment/background.png').convert()

        # calculate the full size of the background
        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image,(full_width,full_height))

        # create a surface that is twice the size of the background and place two copies side by side
        # this allows for smooth scrolling effect
        self.image = pygame.Surface((full_width * 2,full_height))
        self.image.blit(full_sized_image,(0,0))
        self.image.blit(full_sized_image,(full_width,0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self,dt):
        # move the background to the left to create scrolling effect
        self.pos.x -= 300 * dt
        # reset position when the first image is completely off screen
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    """Ground class that creates the scrolling ground surface"""
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'

        # load and scale the ground image
        ground_surface = pygame.image.load('graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground_surface,pygame.math.Vector2(ground_surface.get_size())* scale_factor)

        # position the ground at the bottom of the window
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.bottomleft)

        # create a mask for pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self,dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    """Player-controlled airplane class"""
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # load and scale airplane animation frames
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        # position the plane on the screen
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH/20, WINDOW_HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # physics variables
        self.gravity = 330 # gravity force pulling plane down
        self.direction = 0 # current vertical movement direction

        # collision mask for pixel-perfect collisions
        self.mask = pygame.mask.from_surface(self.image)
 
        # load jump sound effect
        self.jump_sound = pygame.mixer.Sound('sounds/jump.wav')
        self.jump_sound.set_volume(0.3)
    
    def import_frames(self,scale_factor):
        # load all animation frames for the plane
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(f'graphics/plane/red{i}.png').convert_alpha()
            scaled_surf = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
            self.frames.append(scaled_surf)

    def apply_gravity(self,dt):
        # apply gravity force to the plane's vertical movement
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        # make the plane jump (move upward)
        self.jump_sound.play()
        self.direction = -400 # negative value means upward movement

    def animate(self,dt):
        # cycle through the animation frames
        self.frame_index += 14 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        # rotate the plane based on its movement direction
        rotated_plane = pygame.transform.rotate(self.image,-self.direction * 0.05)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        # update plane physics, animation, and rotation each frame
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    """Obstacle class for creating the pipes the plane must avoid"""
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        # randomly choose if obstacle appears from top or bottom
        orientation = choice(('up','down'))
        surf = pygame.image.load(f'./graphics/obstacles/{choice((0,1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size()) * scale_factor)
        
        # position obstacle just off screen to the right
        x = WINDOW_WIDTH + randint(40,100)

        # position obstacle based on orientation
        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10,50)
            self.rect = self.image.get_rect(midbottom = (x,y))
        else:
            y = randint(-50,-10)
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect = self.image.get_rect(midtop = (x,y))
        
        self.pos = pygame.math.Vector2(self.rect.topleft)

		# create collision mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        # move obstacle to the left and remove it when off screen
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
