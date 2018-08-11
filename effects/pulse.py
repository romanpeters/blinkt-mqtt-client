import colorsys
import time
from sys import exit
import numpy as np
import blinkt
from . import Effect


class Pulse(Effect):
    def __init__(self, brightness, rgb_color, *args, **kwargs):
        super().__init__(brightness, rgb_color)

    def make_gaussian(self):
        x = np.arange(0, blinkt.NUM_PIXELS, 1, float)
        y = x[:, np.newaxis]
        x0, y0 = 3.5, 3.5
        gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / self.fwhm ** 2)
        return gauss

    def run(self):
        h, s, v = colorsys.rgb_to_hsv(*self.rgb_color)

        while self.running:
            for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
                self.fwhm = 5.0/z
                gauss = self.make_gaussian()
                start = time.time()
                y = 4
                for x in range(blinkt.NUM_PIXELS):
                    s = 1.0
                    v = gauss[x, y]
                    rgb = colorsys.hsv_to_rgb(h, s, v)
                    r, g, b = [int(255.0 * i) for i in rgb]
                    blinkt.set_pixel(x, r, g, b)

                blinkt.set_brightness(self.brightness)
                blinkt.show()
                end = time.time()
                t = end - start
                if t < 0.04:
                    time.sleep(0.04 - t)




