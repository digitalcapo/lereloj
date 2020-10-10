# leReloj.py

## Description
Raspberry Pi Zero W powered PyGame script that displays decimal time and Republican Calendar using Local Timezone.

Made in collaboration with Adrian Villar Rojas for the exhibition [La Fin de'l Imagination](https://www.mariangoodman.com/exhibitions/adrian-villar-rojas-la-fin-de-limagination-paris/)

## Journal

The goal was simple, the task at hand... not so much: 

8 screens, 4 displaying the current year, month, day, season in the [French Republican Calendar](https://en.wikipedia.org/wiki/French_Republican_calendar) format.

The other 4 would display hours, minutes, seconds and milliseconds.

There were some initial obstacles that needed to be addressed for this to work:
- How to get sync between the screens and current time without breaking the bank? If you do it on video loops, they should be broadcasted from a video switcher, and that alone is really expensive / hard to setup.
- I'm based on Argentina and the exhibition is in Paris. Add 'covid-19' to the equation, so travel over for a couple of weeks was not the ideal scenario. It needed to be something *replicable* on the other side, but simple enough to be setup by regular staff from the gallery.

Soon enough, the Raspberry Pi Zero W came to answer all my problems. My idea was to write a script that uses a game engine to display in real-time the actual local time, synced over WiFi using the Network Time Protocol. It would be the same script, but depending on configuration it would change the display type.

This was the first design on paper:



