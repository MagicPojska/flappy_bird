import pygame, sys, random

def move_floor():                               #function for moving the base
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))    #(we added another image to the right so it can loop)

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))                #Creating bottom pipe with midtop
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 300))          #Creating top pipe with midbottop and moving it up a bit so we can have space between two pipes
    return bottom_pipe, top_pipe

def move_pipes(pipes):      #This function takes all the pipe rectangles and moves them to the left 
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes            #We return a new list of pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:                 #We do this for the bottom pipes if they extend bellow 1024 pixels
            screen.blit(pipe_surface,pipe)
        else:                                   #And here we flip the pipe if its top pipe so we it can be placed nicely
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)    
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):         #Here we check for collisions 
    for pipe in pipes:              #We check if bird is coliding with every pipe(we need for loop because a new pipe is generated every 1.2 seconds)
        if bird_rect.colliderect(pipe):
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:    #And here we will return false if we hit top or bottom
        return False
    return True

pygame.init()
screen = pygame.display.set_mode((576,1024))    #setting the window size
clock = pygame.time.Clock()

# Game variables
gravity = 0.25              #We made a new variable gravity so we can put it on every frame of the bird_movement
bird_movement = 0
game_active = True

bg_surface = pygame.image.load('assets/background-day.png').convert()   #importing a bacground image (convert helps run the game faster)
bg_surface = pygame.transform.scale2x(bg_surface)                       #scaling it 2x so it fits the screen

floor_surface = pygame.image.load('assets/base.png').convert()          #importing base of the backgrount because it moves to the left
floor_surface = pygame.transform.scale2x(floor_surface)  
floor_x_pos = 0                                                         #new variable for position so we can make it move a bit 

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512))             #We are making a rectange around the image so we can later use it for colision(center of rectangle is at 100,512)

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()     #Adding pipes on the surface but without rectangles because we need a rectangle for each new pipe on the screen
pipe_surface = pygame.transform.scale2x(pipe_surface)  
pipe_list = []
SPAWNPIPE = pygame.USEREVENT                                            #Adding an event that happens every 1200miliseconds (that means the pipe will apper on the screen from right every 1.2sec)
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

#Making a screen to play on and our game loop:
while True:     #we need a loopt so the game wont close after one run
    for event in pygame.event.get():    #for loopt that checks for pressed keys and does what we tell it to
        if event.type == pygame.QUIT:   #this allows us to click X button to close the window(without it we would need to shut it down with task manager)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 12
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
        if event.type == SPAWNPIPE:     #This event will create a new pipe and store it in the pipe_list
            pipe_list.extend(create_pipe())

    #this all repeats every frame so if we increment a position of an asset for 1 it will move every time loops plays again (floor_x_pos += 1 as an example and the base will move to the right)
    screen.blit(bg_surface, (0,0))  #positioning assets on the screen

    if game_active:     #While game is true we will load this part of assets
        #Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface, bird_rect)
        game_active = check_collision(pipe_list)        #If we hit into something function will return False and the game wont load the assets for the bird and the pipes

        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    #Floor
    floor_x_pos -= 1
    move_floor()
    if floor_x_pos <= -576:         #if the images go too far to the left we reset the position so we give the illusion that it is infinite
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)

