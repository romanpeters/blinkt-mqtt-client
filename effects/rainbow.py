import colorsys
import time
import blinkt
from . import Effect

class Rainbow(Effect):
    def __init__(self, brightness, *args, **kwargs):
        super().__init__(brightness)

    def run(self):
        spacing = 360.0 / 16.0

        while self.running:
            hue = int(time.time() * 100) % 360
            for x in range(blinkt.NUM_PIXELS):
                offset = x * spacing
                h = ((hue + offset) % 360) / 360.0
                r, g, b = [int(c*255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
                blinkt.set_pixel(x, r, g, b)

            blinkt.show()
            time.sleep(0.001)
