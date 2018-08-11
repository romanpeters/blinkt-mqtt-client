import time
import math
import colorsys
import blinkt
from . import Effect


class Larson(Effect):
    def __init__(self, brightness, rgb_color, *args, **kwargs):
        super().__init__(brightness, rgb_color)

    def run(self):
        h, s, v = colorsys.rgb_to_hsv(*self.rgb_color)

        VALUES = [0, 0, 0, 0, 0, 16, 64, 255, 64, 16, 0, 0, 0, 0, 0, 0]

        start_time = time.time()

        RGB = [(colorsys.hsv_to_rgb(h, s, value)) for value in VALUES]

        while self.running:
            # Sine wave, spends a little longer at min/max
            # delta = (time.time() - start_time) * 8
            # offset = int(round(((math.sin(delta) + 1) / 2) * (blinkt.NUM_PIXELS - 1)))

            # Triangle wave, a snappy ping-pong effect
            delta = (time.time() - start_time) * 16
            offset = int(abs((delta % len(VALUES)) - blinkt.NUM_PIXELS))

            for i in range(blinkt.NUM_PIXELS):
                blinkt.set_pixel(i , *RGB[offset + i])

            blinkt.set_brightness(self.brightness)
            blinkt.show()

            time.sleep(0.1)
