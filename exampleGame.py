import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 900
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Example Screen")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw a blue rectangle - simulate countries
    pygame.draw.rect(screen, BLUE, (100, 100, 200, 200))
    pygame.draw.rect(screen, BLUE, (100, 350, 200, 200))
    pygame.draw.rect(screen, BLUE, (350, 100, 200, 200))
    pygame.draw.rect(screen, BLUE, (350, 350, 200, 200))
    pygame.draw.rect(screen, BLUE, (600, 100, 200, 200))
    pygame.draw.rect(screen, BLUE, (600, 350, 200, 200))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
