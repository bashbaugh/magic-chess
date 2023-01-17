"""Blinky things
Classes to control the LEDs on the chessboard
"""

# Uses rpi_ws281x-python
# Example code at
# https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/examples/strandtest.py

from time import sleep
import rpi_ws281x as neopixel
from rpi_ws281x import Color
from threading import Thread

colors = {'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (30, 0, 255), 'off': (0, 0, 0), 'violet': (150, 0, 105), 'light_orange': (159, 96, 0)}

class Neopixel_RGB_LEDs:
    """Neopixel ws281x addressable RGB led controller
    """
    LED_COUNT = 2
    BLACK_SIDE_LED = 0 # Switch this with WHITE_SIDE_LED if the colors are backwards
    WHITE_SIDE_LED = 1
    LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 50    # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    CONVERT_RGB_TO_GRB = True # Changes RGB format to GRB. Set this to false if your leds' colors are messed up.

    def __init__(self, log_warning):
        self.stop_rainbow = True
        
        self.log_warning = log_warning
        
        self.strip = neopixel.Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS, self.LED_CHANNEL)
        
        self.strip.begin()
        
        self.color('off')
    
    def shutdown(self):
        self.stop_rainbow = True
        self.color('off')
        
    def colorWipe(self, color, wait_ms=10):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            sleep(wait_ms/1000.0)
            
    def color(self, c_name, led=False):
        self.stop_rainbow = True
        # Change RGB to GRB if needed:
        color = Color(*colors[c_name]) if not self.CONVERT_RGB_TO_GRB else Color(colors[c_name][1], colors[c_name][0], colors[c_name][2])
        try:
            if led:
                self.strip.setPixelColor(led, color)
                self.strip.show()
            else:
                self.colorWipe(color)
        except KeyError:
            self.log_warning("Color name not found: {}".format(c_name))
    
    def colorBW(self, black, white):
        self.color(black, self.BLACK_SIDE_LED)
        self.color(white, self.WHITE_SIDE_LED)
    
    @staticmethod
    def wheel(pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
    
    def _rainbow(self, wait_ms=20):
        """Draw rainbow that fades across all pixels at once."""
        while True:
            for j in range(256):
                if self.stop_rainbow:
                    return
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, self.wheel((i+j) & 255))
                self.strip.show()
                sleep(wait_ms/1000.0)

    def rainbow(self, wait_ms=20):
        self.stop_rainbow = False
        rainbow_thread = Thread(target=lambda: self._rainbow(wait_ms))
        rainbow_thread.start()
