#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import math
import random
from demo_opts import get_device
from luma.core.render import canvas


class Orbiter:
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(0.02, 0.08)

    def update(self):
        self.angle += self.speed

    def pos(self):
        x = int(self.cx + math.cos(self.angle) * self.r)
        y = int(self.cy + math.sin(self.angle) * self.r)
        return x, y


def main():
    device = get_device()

    cx = device.width // 2
    cy = device.height // 2

    orbiters = [
        Orbiter(cx, cy, r)
        for r in range(6, min(cx, cy), 6)
    ]

    while True:
        with canvas(device) as draw:
            for o in orbiters:
                o.update()
                x, y = o.pos()
                draw.point((x, y), fill="white")

        time.sleep(0.04)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
