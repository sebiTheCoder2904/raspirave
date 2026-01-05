from spotifyTools import SpotifyTool
from time import sleep
import threading
from zmqTool import ZmqTool

zt = ZmqTool()

st = SpotifyTool()



stTread = threading.Thread(target=st.zmq_manager_thread, daemon=True)
stTread.start()

sleep(0.1)  # Allow time for thread to start

from zmqTool import ZmqTool
zt = ZmqTool()

zt.publish_message(st.topic_playback, "update")
while zt.listen_message(st.topic_playback) == "update":
    pass

print(zt.listen_message(st.topic_playback))

