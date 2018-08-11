import colorsys
import time
import numpy as np
import blinkt
from . import Effect


class Candle(Effect):
    def __init__(self, brightness, *args, **kwargs):
        super().__init__(brightness)

    def run(self):
        start = 0
        end = 60

        while self.running:
            wait = np.random.choice(np.random.noncentral_chisquare(5, 1, 1000), 1)[0] / 50
            n = np.random.choice(np.random.noncentral_chisquare(5, 0.1, 1000), 1)
            limit = int(n[0])

            if limit > blinkt.NUM_PIXELS:
                limit = blinkt.NUM_PIXELS

            for pixel in range(limit):
                hue = start + (((end - start) / float(blinkt.NUM_PIXELS)) * pixel)
                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue/360.0, 1.0, 1.0)]
                blinkt.set_pixel(pixel, r, g, b)
                blinkt.show()
                time.sleep(0.05 / (pixel + 1))

            time.sleep(wait)
            blinkt.clear()






