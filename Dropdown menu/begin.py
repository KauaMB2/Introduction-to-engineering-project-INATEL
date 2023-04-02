import pygame

# Define some constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
DROPDOWN_WIDTH = 150
DROPDOWN_HEIGHT = 30

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dropdown Box")

# Define a function to draw the dropdown box
def draw_dropdown_box(selected_option):
    # Draw the box outline
    pygame.draw.rect(screen, (0, 0, 0), (10, 10, DROPDOWN_WIDTH, DROPDOWN_HEIGHT), 1)
    # Draw the selected option
    font = pygame.font.SysFont(None, 20)
    text = font.render(selected_option, True, (0, 0, 0))
    screen.blit(text, (20, 15))

# Define a list of options
options = ['Option 1', 'Option 2', 'Option 3']
selected_option = options[0]

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked inside the dropdown box
            if event.pos[0] >= 10 and event.pos[0] <= 10 + DROPDOWN_WIDTH and event.pos[1] >= 10 and event.pos[1] <= 10 + DROPDOWN_HEIGHT:
                # Display the options as a dropdown list
                font = pygame.font.SysFont(None, 20)
                for i, option in enumerate(options):
                    text = font.render(option, True, (0, 0, 0))
                    screen.blit(text, (10, 10 + DROPDOWN_HEIGHT + i*DROPDOWN_HEIGHT))
                pygame.display.flip()
                # Wait for the user to select an option
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Check if the user clicked on an option
                        for i, option in enumerate(options):
                            if event.pos[0] >= 10 and event.pos[0] <= 10 + DROPDOWN_WIDTH and event.pos[1] >= 10 + (i+1)*DROPDOWN_HEIGHT and event.pos[1] <= 10 + (i+2)*DROPDOWN_HEIGHT:
                                selected_option = option
                                break
                        # Hide the dropdown list
                        pygame.draw.rect(screen, (255, 255, 255), (10, 10 + DROPDOWN_HEIGHT, DROPDOWN_WIDTH, len(options)*DROPDOWN_HEIGHT))
                        draw_dropdown_box(selected_option)
                        pygame.display.flip()
                        break

    # Update game state

    # Draw game objects
    screen.fill((255, 255, 255))
    draw_dropdown_box(selected_option)

    # Update display
    pygame.display.flip()