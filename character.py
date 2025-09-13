import pygame, time, os
from bullet import Bullet
from main import *
# states--
# cooldown---
# dash---
# movement - figure out suvat
# boundaries---
# shooting--

# Character Class
class character(pygame.sprite.Sprite):
    def __init__(self, win_height, win_width, fps):
        super().__init__()
        self.image = None
        self.init_images()
        self.rect = self.image.get_rect()

        # Variables for movement and states
        self.win_width = win_width
        self.player_offset = (win_width//2) - (self.rect.width//2)
        self.camera_offset = pygame.math.Vector2(self.player_offset, 0)
        self.fps = fps
        self.direction = 1 # 1: right, -1: left
        self.ground_y = win_height
        self.gravity = 0.15
        self.friction = -0.1
        self.jump_const = 15
        self.dash_const = 25
        self.vel_const = 0.3
        self.momentum = 0
        self.state = "stationary"
        self.on_ground = False
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.velocity = pygame.math.Vector2(0, 0)
        self.maxvelocity = pygame.math.Vector2(5, 10)
        self.dash_cooldown = self.fps//2
        self.last_dash = -self.dash_cooldown # character can dash at start of game
        self.air_dash = 0
        self.on_ground = True
        self.bullet_vel = 20
        self.bullet_height = 5
        self.bullet_width = 10


    def update(self, player_bullets, display):
        self.handle_states()
        self.handle_movement()
        self.boundary_restrictions()
        self.handle_shooting(player_bullets)



    def init_images(self, *images):
        # Loading right facing images
        self.char_stationary_right = pygame.image.load(os.path.join("Assets", "char_stationary_right.png"))
        self.char_walking_right = pygame.image.load(os.path.join("Assets", "char_walking_right.png"))
        self.char_jump_right = pygame.image.load(os.path.join("Assets", "char_jump_right.png"))
        self.char_falling_right = pygame.image.load(os.path.join("Assets", "char_falling_right.png"))

        # Flipping images to be left facing 
        self.char_stationary_left = pygame.transform.flip(self.char_stationary_right, True, False)
        self.char_walking_left = pygame.transform.flip(self.char_walking_right, True, False)
        self.char_jump_left = pygame.transform.flip(self.char_jump_right, True, False)
        self.char_falling_left = pygame.transform.flip(self.char_falling_right, True, False)

        self.char_images = {"stationary" : {"right" : self.char_stationary_right, "left": self.char_stationary_left}, "walking" : {"right" : self.char_walking_right, "left": self.char_walking_left}, "jumping" : {"right" : self.char_jump_right, "left": self.char_jump_left}, "falling" : {"right" : self.char_falling_right, "left": self.char_falling_left}, "dashing" : {"right" : self.char_walking_right, "left": self.char_walking_left}}

        self.image = self.char_stationary_right


    def handle_states(self):
        if self.velocity.x == 0 and self.on_ground:
            self.state = "stationary"
        if not self.on_ground and self.velocity.y >= 0:
            self.state = "falling"

        self.image = self.char_images[self.state][self.direction]
        self.rect = self.image.get_rect()


    def handle_shooting(self, player_bullets):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if (now - self.last_dash) >= self.dash_cooldown:
                bullet = Bullet(self.bullet_width, self.bullet_height, self.bullet_vel, self.direction, (self.rect.x + self.rect.width//2 + self.player_offset, self.rect.y + self.rect.height//2))
                player_bullets.add(bullet)



    def handle_movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.acceleration.x += self.vel_const
            self.direction = "right"
            self.state = "walking"
        if keys[pygame.K_a]:
            self.acceleration.x -= self.vel_const
            self.state = "walking"
            self.direction = "left"
        if keys[pygame.K_UP]:
            self.jump()
        if keys[pygame.K_LSHIFT]:
            self.dash()
        
        self.acceleration.x += self.velocity.x * self.friction

        if self.velocity.x >= self.maxvelocity.x:
            self.velocity.x += self.acceleration.x

        if self.rect.bottom == self.ground_y:
            self.velocity.y = 0
            self.on_ground = True
            self.air_dash = 0
        else:
            self.velocity.y += self.acceleration.y
            if self.maxvelocity.y > self.maxvelocity.y:
                self.maxvelocity.y = self.maxvelocity.y
        
        self.camera_offset.x += self.velocity.x
        self.camera_offset.y += self.velocity.y




    def jump(self):
        if self.on_ground:
            self.state = "jumping"
            self.velocity.y -= self.jump_const
            self.on_ground = False

        
    
    def dash(self):
        now = pygame.time.get_ticks()
        if (now - self.last_dash) >= self.dash_cooldown:
            if (self.on_ground == False and self.air_dash == 0) or self.on_ground == True:
                self.acceleration.x += self.dash_const * self.direction
                self.last_dash = now
                if self.on_ground == False:
                    self.air_dash += 1



    def boundary_restrictions(self):
        if self.rect.bottom > self.ground_y:
            self.rect.bottom = self.ground_y


        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > self.win_width:
            self.rect.right = self.win_width





