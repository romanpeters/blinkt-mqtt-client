import math
import time
import colorsys
import blinkt
from . import Effect

FALLOFF = 1.9
SCAN_SPEED = 4
start_time = time.time()

class LarsonHue(Effect):
    def __init__(self, brightness, *args, **kwargs):
        super().__init__(brightness)

    def run(self):

        while self.running:
            delta = (time.time() - start_time)

            # Offset is a sine wave derived from the time delta
            # we use this to animate both the hue and larson scan
            # so they are kept in sync with each other
            offset = (math.sin(delta * SCAN_SPEED) + 1) / 2

            # Use offset to pick the right colour from the hue wheel
            hue = int(round(offset * 360))

            # Maximum number basex on NUM_PIXELS
            max_val = blinkt.NUM_PIXELS - 1

            # Now we generate a value from 0 to max_val
            offset = int(round(offset * max_val))

            for x in range(blinkt.NUM_PIXELS):
                sat = 1.0

                val = max_val - (abs(offset - x) * FALLOFF)
                val /= float(max_val) # Convert to 0.0 to 1.0
                val = max(val,0.0) # Ditch negative values

                xhue = hue # Grab hue for this pixel
                xhue += (1-val) * 10 # Use the val offset to give a slight colour trail variation
                xhue %= 360 # Clamp to 0-359
                xhue /= 360.0 # Convert to 0.0 to 1.0

                r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(xhue, sat, val)]

                blinkt.set_pixel(x, r, g, b, val /4)

            blinkt.set_brightness(self.brightness)
            blinkt.show()

            time.sleep(0.001)








