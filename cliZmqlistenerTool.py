from zmqTool import ZmqTool
from time import sleep
import threading

zt = ZmqTool()
print("zt initialized.")

ztTread = threading.Thread(target=zt.zmq_rep_thread, daemon=True)
ztTread.start()

while 1:
    print(zt.get_dict_message())
    sleep(0.3)
    print("-----------------------------------")

