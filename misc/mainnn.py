import pygame, os, time, random
pygame.font.init()
pygame.init()

# Colours
white = (255, 255, 255)
black = (0, 0, 0)

# Constant Variables
FPS = 60
WIN_HEIGHT, WIN_WIDTH = 800, 800

#CHAR_HEIGHT, CHAR_WIDTH = 119, 81
velocity = round(600/FPS)
JUMP = 10
GRAVITY = 0.15

# Character Dimension Constants
CHAR_STATIONARY_DIMENSIONS = (55, 116)
CHAR_WALKING_DIMENSIONS = (53, 116)
CHAR_JUMP_DIMENSIONS = (56, 115)
CHAR_FALLING_DIMENSIONS = (79, 114)


# Misc Variables
momentum = 0
clock = pygame.time.Clock()
stationary = False
state = "stationary"
right = True
left = False


# Creating Window
WIN = pygame.display.set_mode((WIN_HEIGHT, WIN_WIDTH))
pygame.display.set_caption("Platformer")


# Importing Images
char_stationary_right_image = pygame.image.load(os.path.join("Assets", "char_stationary_right.png"))
char_walking_right_image = pygame.image.load(os.path.join("Assets", "char_walking_right.png"))
char_jump_right_image = pygame.image.load(os.path.join("Assets", "char_jump_right.png"))
char_falling_right_image = pygame.image.load(os.path.join("Assets", "char_falling_right.png"))

char_stationary_left_image = pygame.image.load(os.path.join("Assets", "char_stationary_left.png"))
char_walking_left_image = pygame.image.load(os.path.join("Assets", "char_walking_left.png"))
char_jump_left_image = pygame.image.load(os.path.join("Assets", "char_jump_left.png"))
char_falling_left_image = pygame.image.load(os.path.join("Assets", "char_falling_left.png"))



# Transform Images
char_stationary_right = pygame.transform.scale(char_stationary_right_image, CHAR_STATIONARY_DIMENSIONS)
char_walking_right = pygame.transform.scale(char_walking_right_image, CHAR_WALKING_DIMENSIONS)
char_jump_right = pygame.transform.scale(char_jump_right_image, CHAR_JUMP_DIMENSIONS)
char_falling_right = pygame.transform.scale(char_falling_right_image, CHAR_FALLING_DIMENSIONS)

char_stationary_left = pygame.transform.scale(char_stationary_left_image, CHAR_STATIONARY_DIMENSIONS)
char_walking_left = pygame.transform.scale(char_walking_left_image, CHAR_WALKING_DIMENSIONS)
char_jump_left = pygame.transform.scale(char_jump_left_image, CHAR_JUMP_DIMENSIONS)
char_falling_left = pygame.transform.scale(char_falling_left_image, CHAR_FALLING_DIMENSIONS)



class character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.Rect = pygame.Rect(0, 0, 1000, 1000)


player = character()


def display_window():
    global state
    if state == "stationary" and right:
        player.Rect.height = CHAR_STATIONARY_DIMENSIONS[1]
        player.Rect.width = CHAR_STATIONARY_DIMENSIONS[0]
        WIN.blit(char_stationary_right, (player.Rect.topleft))

    if state == "stationary" and left:
        player.Rect.height = CHAR_STATIONARY_DIMENSIONS[1]
        player.Rect.width = CHAR_STATIONARY_DIMENSIONS[0]
        WIN.blit(char_stationary_right, (player.Rect.topleft))

    if state == "walking" and right:
        player.Rect.height = CHAR_WALKING_DIMENSIONS[1]
        player.Rect.width = CHAR_WALKING_DIMENSIONS[0]
        WIN.blit(char_walking_right, (player.Rect.topleft))

    if state == "walking" and left:
        player.Rect.height = CHAR_WALKING_DIMENSIONS[1]
        player.Rect.width = CHAR_WALKING_DIMENSIONS[0]
        WIN.blit(char_walking_left, (player.Rect.topleft))

    if state == "jumping" and right:
        player.Rect.height = CHAR_JUMP_DIMENSIONS[1]
        player.Rect.width = CHAR_JUMP_DIMENSIONS[0]
        WIN.blit(char_jump_right, (player.Rect.topleft))

    if state == "jumping" and left:
        player.Rect.height = CHAR_JUMP_DIMENSIONS[1]
        player.Rect.width = CHAR_JUMP_DIMENSIONS[0]
        WIN.blit(char_jump_left, (player.Rect.topleft))

    if state == "falling" and right:
        player.Rect.height = CHAR_FALLING_DIMENSIONS[1]
        player.Rect.width = CHAR_FALLING_DIMENSIONS[0]
        WIN.blit(char_falling_right, (player.Rect.topleft))

    if state == "falling" and left:
        player.Rect.height = CHAR_FALLING_DIMENSIONS[1]
        player.Rect.width = CHAR_FALLING_DIMENSIONS[0]
        WIN.blit(char_falling_left, (player.Rect.topleft))



def handle_movement():
    global momentum, state, right, left

    
    
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        momentum = -JUMP
        state = "jumping"

    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.Rect.move_ip(0, velocity)

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.Rect.move_ip(-velocity, 0)
        state = "walking"
        right = False
        left = True

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.Rect.move_ip(velocity, 0)
        state = "walking"
        right = True
        left = False



    if player.Rect.top < 0:
        player.Rect.top = 0

    if player.Rect.bottom > WIN_HEIGHT:
        player.Rect.bottom = WIN_HEIGHT


    if player.Rect.left < 0:
        player.Rect.left = 0

    if player.Rect.right > WIN_WIDTH:
        player.Rect.right = WIN_WIDTH


def gravity(gravity):
    global momentum, state, stationary
    if player.Rect.bottom < WIN_HEIGHT:
        momentum += gravity


    if player.Rect.bottom < WIN_HEIGHT and momentum >= 0:
        state = "falling" 

    if player.Rect.bottom > WIN_HEIGHT:
        momentum = 0

    

    player.Rect.move_ip(0, momentum)






def main():

    running = True
    while running:
        WIN.fill(white)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        global stationary, state

        if player.Rect.bottom == WIN_HEIGHT:
                
            stationary = True
        else:
            stationary = False
            
        if stationary:
            state = "stationary"

        
        gravity(GRAVITY)
        handle_movement()
        print(player.Rect.bottom)



        display_window()


        pygame.display.flip()



main()