import threading
import blinkt

class Effect(object):
    def __init__(self, brightness=1.0, rgb_color=None):
        self.brightness = brightness
        self.rgb_color = rgb_color
        self.running = True
#        blinkt.clear()
#        blinkt.show()
        blinkt.set_brightness(brightness)

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()
