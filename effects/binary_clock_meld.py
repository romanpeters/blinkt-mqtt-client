from time import localtime, sleep
import blinkt
from . import Effect


class BinaryClockMeld(Effect):
    def __init__(self, brightness, *args, **kwargs):
        super().__init__(brightness)

    def run(self):
        on_value = 64
        
        while self.running:
            t = localtime()
            h, m, s = t.tm_hour, t.tm_min, t.tm_sec

            print("{h}:{m}:{s}".format(h=h, m=m, s=s))

            blinkt.clear()

            # Blink LED 0
            c = on_value * (s % 2)
            blinkt.set_pixel(0, c, c, c)

            for n in range(6):
                # Grab the n'th bit from hour, min and second
                bit_h = (h & (1 << n)) > 0
                bit_m = (m & (1 << n)) > 0
                bit_s = (s & (1 << n)) > 0

                r, g, b = [int(c * on_value) for c in (bit_h, bit_m, bit_s)]

                blinkt.set_pixel(7 - n, r, g, b)

            blinkt.set_brightness(self.brightness)
            blinkt.show()

            sleep(1)




