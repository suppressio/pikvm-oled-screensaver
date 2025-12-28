#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
from PIL import Image, ImageDraw
from demo_opts import get_device

NUM_SQUARES = 8
SIZE = 4
FRAME_DELAY = 0.05

class Square:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.x = random.randint(0, w - SIZE)
        self.y = random.randint(0, h - SIZE)
        self.vx = random.choice([-1, 1])
        self.vy = random.choice([-1, 1])

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # rimbalzo sui bordi
        if self.x <= 0 or self.x >= self.w - SIZE:
            self.vx *= -1
        if self.y <= 0 or self.y >= self.h - SIZE:
            self.vy *= -1

    def draw(self, draw_obj):
        draw_obj.rectangle((self.x, self.y, self.x + SIZE, self.y + SIZE), fill=1)

def main():
    device = get_device()
    w, h = device.width, device.height
    squares = [Square(w, h) for _ in range(NUM_SQUARES)]

    try:
        while True:
            image = Image.new("1", (w, h))
            draw = ImageDraw.Draw(image)

            for sq in squares:
                sq.update()
                sq.draw(draw)

            device.display(image)
            time.sleep(FRAME_DELAY)

    except KeyboardInterrupt:
        device.clear()

if __name__ == "__main__":
    main()

