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
WIN_HEIGHT, WIN_WIDTH = 800, 800
CHAR_DIMENSIONS = (55, 116)
GRAVITY = 0.15
JUMP = 15
VELOCITY = 10

# Misc Variables
clock = pygame.time.Clock()
momentum = 0


# Creating Window
WIN = pygame.display.set_mode((WIN_HEIGHT, WIN_WIDTH))
pygame.display.set_caption("Platformer")

# Importing Images
char_image = pygame.image.load(os.path.join("Assets", "char_stationary_right.png"))

# Transforming Images
char = pygame.transform.scale(char_image, CHAR_DIMENSIONS)



# Sprite Class for Player
class character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.Rect = pygame.Rect(0, 0, 1000, 1000)

player = character() # instantiation statement for player


# function to create window to be displayed in game loop
def display_window():
    player.Rect.height = CHAR_DIMENSIONS[1]
    player.Rect.width = CHAR_DIMENSIONS[0]
    WIN.blit(char, (player.Rect.topleft))


# function to handle player's movement
def handle_movement():
    global momentum, state, right, left

    
    
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        momentum = -JUMP
        state = "jumping"



    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.Rect.move_ip(-VELOCITY, 0)
        state = "walking"
        right = False
        left = True

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.Rect.move_ip(VELOCITY, 0)
        state = "walking"
        right = True
        left = False



def gravity():
    global momentum
    if player.Rect.bottom < WIN_HEIGHT:
        momentum += GRAVITY

    elif player.Rect.bottom > WIN_HEIGHT:
        momentum = 0


    player.Rect.move_ip(0, momentum) ###########


    if player.Rect.bottom >= WIN_HEIGHT:
        player.Rect.bottom = WIN_HEIGHT



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


        gravity()
        display_window()
        

        pygame.display.flip() # Updates full display surface to screen



main()

