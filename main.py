import pygame
import subprocess
# Define the function to launch the Tkinter window
def showInfoPage():#Function that calls the Info page
    subprocess.call(["python", "my_tkinter.py"])
pygame.init()#It initializes pygame

# Widths and heights
SCREEN_WIDTH=640
SCREEN_HEIGHT=480
TOP_RECT_HEIGHT=int(SCREEN_HEIGHT * 0.11)

#Colors
TOP_RECT_COLOR=(0, 0, 102)
BLACK=(0,0,0)
COLOR_INACTIVE=pygame.Color('lightskyblue3')
COLOR_ACTIVE=pygame.Color('dodgerblue2')
COLOR_INPUT_USER=COLOR_INACTIVE
COLOR_INPUT_PASSWORD=COLOR_INACTIVE

#Inputs content
textInputUser=''
textInputPassword=''
screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))#Set the Width and height of the screen

#Control variables
activeInputUser=False
activeInputPassword=False

#Donts
font1=pygame.font.SysFont('arial', 32, True, False)
font2=pygame.font.Font(None, 32)
font3=pygame.font.SysFont('arial', 25, True, False)
pygame.time.Clock().tick(120)#Defines the FPS limit

#Set up the input box
inputUser=pygame.Rect(50, 150, 200, 32)
inputPassword=pygame.Rect(50,250,200,32)


while True:
    for event in pygame.event.get():#Pass in each event
        if event.type==pygame.QUIT:#If the quit button was clicked...
            pygame.quit()#Go out pygame
            quit()#Go out aplication
        elif event.type==pygame.MOUSEBUTTONDOWN:#If happened a mouse click...
            xPos, yPos=event.pos#It gets the mouse position
            print(f"Mouse position: X={xPos} - Y={yPos}")
            if((xPos>590)and(xPos<640)and(yPos>0)and(yPos<50)):#Info button clicked...
                showInfoPage()
            if((xPos>30)and(xPos<155)and(yPos>385)and(yPos<455)):#Login button clicked...
                print("Login!")
            if((xPos>240)and(xPos<420)and(yPos>385)and(yPos<455)):#Recognize face button clicked...
                print("Recognize!")
            if((xPos>485)and(xPos<606)and(yPos>385)and(yPos<455)):#Register face button clicked...
                print("Register!")
            if inputUser.collidepoint(event.pos):#Input user clicked...
                activeInputUser=not activeInputUser#Toggle the var
            else:#Click happened out of Input user
                activeInputUser=False
            if inputPassword.collidepoint(event.pos):#Input password clicked...
                activeInputPassword=not activeInputPassword#Toggle the var
            else:#Clicked out of Input user
                activeInputPassword=False
            # change the color of the input box
            COLOR_INPUT_USER=COLOR_ACTIVE if activeInputUser else COLOR_INACTIVE
            COLOR_INPUT_PASSWORD=COLOR_ACTIVE if activeInputPassword else COLOR_INACTIVE
        if event.type==pygame.KEYDOWN:
            if event.unicode.isprintable():
                textInputUser += event.unicode
            elif event.key==pygame.K_BACKSPACE:
                textInputUser=textInputUser[:-1]
    screen.fill((180, 50, 180))
    pygame.draw.rect(screen, TOP_RECT_COLOR, (0, 0, SCREEN_WIDTH, TOP_RECT_HEIGHT))
    #Importing files and adding elements
    logo=pygame.image.load('imgs/logo.png')#Cria objeto para a imagemLogo
    logo=pygame.transform.scale(logo, (230, 40))#Defines the new width and height of the image
    screen.blit(logo,(0, 5))
    infoBtn=pygame.image.load('imgs/info.png')#Cria objeto para a imagemLogo
    infoBtn=pygame.transform.scale(infoBtn, (70, 70))#Defines the new width and height of the image
    screen.blit(infoBtn, (SCREEN_WIDTH*0.90, -10))
    loginBtn=pygame.image.load('imgs/loginBtn.png')#Cria objeto para a imagemLogo
    loginBtn=pygame.transform.scale(loginBtn, (130, 70))#Defines the new width and height of the image
    screen.blit(loginBtn, (30, SCREEN_HEIGHT*0.80))
    registerBtn=pygame.image.load('imgs/registerBtn.png')#Cria objeto para a imagemLogo
    registerBtn=pygame.transform.scale(registerBtn, (130, 70))#Defines the new width and height of the image
    screen.blit(registerBtn, ((SCREEN_WIDTH-160), SCREEN_HEIGHT*0.80))
    recognizeBtn=pygame.image.load('imgs/recognizeBtn.png')#Cria objeto para a imagemLogo
    recognizeBtn=pygame.transform.scale(recognizeBtn, (180, 70))#Defines the new width and height of the image
    screen.blit(recognizeBtn, (SCREEN_WIDTH//2-80, SCREEN_HEIGHT*0.80))
    
    textFormated1=font3.render("User: ", False, BLACK)
    userLabel=textFormated1.get_rect()
    userLabel.center=(85, 130)
    screen.blit(textFormated1, userLabel)
    textFormated3=font3.render("Password: ", False, BLACK)
    passwordLabel=textFormated3.get_rect()
    passwordLabel.center=(115, 230)
    screen.blit(textFormated3, passwordLabel)
    textFormated2=font3.render("Welcome to MoveVision!!", False, BLACK)
    welcomeText=textFormated2.get_rect()
    welcomeText.center=(SCREEN_WIDTH//2, 70)
    screen.blit(textFormated2, welcomeText)
    # Render the inputUser text
    txtUser=font2.render(textInputUser, True, (0,0,0))
    # Resize the box if the useText is too long
    width=max(200, txtUser.get_width()+10)
    inputUser.w=width
    # Draw the input box and text surface
    pygame.draw.rect(screen, COLOR_INPUT_USER, inputUser, border_radius=5)
    screen.blit(txtUser, inputUser)
    # Render the inputUser text
    txtPassword=font2.render(textInputPassword, True, (0,0,0))
    # Resize the box if the useText is too long
    width=max(200, txtPassword.get_width()+10)
    inputPassword.w=width
    # Draw the input box and text surface
    pygame.draw.rect(screen, COLOR_INPUT_PASSWORD, inputPassword, border_radius=5)
    screen.blit(txtPassword, inputPassword)
    # Update display
    pygame.display.flip()