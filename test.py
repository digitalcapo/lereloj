# import time,pygame
# #initialize pygame library
# pygame.init()
# theFont=pygame.font.Font('aAtmospheric.ttf',72)
# clock = pygame.time.Clock()
# screen = pygame.display.set_mode([1280, 720])
# pygame.display.set_caption('Pi Time')

# while True:
#     clock.tick()
#     theTime=time.strftime("%H:%M:%S", time.localtime())
#     timeText=theFont.render(str(theTime), True,(255,255,255),(0,0,0))
#     screen.blit(timeText, (80,60))
#     pygame.display.update()


import pygame
from datetime import datetime
import os

# os.environ["SDL_VIDEODRIVER"]="dummy"
pygame.init()

os.putenv('SDL_VIDEODRIVER', 'fbcon')
pygame.display.init()

pygame.display.set_caption('Show Text')

black = (0, 0, 0) 
white = (255, 255, 255)
blue = (0, 0, 128) 

X = 640
Y = 360

display_surface = pygame.display.set_mode((X, Y),)#pygame.FULLSCREEN)

fontfile = 'Digestive.otf'

font = pygame.font.Font(fontfile, 120)


# create a text suface object, 
# on which text is drawn on it. 

gettime = datetime.now()
now = gettime.strftime("%H:%M:%S")
text = font.render(now, True, white)
  
# create a rectangular object for the 
# text surface object 
textRect = text.get_rect()

# set the center of the rectangular object.
textRect.center = (X // 2, Y // 2) 

clock = pygame.time.Clock()

# infinite loop 
while True :
    clock.tick()
    # completely fill the surface object
    # with white color
    display_surface.fill(black)
    gettime = datetime.today()
    newsec = str(gettime.strftime("%S"))
    #newmin = str(int(int(gettime.strftime("%f"))*.66)/100000)
    text = font.render(newsec, True, white)
    # copying the text surface object 
    # to the display surface object  
    # at the center coordinate.
    display_surface.blit(text, textRect)
    pygame.display.update() 
    # iterate over the list of Event objects 
    # that was returned by pygame.event.get() method. 
    for event in pygame.event.get():
        # if event object type is QUIT
        # then quitting the pygame 
        # and program both. 
        if event.type == pygame.QUIT : 
  
            # deactivates the pygame library 
            pygame.quit()
  
            # quit the program. 
            quit() 
  
        # Draws the surface object to the screen.   
        pygame.display.update()
