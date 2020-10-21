# Le Reloj | A Raspi based Republican Calendar & Decimal Time Device

## Description
Raspberry Pi Zero W powered, PyGame script that displays decimal time and Republican Calendar using Local Timezone.

Made for Adrian Villar Rojas exhibition *La Fin de'l Imagination* https://www.mariangoodman.com/exhibitions/adrian-villar-rojas-la-fin-de-limagination-paris/

<img src="https://i.imgur.com/88HNPsL.png" width="650">

## Journal

The goal was simple, the task at hand... not so much: 

8 screens, 4 displaying the current year, month, day, season in the [French Republican Calendar](https://en.wikipedia.org/wiki/French_Republican_calendar) format.

The other 4 would display hours, minutes, seconds and milliseconds.

![](https://i.imgur.com/oj0cpmd.jpg)

There were some initial obstacles that needed to be addressed for this to work:
- How to get sync between the screens and current time without breaking the bank? If you do it on video loops, they should be broadcasted from a video switcher, and that alone is really expensive / hard to setup.
- I'm based on Argentina and the exhibition is in Paris. Add 'covid-19' to the equation, so travelling over to Paris for a couple of weeks was not the ideal scenario to say the least. So it needed to be something *replicable* on the other side, but simple enough to be setup by regular staff from the gallery.

Soon enough, the Raspberry Pi Zero W came to answer all my problems. My idea was to write a script that uses a game engine to display in real-time the actual local time, synced over WiFi using the Network Time Protocol. It would be the same script, but depending on configuration it would change the display type.

This was the first design on paper:

<img src="https://i.imgur.com/o8PRXDQ.jpg" width="650">


A trello board is also a great tool to quick start development!

![](https://i.imgur.com/tUfvVnS.png)

The deadline was a couple of months ahead, but my internal scope had 2 weeks. 1 week for prototype, 1 week to polish.

Once I got confirmation, I bought a Raspberry Pi Zero W with next day delivery: 

Rasbperry Pi Zero W        |  USB Joystick + Power Supply
:-------------------------:|:-------------------------:
![](https://i.imgur.com/la01fgc.jpg) |  ![](https://i.imgur.com/Z7nmaLq.jpg)


The only bump in the road was... I forgot to order an SD card. Since I had all my main equipment on another location (we were on strict lockdown at that time, yikes), but an old abandoned home camera came to rescue! Inside it was an 8gb micro SDcard, so I could format it and start developing while I wait for a new one.

<img src="https://i.imgur.com/ecY0V1R.jpg" width="500">

After installing the base OS, next dat I had some first tests on Decimal time, based on this repo: [repo]

<img src="https://i.imgur.com/R6iBRxF.png" width="650">

At first the font was displayed via default pygame font library, but got later replaced by ptext, really handy features to handle size, position and antialiasing: [repo]


 
Next step was Republican Calendar; this one was simpler to implement thanks to repubcal [repo]


Two weeks flew by and the code was almost done. We had to wait for a couple of weeks for staff to return from holidays, so we took a break from the project.

Then, the moment of truth: deploying 8 raspberry pi remotely. Kim Gipouloux was a great proxy at Marian Goodman's, she assembled and burned all 8 images onto the SD cards and checked each one.

We only had to apply a small patch a week before opening that contained some texture glitch overlay in a set of particular screens.


It was an incredible fun project, but I'm also honored to be a part of an amazing crew of humans that carried this work throughout completion. Special thanks to Adrian Villar Rojas for his trust and continuos support along the process.

If you're running this on your pi and/or you have any questions don't hesitate to send an email hola@capo.digital 

# Installation
So, apart from the dependencies listed below, you shouldn't need much to get it running. The script should run also on a computer! I tested and configured it in my laptop and then just updated the config file on the raspi via git.

In my case, I had the need for it to run 24/7, headless and self-restart in case of a power outage. If you're looking for something like that, I'm leaving down below all the links that helped me a lot)

## Dependencies

Installed on the raspi via pip:
pygame
pitz
ephem

## Wishlist 

- Performance hits on frame rate when Font is too big, especially in milliseconds.

- Never got to try using ptext OpenGL to test possible performance upgrade.

- There's a cool feature in repubcal that dislays QR code of the Republican Day Wiki page. Would be cool to have one of the screens show it.

- Make a compact layout showing all data in only one screen. 

- The joystick stops sending inputs after a couple of plug/unplugs (cbb joystick detection)

- Set the raspi os to read-only mode

## Resources

- Websites from trello 

## Credits
- repubcal
- decimaltime
- ptext
