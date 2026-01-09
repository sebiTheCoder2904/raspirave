from zmqTool import ZmqTool
from time import sleep

zt = ZmqTool()
print("zt initialized.")


while 1:
    print(zt.get_dict_message())
    sleep(0.1)
    print("-----------------------------------")

