import builtins
from random import randint
from math import floor

class my_rgb_colors(object):
    def __init__(self, colorlist):
        self.data = []
        self.preset_color_list = []
        if len(colorlist) > 0:
            self.set_color_list(colorlist)
        
    def get_random_color(self):
        if len(self.preset_color_list) > 0:
            return self.preset_color_list[randint(1, len(self.preset_color_list) - 1)]
    
    def get_list_of_random_colors(self, num_of_colors):
        color_list = []
        for i in range(num_of_colors):
            color_list.append(self.get_random_color())
        return color_list
    
    def set_color_list(self, colorlist):
        self.preset_color_list = colorlist
        
    def get_color_list(self):
        return self.preset_color_list

    def reset_color_list(self, colorlist):
        self.preset_color_list = []
    
    def get_list_of_similar_colors(self, color, distance):
        color_list = []
        r_1, g_1, b_1 = color
        r1 = int(r_1)
        g1 = int(g_1)
        b1 = int(b_1)
        r1_min = int( r1 - distance )
        r1_max = int( r1 + distance )
        g1_min = int( g1 - distance )
        g1_max = int( g1 + distance )
        b1_min = int( b1 - distance )
        b1_max = int( b1 + distance )
        color_dict_list = self.get_color_list()
        for i in range(len(color_dict_list)):
            r_2, g_2, b_2 = color_dict_list[i]
            r2 = int(r_2)
            g2 = int(g_2)
            b2 = int(b_2)
            #print(r1_min,r2,r1_max,g1_min,g2,g1_max,b1_min,b2,b1_max)
            if (r1_min) < r2 and (r1_max) > r2:
                if (g1_min) < g2 and (g1_max) > g2:
                    if (b1_min) < b2 and (b1_max) > b2:
                        color_list.append(color_dict_list[i])
        return color_list
    
    def build_gradient_pattern_from_two(self, p_color1, p_color2, length_pattern_part):
        pattern = []
        
        if p_color1 == p_color2 or length_pattern_part == 0: return

        right_pixel = length_pattern_part - 1 #max
        left_pixel = 0                    #min
        
        for i in range(right_pixel - left_pixel + 1):
            if i == 0:
                fraction = 0.5 / (right_pixel - left_pixel)
            else:
                fraction = i / (right_pixel - left_pixel)
            red = round(float(p_color2[0] - p_color1[0]) * fraction + float(p_color1[0]))
            green = round(float(p_color2[1] - p_color1[1]) * fraction + float(p_color1[1]))
            blue = round(float(p_color2[2] - p_color1[2]) * fraction + float(p_color1[2]))
            color = [red, green, blue]
            pattern.append(color)
        return pattern
    
    def get_color_from_rgb(self, red = 0, green = 0, blue = 0):
        if red > 255:
            red = 255
        if green > 255:
            green = 255
        if blue > 255:
            blue = 255
        if red < 0:
            red = 0
        if green < 0:
            green = 0
        if blue < 0:
            blue = 0
           
        return red, green, blue
    
    def hex_to_rgb(self, hex_val): #'#4285f4'
        return tuple(int(hex_val.lstrip('#')[ii:ii+2],16) for ii in (0,2,4))
    
    def conv_i0_255_to_f0_1(self, _integer):
        return float( _integer / 255 )

    def conv_f0_1_to_i0_255(self, _float):
        return int( _float * 255 )

    def colorRGBtoHSV(self, r :int, g :int, b :int):
        # r: int 0..255  colorvalue red
        # g: int 0..255  colorvalue green
        # b: int 0..255  colorvalue blue

        hue = 0
        sat = 0
        val = 0
        max = 0
        min = 0

        # rgb_list = []
        # rgb_list.append(r)
        # rgb_list.append(g)
        # rgb_list.append(b)
        # rgb_list.sort()
        # min = rgb_list.pop(0)
        # max = rgb_list.pop(len(rgb_list)-1)

        min = builtins.min(r, g, b)
        max = builtins.max(r, g, b)

        # set brightness
        val = self.conv_i0_255_to_f0_1(max)

        #set degree of HSV colorcircle and saturation
        #decide by max(red, green, blue)
        if r == g and g == b:  #all equal
            hue = 0
            sat = 0
        elif r >= g and r >= b:  #red is max
            hue = 60 * float(( ( g-b ) / ( max-min ) ))
            sat = float(( max-min ) / max )
        elif g >= r and g >= b: #green is max
            hue = 60 * ( 2 + float(( ( b-r ) / ( max-min ) )) )
            sat = float(( max-min ) / max )
        elif b >= r and b >= g: #blue is max
            hue = 60 * ( 4 + float(( ( r-g ) / ( max-min ) )) )
            sat = float(( max-min ) / max )

        return hue, sat, val

    def colorHSVtoRGB(self, hue :float , sat :float, val :float):
        # hue: float 0..360  HSV colorcircle degree
        # sat: float 0..1    Saturation
        # val: float 0..1    Brightness
        
        if sat == 0:
            r = g = b = self.conv_f0_1_to_i0_255(val)
            return r, g, b

        sector = 0
        hue /= 60
        sector = floor(hue)
        factor = hue - sector
        sector = int(sector)

        #funcs for color-values
        p = val * ( 1 - sat )
        q = val * ( 1 - ( sat * factor )) 
        t = val * ( 1 - ( sat * ( 1 - factor )))

        # set rgb-color-values per sector
        if sector == 0:
            r = val
            g = t
            b = p
        elif sector == 1:
            r = q
            g = val
            b = p
        elif sector == 2:
            r = p
            g = val
            b = t
        elif sector == 3:
            r = p
            g = q
            b = val
        elif sector == 4:
            r = t
            g = p
            b = val
        else:
            r = val
            g = p
            b = q

        return self.conv_f0_1_to_i0_255(r), self.conv_f0_1_to_i0_255(g), self.conv_f0_1_to_i0_255(b)