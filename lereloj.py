import pygame
import os
import time
from datetime import datetime
import pytz.reference
import repubcal

pc = True

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
            # Replace with connect / disconnect function
            pygame.joystick.init()
            gamepad = pygame.joystick.Joystick(0)
            gamepad.init()
            # Render screen
            pygame.display.update()
        else:
            pygame.display.init()
            self.size = (pygame.display.Info().current_w,
                        pygame.display.Info().current_h)
            pygame.joystick.init()
            gamepad = pygame.joystick.Joystick(0)
            gamepad.init()
            pygame.font.init()
            self.screen = pygame.display.set_mode((1280,720))
            self.screen.fill((0,0,0))
            pygame.display.update()

    def leClock(self):
        """
        :return: Republican Calendar and Decimal  Time 
                 according to local time zone
        :rtype: list
        Using repubcal module from https://github.com/Nimlar/repubcal
        Decimal time formula based on metric-time by Lakhan Mankani
        https://pypi.org/project/metric-time/
        """
        date = repubcal.RDate.today()
        season = "{:%rf}".format(date)
        day = "{:%rA}".format(date)
        month = "{:%rB}".format(date)
        year = "{:%ry}".format(date)
        # Get local datetime from timezone
        ltz = pytz.reference.LocalTimezone()
        now = datetime.now(ltz)
        # Calcuate seconds from midnight
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        nsfm = (now - midnight).total_seconds()
        # Remap normal seconds to metric seconds
        metricSeconds = nsfm / 0.864
        # Remap clock from metric seconds
        hours = "{:02d}".format((int(metricSeconds / 10000)))
        minutes = "{:02d}".format(int(metricSeconds / 100) % 100)
        seconds = "{:02d}".format(int(metricSeconds % 100))
        miliseconds = "{:03d}".format(int((metricSeconds - int(metricSeconds)) * 1000))
        leclock = [year,month,day,season,
                   hours,minutes,seconds,miliseconds]
        # Return a list with calendar and clock values
        return leclock

    def leDisplay(self):
        clock = pygame.time.Clock()
        fontFile = 'Digestive.otf'
        fontSize = 420
        font = pygame.font.Font(fontFile, fontSize)
        opt = 0
        bgcolor = self.black
        fontcolor = self.white
        while True:
        #for x in range(0,600):
            clock.tick(100)
            displaylist = self.leClock()
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if opt < len(displaylist)-1:
                        opt = opt+1
                    else:
                        opt = 0
                    if opt <= 3:
                        bgcolor = self.black
                        fontcolor = self.white
                    else:
                        bgcolor = self.white
                        fontcolor = self.black
            self.screen.fill(bgcolor)
            text = font.render(str((displaylist[opt])), True, fontcolor)
            textRect = text.get_rect()
            textRect.center = (self.size[0]//2,self.size[1]//2)
            self.screen.blit(text,textRect)
            pygame.display.update()
    
    def __del__(self):
        "Destructor to make sure pygame shuts down"

if __name__ == '__main__':
    lereloj = lereloj()
    lereloj.leDisplay()