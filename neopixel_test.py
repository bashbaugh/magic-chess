# Can be used to test LED colors

# NOTE: SOME LEDs are GRB instead of RGB

COLOR = (150, 50, 100)

CONVERT_RGB_TO_GRB = True

RAINBOW = True


import time
from rpi_ws281x import *

# Change RGB to GRB if needed:
color = Color(*COLOR) if not CONVERT_RGB_TO_GRB else Color(COLOR[1], COLOR[0], COLOR[2])


# LED strip configuration:
LED_COUNT      = 2     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 80     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        print(pos * 3, 255 - pos * 3, 0)
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        print(255 - pos * 3, 0, pos * 3)
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        print(0, pos * 3, 255 - pos * 3)
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    try:
        colorWipe(strip, color)
        while True:
            if RAINBOW:
                rainbow(strip)
            time.sleep(1)
    finally:
        if not RAINBOW:
            colorWipe(strip, Color(0,0,0), 10)