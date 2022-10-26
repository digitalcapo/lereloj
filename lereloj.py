import pygame
import os
import time
from datetime import datetime
import pytz.reference
import repubcal
import argo
import ptext
import random
from subprocess import call

class lereloj:
    screen = None;

    def __init__(self):
        """
        Initializes a new pygame instance using display resolution as fullscreen
        """
        # Let's set some variables first!
        # Define color pallete for further use
        self.white = (255,255,255)
        self.black = (0,0,255)
        self.gray = (125,125,125)
        # Initialize display and get screen resolution
        pygame.display.init()
        self.size = (pygame.display.Info().current_w,
                    pygame.display.Info().current_h)
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.screen.fill(self.black)
        pygame.mouse.set_visible(False)
        pygame.display.update()

    def getCurrentSeason(self, date):
        """
        Checks month number and returns current season
        """
        nmonth = int("{:%rm}".format(date).encode('utf-8'))
        seasons = ["Automne","Hiver","Printemps","Été"]
        if nmonth >= 1 and nmonth <= 3:
            return seasons[0]
        elif nmonth > 3 and nmonth <= 6:
            return seasons[1]
        elif nmonth > 6  and nmonth <= 9:
            return seasons[2]
        elif nmonth > 9 and nmonth <= 12:
            return seasons[3]

    def leClock(self):
        """
        :return: Republican Calendar & Decimal Time in local time zone
        :rtype: list
        # Using repubcal module from https://github.com/Nimlar/repubcal
        # Decimal time formula based on metric-time by Lakhan Mankani
        # https://pypi.org/project/metric-time/
        """
        # Get current date
        date = repubcal.RDate.today()
        # Remap to Republican Calendar
        year = int("{:%ry}".format(date))
        month = "{:%rB}".format(date)
        day = str("{:%rA}".format(date))
        season = str(self.getCurrentSeason(date))
        # Get local datetime from timezone
        ltz = pytz.reference.LocalTimezone()
        now = datetime.now(ltz)
        # Calcuate seconds from midnight
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        nsfm = (now - midnight).total_seconds()
        # Remap normal seconds to metric seconds
        metricSeconds = nsfm / 0.864
        milimetricseconds = int((metricSeconds - int(metricSeconds)) * 1000)
        # Remap clock from metric seconds
        hours = "{:02d}".format((int(metricSeconds / 10000)))
        minutes = "{:02d}".format(int(metricSeconds / 100) % 100)
        seconds = "{:02d}".format(int(metricSeconds % 100))
        miliseconds = "{:03d}".format(milimetricseconds)
        leclock = [year,month,day,season,
                   hours,minutes,seconds,miliseconds]
        # Return a list with calendar and clock values
        return leclock

    def leDisplay(self):
        """
        Main Loop. Renders text, with position and scale set by gamepad input
        Brings last saved data from a JSON file.
        """
        clock = pygame.time.Clock()
        fontFile = 'Digestive.otf'
        run = True
        # This enables/disables option selection
        editMode = False
        # Initial Direction (based on rotation)
        direction = 1
        # Here everything goes a bit crazy, but it works
        while run == True:
            clock.tick(60)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                    pygame.quit()
            # Execute clock / calendar code, store in list.
            displaylist = self.leClock()
            #
            font = pygame.font.Font(fontFile, 200)
            self.screen.fill(self.black)
            grect = pygame.rect.Rect(0,0, self.size[0], self.size[1])
            options = [0,1,2,3,4,5,6,7]
            settings = [{"size":3,"angle":270,"posx":2,"posy":2,'align':"center","anchor":(0.5,0.5)},
                        {"size":5,"angle":0,"posx":1,"posy":.97,'align':"left","anchor":(1,1)},
                        {"size":4,"angle":180,"posx":2,"posy":1.1,'align':"center","anchor":(-.5,0)},
                        {"size":5,"angle":0,"posx":2,"posy":3.1,'align':"center","anchor":(0.5,1)},
                        {"size":2.5,"angle":90,"posx":3.3,"posy":3,'align':"left","anchor":(.4,.75)},
                        {"size":2.5,"angle":0,"posx":1.22,"posy":2,'align':"center","anchor":(1,.75)},
                        {"size":2.5,"angle":0,"posx":.99,"posy":2,'align':"center","anchor":(1,0.75)},
                        {"size":4.6,"angle":180,"posx":2,"posy":1.15,'align':"right","anchor":(.5,0.5)}]
            for each in options:
                selectedText = str((displaylist[each]))
                fontSize =(self.size[0]//settings[each]["size"])
                textPos = (self.size[0]//settings[each]["posx"],
                                    self.size[1]//settings[each]["posy"])
                text = ptext.draw(selectedText, textPos,
                                fontname=fontFile, fontsize=fontSize, align=settings[each]["align"],
                                color=self.white, anchor=settings[each]["anchor"],
                                angle=settings[each]["angle"], cache=False)

            pygame.display.update()
              
    def __del__(self):
        '''Destructor to make sure pygame shuts down'''

if __name__ == '__main__':
    lereloj = lereloj()
    lereloj.leDisplay()