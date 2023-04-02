import pygame
import sys

# Define some constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Button")

# Define a function to draw the button
def draw_button(x, y, text):
    # Draw the button rectangle
    pygame.draw.rect(screen, (0, 0, 0), (x, y, BUTTON_WIDTH, BUTTON_HEIGHT), 1)
    # Draw the button text
    font = pygame.font.SysFont(None, 20)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x + 10, y + 15))

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on the button
            if event.pos[0] >= 10 and event.pos[0] <= 10 + BUTTON_WIDTH and event.pos[1] >= 10 and event.pos[1] <= 10 + BUTTON_HEIGHT:
                print("Button clicked")

    # Update game state

    # Draw game objects
    screen.fill((255, 255, 255))
    draw_button(10, 10, "Click me")

    # Update display
    pygame.display.flip()