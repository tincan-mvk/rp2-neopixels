from time import sleep, ticks_ms, ticks_diff
from random import randint
from machine import Pin
import math
from lib.myneopixel import MyNeoPixel
from lib.my_rgb_colors import my_rgb_colors

# Number of NeoPixels - Length of Strip -> numpix
numpix = int(20)
pixel_pin = Pin(0)

strip = MyNeoPixel(pixel_pin, numpix)
delay = 0.08  #delay=0.005

#build hue smooth color length numpix
colors = []

def create_color_pattern(pattern_type: int=0, num_of_pixels: int=numpix, num_of_colors: int=3):
    global colors
    MAX_DEGREES_OF_HSV_COLORWHEEL = 360
    color_maker = my_rgb_colors([])

    if pattern_type == 0:
        hue = float(0.0)
        hue_steps = float(MAX_DEGREES_OF_HSV_COLORWHEEL / num_of_colors)
        for i in range(num_of_colors):
            colors.append(color_maker.colorHSVtoRGB(hue, 1, 0.7))
            hue += hue_steps
            
    if pattern_type == 1:
        HALF_SINUS_CURVE = math.pi
        value = float(0.0)
        value_steps = float(HALF_SINUS_CURVE / num_of_pixels)
        #print(value_steps)
        for i in range(num_of_pixels):
            value = math.sin(i*value_steps)
            colors.append(color_maker.colorHSVtoRGB(0, 1, value))
    else:
        hue = float(0.0)
        hue_steps = float(MAX_DEGREES_OF_HSV_COLORWHEEL / num_of_colors)
        for i in range(num_of_colors):
            colors.append(color_maker.colorHSVtoRGB(hue, 1, 0.7))       

create_color_pattern(0, numpix, 20)
#create_color_pattern(1, numpix)

for idx in range(len(strip.np)):
    strip.set_pixel(0,colors[idx%len(colors)])
    strip.shift_left()

strip.show()
sleep(1)
strip.set_brightness(50)
strip.show()
sleep(1)

count = 0
brightness = int(0)
brightness_steps = float(math.pi / (numpix*4))

while True:

    for i in range(numpix*4):
        brightness = int(math.sin(i*brightness_steps) * 100)
        strip.set_brightness(brightness)
        strip.show()
        sleep(delay)
        strip.shift_right()

