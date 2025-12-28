#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
from PIL import Image, ImageDraw
from demo_opts import get_device

CELL_SIZE = 6
MAX_BRIGHT = 12
SPAWN_PER_FRAME = 2   # ridotto da 3
FRAME_DELAY = 0.08


def main():
    device = get_device()
    w, h = device.width, device.height

    cols = w // CELL_SIZE
    rows = h // CELL_SIZE

    # grid[x][y] = [brightness, phase]
    grid = [[None for _ in range(rows)] for _ in range(cols)]

    image = Image.new("1", (w, h))
    draw = ImageDraw.Draw(image)

    frame = 0

    try:
        while True:
            draw.rectangle(device.bounding_box, fill=0)

            for x in range(cols):
                for y in range(rows):
                    cell = grid[x][y]
                    if cell:
                        b, phase = cell
                        if b > 0:
                            if b > ((frame + phase) % MAX_BRIGHT):
                                px = x * CELL_SIZE
                                py = y * CELL_SIZE
                                draw.rectangle(
                                    (px, py,
                                     px + CELL_SIZE - 1,
                                     py + CELL_SIZE - 1),
                                    fill=1
                                )
                            grid[x][y][0] -= 1
                        else:
                            grid[x][y] = None

            # spawn nuove gocce (desincronizzate)
            for _ in range(SPAWN_PER_FRAME):
                x = random.randrange(cols)
                y = random.randrange(rows)
                grid[x][y] = [MAX_BRIGHT, random.randrange(MAX_BRIGHT)]

            device.display(image)
            frame += 1
            time.sleep(FRAME_DELAY)
    except KeyboardInterrupt:
        # pulizia immediata e uscita pulita
        device.clear()

if __name__ == "__main__":
    main()

