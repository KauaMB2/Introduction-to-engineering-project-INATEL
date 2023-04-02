import pygame
import subprocess

# Initialize Pygame
pygame.init()

# Define the dimensions of the screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define the font
font = pygame.font.Font(None, 36)

# Define the button
button_text = "Click me for Tkinter!"
button_surface = font.render(button_text, True, BLACK)
button_rect = button_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# Define the function to launch the Tkinter window
def show_tkinter_page():
    subprocess.call(["python", "my_tkinter.py"])

# Start the game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                show_tkinter_page()

    # Draw the button
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, button_rect, 2)
    screen.blit(button_surface, button_rect)

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()