# will be executed on the Raspberry Pi

import adafruit_ssd1306
import board, busio
from time import sleep
from imageConstructor import ImageConstructor
import threading
from zmqTool import ZmqTool
from updateManager import UpdateManager
from spotifyTools import SpotifyTool
from upsTools import UpsTools


i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.show()

image_constructor = ImageConstructor()

zt = ZmqTool()
um = UpdateManager()
st = SpotifyTool()
ut = UpsTools()

ztTread = threading.Thread(target=zt.zmq_rep_thread, daemon=True)
ztTread.start()

umTread = threading.Thread(target=um.update, daemon=True)
umTread.start()

stTread = threading.Thread(target=st.zmq_manager_thread, daemon=True)
stTread.start()

utTread = threading.Thread(target=ut.update, daemon=True)
utTread.start()

while True:
    oled.fill(0)
    oled.image(image_constructor.construct_image())
    oled.show()
    sleep(1)
