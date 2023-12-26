import pygame
import os
import cv2
import sys
import random

#initialize pygame
pygame.init()

TITTLE = "Bubble Buster"

WIDTH, HEIGHT = 1000, 600

BUTTON_WIDTH, BUTTON_HEIGHT = 120, 75

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

video = cv2.VideoCapture('start.mp4')

START_BUTTON = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 - 60, 220, 120)
START_BUTTON = START_BUTTON.inflate(-21, -21)

START_BUTTON_IMAGE = pygame.image.load('button.png')
START_BUTTON_IMAGE = pygame.transform.scale(START_BUTTON_IMAGE, (220, 120))

FONT = pygame.font.SysFont('Comic Sans MS', 30)

TEXT_SURFACE = FONT.render('Start', True, (255, 255, 255))

CHARACTER_VEL = 5
BALLOON_VEL = 7
BALLOON_DIMENSION = (50, 50)
CHARACTER_WIDTH, CHARACTER_HEIGHT = 60, 90

CHARACTER_IMAGE1 = pygame.image.load('character_assets/c1.png')
CHARACTER_IMAGE2 = pygame.image.load('character_assets/c2.png')
CHARACTER_IMAGE3 = pygame.image.load('character_assets/c3.png')
CHARACTER_IMAGE4 = pygame.image.load('character_assets/c4.png')
CHARACTER_IMAGE5 = pygame.image.load('character_assets/c5.png')

BALLOON_IMAGE1 = pygame.image.load("balloon1.png")
BALLOON_IMAGE2 = pygame.image.load("balloon2.png")
BALLOON_IMAGE3 = pygame.image.load("balloon3.png")

list_of_balloon_image = [BALLOON_IMAGE1, BALLOON_IMAGE2, BALLOON_IMAGE3]
list_of_character_image = [CHARACTER_IMAGE1, CHARACTER_IMAGE2, CHARACTER_IMAGE3, CHARACTER_IMAGE4, CHARACTER_IMAGE5]

IMAGE_POSITION = 0

# initializing main background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("main_background.png")), (WIDTH, HEIGHT))

def flip_image(image):
    return pygame.transform.flip(image, True, False)

def is_video_ended():
  success, video_image = video.read()
  if success:
    # Convert the image from BGR to RGB format
    video_image = cv2.cvtColor(video_image, cv2.COLOR_BGR2RGB)

    # Create a pygame surface from the NumPy array
    video_surface = pygame.surfarray.make_surface(video_image)
    flipped = pygame.transform.flip(video_surface, True, False)

    WIN.blit(pygame.transform.rotate(flipped, 90), (0,0))
    return False
  else:
    return True

def ctr_left_clicked(CHARACTER, key_pressed, IMAGE_POSITION):
  if key_pressed[pygame.K_LEFT] and (CHARACTER.x - CHARACTER_VEL) > 0:
      CHARACTER.x -= CHARACTER_VEL
      IMAGE_POSITION = (IMAGE_POSITION - 1) % len(list_of_character_image)
      WIN.blit(flip_image(list_of_character_image[IMAGE_POSITION]), (CHARACTER.x, CHARACTER.y))
  return IMAGE_POSITION

def ctr_right_clicked(CHARACTER, key_pressed, IMAGE_POSITION):
  if key_pressed[pygame.K_RIGHT] and (CHARACTER.x + CHARACTER_VEL) < WIDTH:
    CHARACTER.x += CHARACTER_VEL
    IMAGE_POSITION = (IMAGE_POSITION + 1) % len(list_of_character_image)
    WIN.blit(list_of_character_image[IMAGE_POSITION], (CHARACTER.x, CHARACTER.y))
  return IMAGE_POSITION

def draw_window(CHARACTER, BALLOONS, start_button_clicked, key_pressed, IMAGE_POSITION, last_direction):
  if is_video_ended() and not start_button_clicked:
    pygame.draw.ellipse(WIN, (0, 255, 0), START_BUTTON)
    START_BUTTON_IMAGE.blit(TEXT_SURFACE, (110 - 35, 60 - 25))
    WIN.blit(START_BUTTON_IMAGE, (WIDTH // 2 - 110, HEIGHT // 2 - 60))
  elif is_video_ended() and start_button_clicked:
    if last_direction == "right":
      WIN.blit(list_of_character_image[IMAGE_POSITION], (CHARACTER.x, CHARACTER.y))
    else:
      WIN.blit(flip_image(list_of_character_image[IMAGE_POSITION]), (CHARACTER.x, CHARACTER.y))
    if key_pressed[pygame.K_RIGHT]:
      IMAGE_POSITION = ctr_right_clicked(CHARACTER, key_pressed, IMAGE_POSITION)
      last_direction = "right"
    if key_pressed[pygame.K_LEFT]:
      IMAGE_POSITION = ctr_left_clicked(CHARACTER, key_pressed, IMAGE_POSITION)
      last_direction = "left"
   
  pygame.display.update()
  return IMAGE_POSITION, last_direction

def main():
  #initialize the time clock to handle fps
  clock = pygame.time.Clock()

  start_button_clicked = False

  CHARACTER = pygame.Rect(WIDTH // 2, HEIGHT - 116, CHARACTER_WIDTH, CHARACTER_HEIGHT)

  IMAGE_POSITION = 0
  last_direction = "right"

  # Initialize balloons
  BALLOONS = [pygame.Rect(random.randint(0, WIDTH), 0, BALLOON_DIMENSION[0], BALLOON_DIMENSION[1]) for _ in range(3)]

  run = True
  while run:

    clock.tick(FPS)
    #validating if the video is ended
    if is_video_ended():
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False  

      if event.type == pygame.MOUSEBUTTONDOWN:
        #if the button is clicked
        if START_BUTTON.collidepoint(event.pos):
          start_button_clicked = True
              
    key_pressed = pygame.key.get_pressed()    
    WIN.blit(BACKGROUND, (0,0))
    is_video_ended()
    IMAGE_POSITION, last_direction = draw_window(CHARACTER, BALLOONS, start_button_clicked, key_pressed, IMAGE_POSITION, last_direction)

    # Move the balloons down
    for i, BALLOON in enumerate(BALLOONS):
        if start_button_clicked:
            BALLOON.y += BALLOON_VEL
            # If the balloon hits the bottom of the screen, reset its position
            if BALLOON.y > HEIGHT:
                FONT = pygame.font.SysFont('Comic Sans MS', 50)
                TEXT_SURFACE = FONT.render('Game Over', True, (255, 0, 0))
                WIN.blit(TEXT_SURFACE, (WIDTH // 2 - TEXT_SURFACE.get_width() // 2, HEIGHT // 2 - TEXT_SURFACE.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(2000)
                run = False

            # Draw the balloon
            WIN.blit(list_of_balloon_image[i], (BALLOON.x, BALLOON.y))

            # Check for collision between the character and the balloon
            if CHARACTER.colliderect(BALLOON):
                FONT = pygame.font.SysFont('Comic Sans MS', 50)
                TEXT_SURFACE = FONT.render('Game Over', True, (255, 0, 0))
                WIN.blit(TEXT_SURFACE, (WIDTH // 2 - TEXT_SURFACE.get_width() // 2, HEIGHT // 2 - TEXT_SURFACE.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(2000)
                run = False

  pygame.quit()


if __name__ == "__main__":
  main()
