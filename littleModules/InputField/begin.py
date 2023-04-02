import pygame

pygame.init()

# Set up the display
screen = pygame.display.set_mode((640, 480))

# Set up the font and text input box
font = pygame.font.Font(None, 32)
input_box = pygame.Rect(10, 10, 200, 30)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
text = ''
active = False

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Handle text input events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input box, toggle the active variable
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            # Change the input box color based on whether it is active or inactive
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if event.unicode.isprintable():
                text += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]

    # Fill the background
    screen.fill((255, 255, 255))

    # Render the input box text
    txt_surface = font.render(text, True, (0,0,0))
    # Resize the box if the text is too long
    width = max(200, txt_surface.get_width()+10)
    input_box.w = width
    # Draw the input box and text surface
    pygame.draw.rect(screen, color, input_box, border_radius=5)
    screen.blit(txt_surface, input_box)

    # Update the display
    pygame.display.update()
