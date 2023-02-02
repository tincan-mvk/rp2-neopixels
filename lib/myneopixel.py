from machine import Pin
from neopixel import NeoPixel

class MyNeoPixel(object):
    """
    Delegation of neopixel.py
    """
    def __init__(self, outputPin: Pin=Pin(0), numOfPixels: int=3, breakPin=None) -> None:
        """
        create delegation object with NeoPixel member variable and others
        """
        self.np = NeoPixel(outputPin, numOfPixels, bpp=3, timing=1)
        self.pixels = []
        if breakPin != None:
            self.breakPin = Pin(breakPin, Pin.IN)
        else:
            self.breakPin = None
        self.brightness = 100
        self.segments = []
        self.IGNORE_PIXEL_BRIGHTNESS = 999
        self.pixel_brightness = [ self.IGNORE_PIXEL_BRIGHTNESS for i in range(len(self.np)) ]
        self.sync_pixels()

    def sync_np(self):
        """
        tranfer intern list to NeoPixel-list
        """
        brightness = 0
        for idx in range (len(self.pixels)):
            r, g, b = self.get_color_pixel(idx)
            if self.pixel_brightness[idx] != self.brightness and self.pixel_brightness[idx] != self.IGNORE_PIXEL_BRIGHTNESS:
                brightness = self.pixel_brightness[idx]
            else:
                brightness = self.brightness

            r = int( r * ( brightness / 100 ))
            g = int( g * ( brightness / 100 ))
            b = int( b * ( brightness / 100 ))
            self.np[idx] = (r, g, b)

    def show(self):
        """
        produce output via NeoPixel
        """
        self.sync_np()
        self.np.write()
    
    def sync_pixels(self):
        """
        re-write intern list from NeoPixel-list
        """
        self.pixels = []
        for i in range (len(self.np)):
            self.pixels.append(self.np[i])

    def set_brightness(self, brightness=None):
        """
        set global brightness
        """
        if brightness == None:
            pass
        else:
            self.brightness = brightness

    def set_pixel_brightness(self, idx: int, brightness: int=999):
        """
        set brightness for single pixel, initial brightness value resets pixel brightness (999)
        """
        self.pixel_brightness[idx] = brightness

    def reset_pixel_brightness(self):
        """
        set brightness for single pixel
        """
        self.pixel_brightness = []
        self.pixel_brightness = [ self.IGNORE_PIXEL_BRIGHTNESS for i in range(len(self.np)) ]

    def set_pixel(self, idx: int, color: tuple):
        """
        set pixel value in intern list
        """
        self.pixels[idx] = color

    def set_pixel_line(self, idx1: int, idx2: int, color: tuple):
        """
        set value for row of pixels in intern list
        """
        for i in range(idx1, idx2+1):
            self.set_pixel(i, color)

    def fill(self, color: tuple):
        """
        set value for whole led strip in intern list
        """
        self.set_pixel_line(0, len(self.np)-1, color)

    def get_color_pixel(self, idx: int):
        """
        get value of single pixel in intern list
        """
        r, g, b = self.pixels[idx]
        return (r, g, b)

    def shift_right(self, step: int=1):
        """
        shift intern list for rotation right(up)
        """
        self.pixels = self.pixels[-step:] + self.pixels[:-step]

    def shift_left(self, step: int=1):
        """
        shift intern list for rotation left(down)
        """
        self.pixels = self.pixels[step:] + self.pixels[:step]
    
    def stop(self):
        """
        read metering value of exit Pin
        """
        if self.breakPin != None:
            return self.breakPin.value()
        else:
            return False
    
    def add_segment(self, segment: tuple):
        """ 
        add segment to member variable segment-list
        segment = (index_from: int, index_to: int, color_tuple: tuple)
        color_tuple ((r: int,g: int,b: int))
        """
        self.segments.append(segment)

    def set_segment(self, idx: int, color_def: tuple):
        """
        set color definition of segment by index
        """
        idx_from, idx_to, pix_def = self.segments[idx]
        self.segments[idx] = (idx_from, idx_to, color_def)

    def get_segment(self, idx: int):
        """
        get segment from member varaibe segement-list
        """
        idx_from, idx_to, pix_def = self.segments[idx]
        return idx_from, idx_to, pix_def
    
    def clear_segment(self, idx: int, default_color: tuple=(0,0,0)):
        """
        reset segment to "black" or any color by index
        """
        idx_from, idx_to, pix_def = self.segments[idx]
        new_def = []
        for i in range(len(pix_def)):
            new_def.append(default_color)
        self.segments[idx] = (idx_from, idx_to, new_def)

    def apply_segments(self):
        """
        apply all segment definitions to pixels of strip
        """
        for idx_from, idx_to, pix_def in self.segments:
            color_pattern_idx = 0
            for i in range(idx_from, idx_to+1):
                self.set_pixel(i,pix_def[color_pattern_idx])
                color_pattern_idx += 1

    def shift_segment_right(self, idx: int, steps: int=1):
        """
        shift inner list of segment by index for rotation right(up) 
        """
        idx_from, idx_to, pix_def = self.segments[idx]
        pix_def = pix_def[-steps:] + pix_def[:-steps]
        self.segments[idx] = (idx_from, idx_to, pix_def)

    def shift_segment_left(self, idx: int, steps: int=1):
        """
        shift inner list of segment by index for rotation left(down)
        """
        idx_from, idx_to, pix_def = self.segments[idx]
        pix_def = pix_def[steps:] + pix_def[:steps]
        self.segments[idx] = (idx_from, idx_to, pix_def)

    def shift_segment_right_out(self, idx: int, default_color: tuple=(0,0,0), steps: int=1):
        """
        shift inner list of segment by index without rotation right(up)
        """
        idx_from, idx_to, pix_def = self.segments[idx]
        pix_def[len(pix_def)-steps] = default_color
        pix_def = pix_def[-steps:] + pix_def[:-steps]
        self.segments[idx] = (idx_from, idx_to, pix_def)

    def shift_segment_left_out(self, idx: int, default_color: tuple=(0,0,0), steps: int=1):
        """
        shift inner list of segment by index without rotation left(down)
        """
        idx_from, idx_to, pix_def = self.segments[idx]
        pix_def[0] = default_color
        pix_def = pix_def[steps:] + pix_def[:steps]
        self.segments[idx] = (idx_from, idx_to, pix_def)

    def shift_all_segments_right(self):
        """
        shift all segments on strip to right(up)
        """
        temp_segments = []
        temp_segments = self.segments[:]

        for seg_idx in range(len(self.segments)):
            print(seg_idx)
            if seg_idx == len(self.segments)-1:
                next_idx = 0
            else:
                next_idx = seg_idx + 1
            print(next_idx)
            idx_from, idx_to, pix_def = temp_segments[seg_idx]
            self.set_segment(next_idx, pix_def)

    def shift_all_segments_left(self):
        """
        shift all segments on strip to left(down)
        """
        temp_segments = []
        temp_segments = self.segments[:]

        for seg_idx in range(len(self.segments)):
            print(seg_idx)
            if seg_idx == 0:
                next_idx = len(self.segments)-1
            else:
                next_idx = seg_idx - 1
            print(next_idx)
            idx_from, idx_to, pix_def = temp_segments[seg_idx]
            self.set_segment(next_idx, pix_def)