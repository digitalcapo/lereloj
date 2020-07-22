import pygame
import os
import time
from datetime import datetime
import pytz.reference

pc = False

class lereloj:
    screen = None;

    def __init__(self):
        "Initializes a new pygame using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        # Define color pallete for further use
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.gray = (125,125,125)

        if not pc:
            # quick and dirty way to debug on PC
            #
            disp_no = os.getenv("DISPLAY")
            if disp_no:
                print("I'm running under X display = {0}".format(disp_no))
            # Use fbcon as display driver
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            try:
                pygame.display.init()
            except pygame.error:
                print('Pygame Display Init failed')

            self.size = (pygame.display.Info().current_w,
                    pygame.display.Info().current_h)

            print("Framebuffer size: {0} x {1}".format(self.size[0], self.size[1]))
            self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
            # Clear screen
            self.screen.fill((0,0,0))
            # Init font support
            # Will replace later with ptext module
            pygame.font.init()
            # init Joystick 
            pygame.joystick.init()
            gamepad = pygame.joystick.Joystick(0)
            gamepad.init()
            # Render screen
            pygame.display.update()
        else:
            pygame.display.init()
            pygame.joystick.init()
            gamepad = pygame.joystick.Joystick(1)
            gamepad.init()
            pygame.font.init()
            self.screen = pygame.display.set_mode((1920,1080))
            self.screen.fill((0,0,0))
            pygame.display.update()


    def decimalTime(self):
        """
        :return: Decimal time according to local time zone
        :rtype: list
        Based on metric-time by Lakhan Mankani
        https://pypi.org/project/metric-time/
        """
        # Get local datetime from timezone
        ltz = pytz.reference.LocalTimezone()
        now = datetime.now(ltz)
        # Calcuate seconds from midnight
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        nsfm = (now - midnight).total_seconds()
        # Remap normal seconds to metric seconds
        metricSeconds = nsfm / 0.864
        # Remap clock from metric seconds
        hours = int(metricSeconds / 10000)
        minutes = int(metricSeconds / 100) % 100
        seconds = int(metricSeconds % 100)
        miliseconds = int((metricSeconds - int(metricSeconds)) * 1000)
        metricTime = [hours,minutes,seconds,miliseconds]
        # Return a list with clock values
        return metricTime

    def leClock(self):
        clock = pygame.time.Clock()
        fontFile = 'Digestive.otf'
        font = pygame.font.Font(fontFile, 420)
        opt = 0
        for x in range(0,2000):
            clock.tick(100)
            for event in pygame.event.get(): # User did something.
                if event.type == pygame.JOYBUTTONDOWN:
                    if opt < 3:
                        opt = opt+1
                    else:
                        opt = 0
                    print("Joystick button pressed.")
                elif event.type == pygame.JOYBUTTONUP:
                    print("Joystick button released.")
            self.screen.fill(self.black)
            text = font.render(str('{:02d}'.format(self.decimalTime()[opt])), True, self.white)
            textRect = text.get_rect()
            textRect.center = (self.size[0]//2,self.size[1]//2)
            self.screen.blit(text,textRect)
            pygame.display.update()
    
    def __del__(self):
        "Destructor to make sure pygame shuts down"

if __name__ == '__main__':
    lereloj = lereloj()
    lereloj.leClock()