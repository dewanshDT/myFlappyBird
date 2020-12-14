import sys, random, time
import pygame

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
pygame.init()
screen = pygame.display.set_mode((288, 512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 20)

# Game variables
gravity = 0.12
bird_movement = 0

bg_surface = pygame.image.load('img_assets/background-day.png').convert()
floor_surface = pygame.image.load('img_assets/base.png').convert()
floorPos = 0

bird_upflap = pygame.image.load('img_assets/yellowbird-upflap.png').convert_alpha()
bird_midflap = pygame.image.load('img_assets/yellowbird-midflap.png').convert_alpha()
bird_down = pygame.image.load('img_assets/yellowbird-downflap.png').convert_alpha()
bird_frames = [bird_upflap, bird_midflap, bird_down]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, 256))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('img_assets/pipe-green.png').convert()
pipe_list = []

SPAWNTIME = pygame.USEREVENT
pygame.time.set_timer(SPAWNTIME, 1000)

pipe_height = [189, 269, 378, 400, 200, 300]

game_active = True

score = -1
highscore = 0

message_surface = pygame.image.load('img_assets/message.png').convert_alpha()
message_rect = message_surface.get_rect(center = (144, 256))

gameover_surface = pygame.image.load('img_assets/gameover.png').convert_alpha()
gameover_rect = gameover_surface.get_rect(center = (144, 256))

flap_sound = pygame.mixer.Sound('audio_assets/sfx_wing.wav')
death_sound = pygame.mixer.Sound('audio_assets/sfx_hit.wav')
score_sound = pygame.mixer.Sound('audio_assets/sfx_point.wav')

# defining functions
def drawFloor():
        screen.blit(floor_surface, (floorPos, 450))
        screen.blit(floor_surface, (floorPos+288, 450))

def createPipe():
    random_pipe_height = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (400, random_pipe_height - 150))
    bottom_pipe = pipe_surface.get_rect(midtop = (400, random_pipe_height))
    return bottom_pipe, top_pipe

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 450:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def checkCollision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            screen.blit(gameover_surface, gameover_rect)
            return False

    if bird_rect.bottom >= 450 or bird_rect.top <= -50:
        death_sound.play()
        screen.blit(gameover_surface, gameover_rect)
        return False

    return True

def rotateBird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def birdAnimation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
    return new_bird, new_bird_rect

def displayScore(score):
    if score <= 0:
        score_surface = game_font.render(str(int(0)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144, 50))
        screen.blit(score_surface, score_rect)

def highScore(num):
    if num < highscore:
        return highscore
    else:
        return num


while True:
    #args
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 4
                flap_sound.play()
            elif event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear() 
                bird_rect.center = (50, 256)
                bird_movement = 0
                score = -1
        if event.type == SPAWNTIME:
            pipe_list.extend(createPipe())
            if game_active:
                 score += 1
                 if score > 0:
                    score_sound.play()
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1 
            else:
                bird_index = 0

            bird_surface, bird_rect = birdAnimation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        #bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotateBird(bird_surface)
        screen.blit(rotated_bird, bird_rect) 
        game_active = checkCollision(pipe_list)
        # if game_active ==  False:
        #     screen.blit(gameover_surface, gameover_rect)
        #     time.sleep(1)

        #pipes;
        pipe_list = movePipes(pipe_list)
        drawPipes(pipe_list)
        displayScore(score)
    else:
        time.sleep(1)
        screen.blit(message_surface, message_rect)
        highscore = highScore(score)
        displayScore(highscore)

    #floor
    drawFloor()
    floorPos -= 1
    if floorPos <= -288:
        floorPos = 0

    pygame.display.update()
    clock.tick(120)