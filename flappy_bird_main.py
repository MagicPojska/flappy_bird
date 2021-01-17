import pygame
import sys
import random


def move_floor():  # function for moving the base
    screen.blit(floor_surface, (floor_x_pos, 900))
    # (we added another image to the right so it can loop)
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    # Creating bottom pipe with midtop
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    # Creating top pipe with midbottop and moving it up a bit so we can have space between two pipes
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):  # This function takes all the pipe rectangles and moves them to the left
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes  # We return a new list of pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:  # We do this for the bottom pipes if they extend bellow 1024 pixels
            screen.blit(pipe_surface, pipe)
        else:  # And here we flip the pipe if its top pipe so we it can be placed nicely
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):  # Here we check for collisions
    # We check if bird is coliding with every pipe(we need for loop because a new pipe is generated every 1.2 seconds)
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True  # After dying it can_score resets to True so we cans core the first point
            return False

    # And here we will return false if we hit top or bottom
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        can_score = True
        return False
    return True


def rotate_bird(bird):  # function for rotating bird using rotozoom
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():  # this function is for new assets of bird to spawn where the last one was
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(
            str(int(score)), False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(
            f'Score: {int(score)}', False, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f'High score: {int(high_score)}', False, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))  # setting the window size
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# Game variables
gravity = 0.25  # We made a new variable gravity so we can put it on every frame of the bird_movement
bird_movement = 0
game_active = True
score = 0  # Current score
high_score = 0  # High score
can_score = True


# importing a bacground image (convert helps run the game faster)
bg_surface = pygame.image.load('assets/background-day.png').convert()
# scaling it 2x so it fits the screen
bg_surface = pygame.transform.scale2x(bg_surface)

# importing base of the backgrount because it moves to the left
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0  # new variable for position so we can make it move a bit

# Here we removed old bird and added new assets so we can animate it
bird_downflap = pygame.transform.scale2x(pygame.image.load(
    'assets/bluebird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load(
    'assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load(
    'assets/bluebird-upflap.png').convert_alpha())
# We will animate it using a list that will by order display 3 states of bird
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))


BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


# Adding pipes on the surface but without rectangles because we need a rectangle for each new pipe on the screen
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# Adding an event that happens every 1200miliseconds (that means the pipe will apper on the screen from right every 1.2sec)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(
    pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('audio/wing.wav')  # Importing sounds
death_sound = pygame.mixer.Sound('audio/hit.wav')
score_sound = pygame.mixer.Sound('audio/point.wav')
score_sound_countdown = 100

# Making a screen to play on and our game loop:
while True:  # we need a loopt so the game wont close after one run
    for event in pygame.event.get():  # for loopt that checks for pressed keys and does what we tell it to
        # this allows us to click X button to close the window(without it we would need to shut it down with task manager)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:  # This event will create a new pipe and store it in the pipe_list
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()
    # this all repeats every frame so if we increment a position of an asset for 1 it will move every time loops plays again (floor_x_pos += 1 as an example and the base will move to the right)
    screen.blit(bg_surface, (0, 0))  # positioning assets on the screen

    if game_active:  # While game is true we will load this part of assets
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        # If we hit into something function will return False and the game wont load the assets for the bird and the pipes
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        pipe_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    move_floor()
    if floor_x_pos <= -576:  # if the images go too far to the left we reset the position so we give the illusion that it is infinite
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
