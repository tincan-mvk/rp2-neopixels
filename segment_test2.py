from time import sleep
from random import randint
from machine import Pin
from lib.myneopixel import MyNeoPixel
from lib.my_rgb_colors import my_rgb_colors
from lib.rgb_color_palette import rgb_color_palette

# Number of NeoPixels - Length of Strip -> numpix
numpix = int(20)
pixel_pin = Pin(0)

# Pin where NeoPixels are connected
strip = MyNeoPixel(pixel_pin, numpix)

color_maker = my_rgb_colors([])
delay = 0.005  #delay=0.005
turn = 0
shift_steps = 0
MAX_DEGREES_OF_HSV_COLORWHEEL = 360
NUM_OF_COLORS = 20

#build hue smooth color length numpix
colors = []
hue = float(0.0)
hue_steps = float(MAX_DEGREES_OF_HSV_COLORWHEEL / NUM_OF_COLORS)
for i in range(NUM_OF_COLORS):
    colors.append(color_maker.colorHSVtoRGB(hue, 1, 0.5))
    hue += hue_steps

color_pattern20 = [ 

                   rgb_color_palette.ROT,
                   (25,0,0),  
                   (25,0,0), 
                   (25,0,0), 
                   (25,0,0),  
                   (25,0,0), 
                   (25,0,0), 
                   (25,0,0), 
                   (25,0,0), 
                   rgb_color_palette.ROT,
                   rgb_color_palette.ROT,
                   (25,0,0),  
                   (25,0,0), 
                   (25,0,0), 
                   (25,0,0),  
                   (25,0,0), 
                   (25,0,0), 
                   (25,0,0), 
                   (25,0,0), 
                   rgb_color_palette.ROT,
                    ]

strip.fill((20,20,20))
strip.show()
sleep(2)
strip.fill((0,0,0))
strip.show()
sleep(2)
count = 0
color_pattern = []

num_of_segments = 0

num_of_segments = int(numpix/10)
color_pattern = color_pattern20


length_of_segment = int(numpix/num_of_segments)
for i in range(num_of_segments):
    seg_from = int(i*length_of_segment)
    seg_to = int(seg_from+(length_of_segment-1))
    print(seg_from, seg_to)
    strip.add_segment((seg_from,seg_to,color_pattern))

strip.apply_segments()
strip.show()
sleep(1)
direction = 1
bounce = 1

while True:
    
    turn += 1

    if turn%50 == 0:
        new_color = colors[randint(0,len(colors)-1)]
        turn = 0
        for i in range(len(strip.segments)):
            idx_from, idx_to, color_def = strip.get_segment(i)
            for j in range(len(color_def)):
                if j < len(color_def)/2:
                    color_def[j] = new_color
            strip.set_segment(i,color_def)

        strip.apply_segments()
        
    strip.show()
    sleep(0.08)
    count += 1
    if count%length_of_segment == 0 and bounce == 1:
        direction = 1 - direction
        count = 2
    for i in range(len(strip.segments)):
        if i%2 == 0 and direction == 1:
            strip.shift_segment_right(i)
        elif i%2 != 0 and direction == 1:
            strip.shift_segment_left(i)
        elif i%2 == 0 and direction == 0:
            strip.shift_segment_left(i)
        elif i%2 != 0 and direction == 0:
            strip.shift_segment_right(i)

    strip.apply_segments()

