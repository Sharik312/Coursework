import pygame, os, time
from tiles import *
pygame.font.init()
pygame.init()


# Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


# Constant Variables
FPS = 60
WIN_HEIGHT, WIN_WIDTH = 900, 1320
GRAVITY = 0.15
JUMP = 8
VELOCITY = 10
DASH = 250

# Character Dimension Constants
CHAR_STATIONARY_DIMENSIONS = (55, 116)
CHAR_WALKING_DIMENSIONS = (53, 116)
CHAR_JUMP_DIMENSIONS = (56, 115)
CHAR_FALLING_DIMENSIONS = (79, 114)


# Misc Variables
clock = pygame.time.Clock()
momentum = 0
state = "stationary"
char_image = ""
direction = "right"


# Camera Variable
camera_offset_x = 0
camera_offset_y = 0
ground_y  = WIN_HEIGHT


# Creating Window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Platformer")


# Dash
dash_cooldown = 0
dash_counter = 0
dashing = False
DASH_COOLDOWN = 0.5


# Bullets
BULLET_VEL = 20
BULLET_HEIGHT = 5
BULLET_WIDTH = 10
BULLET_COOLDOWN = 0.5
bullet_cooldown = 0


# Enemies
ENEMY_HEALTH = 100
ENEMY_ATTACK = 50
ENEMY_ATTACK_COOLDOWN = 2
ENEMY_SIZE = 20


# Importing Images
house = pygame.image.load(os.path.join("Assets", 'example_bg.png')).convert()
char_stationary_right_image = pygame.image.load(os.path.join("Assets", "char_stationary_right.png"))
char_walking_right_image = pygame.image.load(os.path.join("Assets", "char_walking_right.png"))
char_jump_right_image = pygame.image.load(os.path.join("Assets", "char_jump_right.png"))
char_falling_right_image = pygame.image.load(os.path.join("Assets", "char_falling_right.png"))

char_stationary_left_image = pygame.image.load(os.path.join("Assets", "char_stationary_left.png"))
char_walking_left_image = pygame.image.load(os.path.join("Assets", "char_walking_left.png"))
char_jump_left_image = pygame.image.load(os.path.join("Assets", "char_jump_left.png"))
char_falling_left_image = pygame.image.load(os.path.join("Assets", "char_falling_left.png"))

# Transforming Images
char_stationary_right = pygame.transform.scale(char_stationary_right_image, CHAR_STATIONARY_DIMENSIONS)
char_walking_right = pygame.transform.scale(char_walking_right_image, CHAR_WALKING_DIMENSIONS)
char_jump_right = pygame.transform.scale(char_jump_right_image, CHAR_JUMP_DIMENSIONS)
char_falling_right = pygame.transform.scale(char_falling_right_image, CHAR_FALLING_DIMENSIONS)

char_stationary_left = pygame.transform.scale(char_stationary_left_image, CHAR_STATIONARY_DIMENSIONS)
char_walking_left = pygame.transform.scale(char_walking_left_image, CHAR_WALKING_DIMENSIONS)
char_jump_left = pygame.transform.scale(char_jump_left_image, CHAR_JUMP_DIMENSIONS)
char_falling_left = pygame.transform.scale(char_falling_left_image, CHAR_FALLING_DIMENSIONS)

# Tilemap
map = TileMap("example_level.csv", WIN)




# Dictionaries to hold character dimensions and images
char_dimensions = {"stationary" : CHAR_STATIONARY_DIMENSIONS, "jumping" : CHAR_JUMP_DIMENSIONS, "walking" : CHAR_WALKING_DIMENSIONS, "falling" : CHAR_FALLING_DIMENSIONS, "dashing" : CHAR_WALKING_DIMENSIONS}
char_images = {"stationary" : {"right" : char_stationary_right, "left": char_stationary_left}, "walking" : {"right" : char_walking_right, "left": char_walking_left}, "jumping" : {"right" : char_jump_right, "left": char_jump_left}, "falling" : {"right" : char_falling_right, "left": char_falling_left}, "dashing" : {"right" : char_walking_right, "left": char_walking_left}}


# Sprite Class for Player
class character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Rect = pygame.Rect(0, 0, 0, 0)

player = character() # instantiation statement for player


class Bullet(pygame.sprite.Sprite):
    def __init__(self, width, height, direction, pos):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(red)
        self.rect = self.image.get_rect(center=pos)

        if direction == "right":
            self.direction = 1
        else:
            self.direction = -1


    def update(self):
        if self.rect.x < 0 or self.rect.x > WIN_WIDTH or self.rect.y < 0 or self.rect.y > WIN_HEIGHT:
            self.kill()

        self.rect.x += BULLET_VEL*self.direction


class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, attack, cooldown_time, size, pos):
        super().__init__()
        self.health = health
        self.attack = attack
        self.cooldown_time = cooldown_time*FPS
        self.cooldown = cooldown_time*FPS
        self.size = size
        self.pos = pos

        self.image = pygame.Surface((size, size))
        self.image.fill(red)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        global camera_offset_x, camera_offset_y
        self.rect.x = -camera_offset_x + self.pos[0]
        self.rect.y = -camera_offset_y + self.pos[1]

        self.cooldown -= 1

        if self.cooldown == 0:
            self.cooldown = self.cooldown_time

            bulletr = Bullet(BULLET_WIDTH, BULLET_HEIGHT, "right", (self.rect.x, self.rect.y + self.rect.height//2))
            bulletl = Bullet(BULLET_WIDTH, BULLET_HEIGHT, "left", (self.rect.x, self.rect.y + self.rect.height//2))
            enemy_bullets.add(bulletr)
            enemy_bullets.add(bulletl)



        

enemies = pygame.sprite.Group()      
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()


enemy1 = Enemy(ENEMY_HEALTH, ENEMY_ATTACK, ENEMY_ATTACK_COOLDOWN, ENEMY_SIZE, (50, ground_y - 20))
enemies.add(enemy1)




# function to create window to be displayed in game loop
def display_window():
    global char_image, player_offset, camera_offset_y, camera_offset_x
    player_offset = (WIN_WIDTH//2) - (player.Rect.width//2)

    player.Rect.height = CHAR_STATIONARY_DIMENSIONS[1]
    player.Rect.width = CHAR_STATIONARY_DIMENSIONS[0]


    map.draw_map(WIN, camera_offset_x, camera_offset_y)
    WIN.blit(char_image, (player.Rect.topleft[0] + player_offset, player.Rect.topleft[1]))
    player_bullets.draw(WIN)
    enemies.draw(WIN)
    enemy_bullets.draw(WIN)
    

# Function to check if character is stationary
def is_stationary():
    keys = pygame.key.get_pressed()
    return (player.Rect.bottom >= ground_y) and (not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_a])) and ((not keys[pygame.K_UP] or not keys[pygame.K_w]) and state == "falling")  and not dashing


# Function to handle character states
def handle_states():
    global state, direction, char_image, char_images, char_dimensions
    
    if is_stationary():
        state = "stationary"

    player.Rect.width = char_dimensions[state][0]
    player.Rect.height = char_dimensions[state][1]

    char_image = char_images[state][direction]


# Function to handle cooldowns
def cooldowns():
    global dash_cooldown, dash_counter, camera_offset_x, camera_offset_y, bullet_cooldown
    if dash_cooldown != 0:
        dash_cooldown -= 1

    if player.Rect.bottom >= ground_y:
        dash_counter = 0

    if bullet_cooldown != 0:
        bullet_cooldown -= 1
    

# function to handle player's movement
def handle_movement():
    global momentum, state, direction, dash_cooldown, dash_counter, dashing, counter, camera_offset_x, camera_offset_y, bullet_cooldown

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        if state != "jumping" and state != "falling" and state != "dashing":
            state = "jumping"
            momentum -= JUMP
            
    
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not dashing:
        camera_offset_x += VELOCITY
        direction = "right"
        
        if player.Rect.bottom >= ground_y:
            state = "walking"
        
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not dashing:
        camera_offset_x -= VELOCITY
        direction = "left"
        
        if player.Rect.bottom >= ground_y:
            state = "walking"

    if keys[pygame.K_SPACE] and bullet_cooldown == 0:
        bullet = Bullet(BULLET_WIDTH, BULLET_HEIGHT, direction, (player.Rect.x + player.Rect.width//2 + player_offset, player.Rect.y + player.Rect.height//2))
        player_bullets.add(bullet)

        bullet_cooldown = int(FPS*BULLET_COOLDOWN)

    if keys[pygame.K_LSHIFT] and dash_cooldown == 0 and dash_counter == 0:
        state = "dashing"
        dash_cooldown = int(FPS*DASH_COOLDOWN)
        dashing = True
        counter = 0

        if player.Rect.bottom < ground_y:
            dash_counter += 1

        
    if dashing:
        if direction == "right":
            camera_offset_x += (DASH//(FPS//6))
        else:
            camera_offset_x -= (DASH//(FPS//6))
        counter += 1
        if counter >= FPS//6:
            dashing = False


    

# Function to stop character moving out of screen
def boundary_restrictions():
    global camera_offset_y


    if player.Rect.collidedict()

    if player.Rect.top < 0:
        camera_offset_y = player.Rect.top
    else:
        camera_offset_y = 0

    if player.Rect.bottom > ground_y:
        player.Rect.bottom = ground_y


    if player.Rect.left < 0:
        player.Rect.left = 0

    if player.Rect.right > WIN_WIDTH:
        player.Rect.right = WIN_WIDTH


# Function to make gravity affect the player
def gravity():
    global momentum, state
    if player.Rect.bottom < ground_y:
        momentum += GRAVITY

    if player.Rect.bottom < ground_y and momentum >= 0:
        state = "falling"
    
    if player.Rect.bottom < ground_y and momentum < 0 and state != "dashing":
        state = "jumping"
    
    elif player.Rect.bottom >= ground_y:
        momentum = 0



    player.Rect.move_ip(0, momentum)


# Main Function
def main():
    running = True
    # while loop to run window
    while running:
        WIN.fill(white)
        clock.tick(FPS)

        for event in pygame.event.get(): # Checking for events
            # Closes window if exit window button is pressed
            if event.type == pygame.QUIT:
                running = False


        handle_movement()
        boundary_restrictions()
        cooldowns()
        handle_states()
        gravity()
        enemies.update()
        enemy_bullets.update()
        player_bullets.update()
        #print(player.Rect.top, camera_offset_y)
        

        display_window()

        pygame.display.update() # Updates full display surface to screen



main()