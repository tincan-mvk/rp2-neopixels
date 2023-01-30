from time import sleep
from random import randint
import math
from machine import Pin
from lib.myneopixel import MyNeoPixel
from lib.my_rgb_colors import my_rgb_colors

# Number of NeoPixels - Length of Strip -> numpix
numpix = int(20)
pixel_pin = Pin(0)

strip = MyNeoPixel(pixel_pin, numpix)

color_maker = my_rgb_colors([])
delay = 0.005
turn = 0
shift_steps = 0
MAX_DEGREES_OF_HSV_COLORWHEEL = 360
NUM_OF_COLORS = numpix

#build hue smooth color length numpix
print("Create colors")
colors = []
hue = float(0.0)
hue_steps = float(MAX_DEGREES_OF_HSV_COLORWHEEL / NUM_OF_COLORS)
for i in range(NUM_OF_COLORS):
    colors.append(color_maker.colorHSVtoRGB(hue, 1, 0.7))
    hue += hue_steps

color_pattern = []

num_of_segments = 2


length_of_segment = int(numpix/num_of_segments)
print("Create segments:",num_of_segments, length_of_segment)
for i in range(num_of_segments):
    color_pattern = []
    seg_from = int(i*length_of_segment)
    seg_to = int(seg_from+(length_of_segment-1))
    print(seg_from, seg_to)
    for i in range(seg_from, seg_to+1):
        color_pattern.append(colors[0])
    print("Length color_pattern",len(color_pattern))
    strip.add_segment((seg_from,seg_to,color_pattern))

strip.apply_segments()
strip.show()
sleep(1)

turn_left = False
color = colors[randint(0,len(colors)-1)]

while True:
    
    turn += 1
    if int(math.floor(turn/numpix))%2 == 0:
        if turn_left == True:
            turn_left = False
            color = colors[randint(0,len(colors)-1)]
        color = colors[randint(0,len(colors)-1)]
        for i in range(len(strip.segments)):
            if i%2 == 0:
                strip.shift_segment_right_out(i, color)
            else:
                strip.shift_segment_left_out(i, color)
                
    else:
        if turn_left == False:
            turn_left = True
            color = colors[randint(0,len(colors)-1)]
        for i in range(len(strip.segments)):
            if i%2 == 0:
                strip.shift_segment_left_out(i, color)
            else:
                strip.shift_segment_right_out(i, color)
    strip.apply_segments()
    strip.show()
    sleep(0.05)
