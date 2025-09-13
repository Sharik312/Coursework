import pygame, os, time, random
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
WIN_HEIGHT, WIN_WIDTH = 380, 500
GRAVITY = 0.15
JUMP = 5
VELOCITY = 10
DASH = 150

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
dash_cooldown = 0
dash_counter = 0
dashing = False


# Camera Variable
camera_offset = (0, 0)
ground_y  = 283



# Creating Window
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Platformer")


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

# Dictionaries to hold character dimensions and images
char_dimensions = {"stationary" : CHAR_STATIONARY_DIMENSIONS, "jumping" : CHAR_JUMP_DIMENSIONS, "walking" : CHAR_WALKING_DIMENSIONS, "falling" : CHAR_FALLING_DIMENSIONS, "dashing" : CHAR_WALKING_DIMENSIONS}
char_images = {"stationary" : {"right" : char_stationary_right, "left": char_stationary_left}, "walking" : {"right" : char_walking_right, "left": char_walking_left}, "jumping" : {"right" : char_jump_right, "left": char_jump_left}, "falling" : {"right" : char_falling_right, "left": char_falling_left}, "dashing" : {"right" : char_walking_right, "left": char_walking_left}}

# Sprite Class for Player
class character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.Rect = pygame.Rect(0, 0, 1000, 1000)

player = character() # instantiation statement for player


# function to create window to be displayed in game loop
def display_window():
    global char_image
    player.Rect.height = CHAR_STATIONARY_DIMENSIONS[1]
    player.Rect.width = CHAR_STATIONARY_DIMENSIONS[0]
    WIN.blit(house, (0, 0))
    WIN.blit(char_image, (player.Rect.topleft))


def is_stationary():
    keys = pygame.key.get_pressed()
    return (player.Rect.bottom >= ground_y) and (not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w])  and not dashing)


def handle_states():
    global state, direction, char_image, char_images, char_dimensions
    
    if is_stationary():
        state = "stationary"

    player.Rect.width = char_dimensions[state][0]
    player.Rect.height = char_dimensions[state][1]

    char_image = char_images[state][direction]


def cooldowns():
    global dash_cooldown, dash_counter
    if dash_cooldown != 0:
        dash_cooldown -= 1

    if player.Rect.bottom >= ground_y:
        dash_counter = 0

    

# function to handle player's movement
def handle_movement():
    global momentum, state, direction, dash_cooldown, dash_counter, dashing, counter

    keys = pygame.key.get_pressed()

    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        if state != "jumping" and state != "falling" and state != "dashing":
            state = "jumping"
            momentum -= JUMP
            
    
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not dashing:
        player.Rect.move_ip(VELOCITY, 0)
        direction = "right"
        
        if player.Rect.bottom >= WIN_HEIGHT:
            state = "walking"
        
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not dashing:
        player.Rect.move_ip(-VELOCITY, 0)
        direction = "left"
        
        if player.Rect.bottom >= WIN_HEIGHT:
            state = "walking"

    if keys[pygame.K_LSHIFT] and dash_cooldown == 0 and dash_counter == 0:
        state = "dashing"
        dash_cooldown = FPS//4
        dashing = True
        counter = 0

        if player.Rect.bottom < ground_y:
            dash_counter += 1

        
    if dashing:
        if direction == "right":
            player.Rect.move_ip((DASH//(FPS//6)), 0)
        else:
            player.Rect.move_ip((-DASH//(FPS//6)), 0)
        counter += 1
        if counter >= FPS//6:
            dashing = False

    

# Function to stop character moving out of screen
def boundary_restrictions():
    if player.Rect.top < 0:
        player.Rect.top = 0

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

    if player.Rect.bottom < ground_y and momentum >= 0 and state != "dashing":
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
        #print(player.Rect.height, player.Rect.width, player.Rect.right)
        print(state, dash_cooldown)
        
        display_window()
        
        pygame.display.flip() # Updates full display surface to screen



main()
