# will be executed on the Raspberry Pi

import adafruit_ssd1306
import board, busio
import os
from time import sleep
from imageConstructor import ImageConstructor

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.show()

image_constructor = ImageConstructor()


while True:
    oled.fill(0)
    oled.image(image_constructor.construct_image())
    oled.show()
    sleep(1)
