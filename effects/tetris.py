import time
from random import randint
import blinkt
from . import Effect

spacing = 360.0 / 16.0
MAX_SIZE = 4
MAX_GRID = blinkt.NUM_PIXELS + MAX_SIZE - 1
OFF = (0, 0, 0)

class Tetris(Effect):
    def __init__(self, brightness, *args, **kwargs):
        super().__init__(brightness)

    def run(self):
        self.grid = [OFF] * (MAX_GRID + 1)
        blinkt.set_brightness(0.1)
        self.place(self.random_tile(MAX_SIZE))
        self.update()

        while self.running:
            time.sleep(0.5)

            if self.has_lines():
                self.blink_lines()
                self.remove_lines()
                self.place(self.random_tile(MAX_SIZE))
            else:
                self.gravity()

            self.update()


    def random_color(self):
        return (randint(0, 255), randint(0, 255), randint(1, 50))

    def random_tile(self, max_size, min_size=1):
        return (randint(min_size, max_size), self.random_color())

    def place(self, tile):
        for i in range(0, tile[0]):
            self.grid[MAX_GRID - i - len(tile)] = tile[1]

    def update(self):
        for i in range(blinkt.NUM_PIXELS):
            blinkt.set_pixel(i, self.grid[i][0], self.grid[i][1], self.grid[i][2])
        blinkt.show()

    def has_lines(self):
        return self.grid[0] != OFF

    def get_lines(self):
        lines = []
        for i, color in enumerate(self.grid):
            if color == OFF:
                return lines
            else:
                lines.append(i)
        return lines

    def blink_lines(self):
        def hide():
            for line in self.get_lines():
                blinkt.set_pixel(line, 0, 0, 0)
            blinkt.show()

        hide()
        time.sleep(0.5)
        self.update()
        time.sleep(0.5)
        hide()
        time.sleep(0.5)

    def remove_lines(self):
        for line in self.get_lines():
            self.grid[line] = OFF

    def gravity(self):
        self.grid.append(OFF)
        self.grid.pop(0)



