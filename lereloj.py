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
        self.black = (0,0,0)
        self.gray = (125,125,125)
        # Initialize display and get screen resolution
        pygame.display.init()
        self.size = (pygame.display.Info().current_w,
                    pygame.display.Info().current_h)
        # Inits joystick support
        self.gamepadpresent = False
        self.gamepad = None
        # Checks if initally connected to the pi
        try:
            self.isGamepadConnected()
        except:
            print("No Joystick present. Moving on.")
        # Set display mode and display update
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.screen.fill(self.black)
        pygame.mouse.set_visible(False)
        pygame.display.update()

    def isGamepadConnected(self):
        """
        Checks if gamepad is connected and initializes pygame.joystick
        """
        if self.gamepadpresent == False:
            pygame.joystick.quit()
            pygame.joystick.init()
            joycount = pygame.joystick.get_count()
            if joycount > 0:
                self.gamepad = pygame.joystick.Joystick(0)
                self.gamepad.init()
                self.gamepadpresent = True
            else:
                if self.gamepadpresent == True:
                    self.gamepadpresent = False


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

    def glitcher(self, iter):
        """
        Last minute update:
        Add .png texture with alpha over the main screen depending on option
        """
        imageFile = "glitches/{:01d}.png".format(iter)
        if os.path.exists(imageFile):
            return imageFile
        else:
            return None

    def leDisplay(self):
        """
        Main Loop. Renders text, with position and scale set by gamepad input
        Brings last saved data from a JSON file.
        """
        clock = pygame.time.Clock()
        jsondata = self.getJSON()
        fontFile = 'Digestive.otf'
        # Load settings from JSON
        # Font Settings
        fontOffsetX = jsondata[0]
        fontOffsetY = jsondata[1]
        fontSize = jsondata[2]
        # Option changes display type (year,month,day,etc)
        opt = jsondata[3]
        bgcolor = jsondata[4]
        fontcolor = jsondata[5]
        # Rotation
        rotate = jsondata[6]
        # killSwitch variable
        run = True
        # This enables/disables option selection
        editMode = False
        # Initial Direction (based on rotation)
        direction = 1
        # Glitch managment. Not all screens have a glitch.
        glitch = True
        # Preload image file to draw faster on blip()
        gpreload = self.glitcher(opt)
        gimage = pygame.image.load(gpreload).convert_alpha()
        # Here everything goes a bit crazy, but it works
        while run == True:
            clock.tick(60)
            # Checks glitch again
            gpreload = self.glitcher(opt)
            # Force alpha premult
            gimage = pygame.image.load(gpreload).convert_alpha()
            # Execute clock / calendar code, store in list.
            displaylist = self.leClock()
            # Check gamepad connected. If so, listen to inputs.
            self.isGamepadConnected()
            if self.gamepadpresent:
                g = self.gamepad
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        if g.get_button(9):
                            if editMode == False:
                                editMode = True
                            else:
                                dictdata = [fontOffsetX, fontOffsetY, 
                                            fontSize, opt, bgcolor, fontcolor, rotate]
                                self.saveJSON(dictdata)
                                editMode = False
                        if editMode == True:
                            font = pygame.font.Font(fontFile, fontSize)
                            if g.get_button(2):
                                fontOffsetX=0
                                fontOffsetY=0
                                fontSize=200
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
                            if g.get_button(1):
                                if rotate == 90:
                                    rotate = -90
                                    direction = -1
                                else:
                                    rotate = 90
                                    direction = 1
                        if g.get_button(8):
                            run = False
                            call("sudo nohup shutdown -h now", shell=True)
                    if event.type == pygame.JOYAXISMOTION:
                        if editMode == True:
                            offsetN = 20 * direction
                            if g.get_axis(1) > 0.1:
                                fontOffsetX = fontOffsetX + offsetN
                            elif g.get_axis(1) < -0.1:
                                fontOffsetX = fontOffsetX - offsetN
                            elif g.get_axis(0) > 0.1:
                                fontOffsetY = fontOffsetY - offsetN
                            elif g.get_axis(0) < -0.1:
                                fontOffsetY = fontOffsetY + offsetN
            self.screen.fill(bgcolor)
            grect = pygame.rect.Rect(0,0, self.size[0], self.size[1])
            selectedText = str((displaylist[opt]))
            textPos = (self.size[0]//2+fontOffsetX,
                                self.size[1]//2+fontOffsetY)
            if opt == 2 or opt == 3 or opt == 4 or opt == 5:
                glitch = True
            else:
                glitch = False
            if glitch == True:
                self.screen.blit(gimage, grect)
            text = ptext.draw(selectedText, textPos,
                            fontname=fontFile, fontsize=fontSize, align="center",
                            color=fontcolor, anchor=(0.5,0.5),
                            angle=rotate, cache=False)
            pygame.display.update()
    
    def __del__(self):
        '''Destructor to make sure pygame shuts down'''

if __name__ == '__main__':
    lereloj = lereloj()
    lereloj.leDisplay()