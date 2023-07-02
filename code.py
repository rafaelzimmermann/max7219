# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import digitalio
from libs import matrices


# You may need to change the chip select pin depending on your wiring
spi =  busio.SPI(clock=board.GP18, MOSI=board.GP19)
cs = digitalio.DigitalInOut(board.GP17)
matrix = matrices.CustomMatrix(width=32, height=8, spi=spi, cs=cs)
while True:
    print("Cycle start")
    # all lit up
    matrix.fill(True)
    matrix.show()
    time.sleep(0.5)

    # all off
    matrix.fill(False)
    matrix.show()
    time.sleep(0.5)

    # one column of leds lit
    for i in range(8):
        matrix.pixel(1, i, 1)
    matrix.show()
    time.sleep(0.5)
    # now scroll the column to the right
    for j in range(32):
        matrix.scroll(1, 0)
        matrix.show()
        time.sleep(0.1)

    adafruit = "test"

    # # scroll a string across the display
    for pixel_position in range(len(adafruit) * 8):
        matrix.fill(0)
        matrix.text(adafruit, -pixel_position, 0)
        matrix.show()
        time.sleep(0.25)