import pygame
import os
import time
from datetime import datetime
import pytz.reference
import repubcal
import argo

class lereloj:
    screen = None;

    def __init__(self):
        """
        Initializes a new pygame instance using display resolution as fullscreen
        """
        # Let's set some variables first!
        # Define color pallete for further use
        self.white = (255,255,255)
        self.black = (0,0,0)
        self.gray = (125,125,125)
        # Initialize display and get screen resolution
        pygame.display.init()
        self.size = (pygame.display.Info().current_w,
                    pygame.display.Info().current_h)
        # Inits joystick support
        # Replace later with a full function that updates in the mainloop
        self.gamepadpresent = False
        try:
            pygame.joystick.init()
            self.gamepad = pygame.joystick.Joystick(0)
            self.gamepad.init()
            self.gamepadpresent = True
        except:
            print("No Joystick present. Moving on.")
        # Inits Font Support
        pygame.font.init()
        # Set display mode and display update
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.screen.fill(self.black)
        pygame.mouse.set_visible(False)
        pygame.display.update()

    def getCurrentSeason(self, date):
        """
        Checks month number and returns current season
        """
        nmonth = int("{:%rm}".format(date))
        seasons = ["Automne","Hiver","Printemps","Été"]
        if nmonth >= 1 and nmonth <= 3:
            return seasons[0]
        elif nmonth > 3 and nmonth <= 6:
            return seasons[1]
        elif nmonth > 6  and nmonth <= 9:
            return seasons[2]
        elif nmonth > 9 and nmonth <= 12:
            return seasons[3]

    def getJSON(self):
        jsonFile = './config.json'
        data = []
        data = argo.JSON.bringThis(self,jsonFile)
        return data

    def saveJSON(self,data):
        jsonFile = './config.json'
        try:
            argo.JSON.saveThis(self,data,jsonFile)
        except Exception as e:
            print("NOPE because: {0}".format(e))

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
        year = "{:%ry}".format(date)
        month = "{:%rB}".format(date)
        day = "{:%rA}".format(date)
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
        """
        clock = pygame.time.Clock()
        jsondata = self.getJSON()
        fontFile = 'Digestive.otf'
        fontOffsetX = jsondata[0]
        fontOffsetY = jsondata[1]
        fontSize = jsondata[2]
        opt = jsondata[3]
        rotate = 90
        bgcolor = jsondata[4]
        fontcolor = jsondata[5]
        run = True
        font = pygame.font.Font(fontFile, fontSize)
        editMode = False
        antialias = True
        while run == True:
            clock.tick(100)
            displaylist = self.leClock()
            if self.gamepadpresent:
                g = self.gamepad
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        if g.get_button(9):
                            if editMode == False:
                                editMode = True
                            else:
                                dictdata = [fontOffsetX, fontOffsetY, 
                                            fontSize, opt, bgcolor, fontcolor]
                                self.saveJSON(dictdata)
                                editMode = False
                        if editMode == True:
                            font = pygame.font.Font(fontFile, fontSize)
                            if g.get_button(2):
                                if antialias == True:
                                    antialias = False
                                else:
                                    antialias = True
                            if g.get_button(4):
                                fontSize = int(fontSize/1.1)
                            if g.get_button(5):
                                fontSize = int(fontSize*1.1)
                            if g.get_button(4):
                                fontSize = int(fontSize/1.1)
                            if g.get_button(5):
                                fontSize = int(fontSize*1.1)
                            if g.get_button(3):
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
                        if g.get_button(8):
                            run = False
                    if event.type == pygame.JOYAXISMOTION:
                        if editMode == True:
                            if g.get_axis(1) > 0.1:
                                fontOffsetX = fontOffsetX + 20
                            elif g.get_axis(1) < -0.1:
                                fontOffsetX = fontOffsetX - 20
                            elif g.get_axis(0) > 0.1:
                                fontOffsetY = fontOffsetY - 20
                            elif g.get_axis(0) < -0.1:
                                fontOffsetY = fontOffsetY + 20
            self.screen.fill(bgcolor)
            text = font.render(str((displaylist[opt])), antialias, fontcolor)
            rtext = pygame.transform.rotate(text, rotate)
            textRect = rtext.get_rect()
            textRect.center = (self.size[0]//2+fontOffsetX,
                                self.size[1]//2+fontOffsetY)
            self.screen.blit(rtext,textRect)
            pygame.display.update()
    
    def __del__(self):
        "Destructor to make sure pygame shuts down"

if __name__ == '__main__':
    lereloj = lereloj()
    lereloj.leDisplay()