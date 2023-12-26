# Import the Pygame library
import pygame

# Initialize Pygame
pygame.init()

# Set the width and height of the game window
WIDTH = 800
HEIGHT = 600

# Set the speed at which the balloons fall
BALLOON_SPEED = 1

# Set the number of balloons
NUM_BALLOONS = 100

# Create a window
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a list to store the balloons
balloons = []
balloon_rects = []

# Load an image for each balloon and get its rectangle
for i in range(NUM_BALLOONS):
    balloon = pygame.image.load('balloon1.png')
    rect = balloon.get_rect()
    rect.topleft = (WIDTH // 2, -i * HEIGHT // 2)
    balloons.append(balloon)
    balloon_rects.append(rect)

# Start the game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the balloons down
    for rect in balloon_rects:
        rect.y += BALLOON_SPEED

        # If a balloon has moved off the bottom of the window, move it back to the top
        if rect.top > HEIGHT:
            rect.y = -rect.height

    # Draw everything
    window.fill((255, 255, 255))  # Fill the window with white
    for i in range(NUM_BALLOONS):
        window.blit(balloons[i], balloon_rects[i])  # Draw the balloon

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
