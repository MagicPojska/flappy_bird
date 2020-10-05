import pygame, sys



def move_floor():                               #function for moving the base
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))    #(we added another image to the right so it can loop)


pygame.init()
screen = pygame.display.set_mode((576,1024))    #setting the window size
clock = pygame.time.Clock()

# Game variables
gravity = 0.25              #We made a new variable gravity so we can put it on every frame of the bird_movement
bird_movement = 0

bg_surface = pygame.image.load('assets/background-day.png').convert()   #importing a bacground image (convert helps run the game faster)
bg_surface = pygame.transform.scale2x(bg_surface)                       #scaling it 2x so it fits the screen

floor_surface = pygame.image.load('assets/base.png').convert()          #importing base of the backgrount because it moves to the left
floor_surface = pygame.transform.scale2x(floor_surface)  
floor_x_pos = 0                                                         #new variable for position so we can make it move a bit 

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512))             #We are making a rectange around the image so we can later use it for colision(center of rectangle is at 100,512)



#Making a screen to play on and our game loop:
while True:     #we need a loopt so the game wont close after one run
    for event in pygame.event.get():    #for loopt that checks for pressed keys and does what we tell it to
        if event.type == pygame.QUIT:   #this allows us to click X button to close the window(without it we would need to shut it down with task manager)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 12

    #this all repeats every frame so if we increment a position of an asset for 1 it will move every time loops plays again (floor_x_pos += 1 as an example and the base will move to the right)
    screen.blit(bg_surface, (0,0))  #positioning assets on the screen

    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    floor_x_pos -= 1
    move_floor()
    if floor_x_pos <= -576:         #if the images go too far to the left we reset the position so we give the illusion that it is infinite
        floor_x_pos = 0


    pygame.display.update()
    clock.tick(120)

