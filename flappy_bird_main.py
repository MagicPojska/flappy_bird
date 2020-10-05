import pygame, sys



def move_floor():                               #function for moving the base
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


pygame.init()
screen = pygame.display.set_mode((576,1024))    #setting the window size
clock = pygame.time.Clock()

bg_surface = pygame.image.load('assets/background-day.png').convert()   #importing a bacground image (convert helps run the game faster)
bg_surface = pygame.transform.scale2x(bg_surface)                       #scaling it 2x so it fits the screen

floor_surface = pygame.image.load('assets/base.png').convert()          #importing base of the backgrount because it moves to the left
floor_surface = pygame.transform.scale2x(floor_surface)  
floor_x_pos = 0                                                         #new variable for position so we can make it move a bit 


#Making a screen to play on and a X as a quit button:
while True:     #we need a loopt so the game wont close after one run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #this allows us to click X button to close the window(without it we would need to shut it down with task manager)
            pygame.quit()
            sys.exit()

    #this all repeats every frame so if we increment a position of an asset for 1 it will move every time loops plays again (floor_x_pos += 1 as an example and the base will move to the right)
    screen.blit(bg_surface, (0,0))  #positioning assets on the screen

    floor_x_pos -= 1
    move_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0



    pygame.display.update()
    clock.tick(120)
