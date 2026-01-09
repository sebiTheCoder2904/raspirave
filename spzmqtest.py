from spotifyTools import SpotifyTool
from time import sleep
import threading
from zmqTool import ZmqTool

zt = ZmqTool()

st = SpotifyTool()



stTread = threading.Thread(target=st.zmq_manager_thread, daemon=True)
stTread.start()


from zmqTool import ZmqTool
zt = ZmqTool()

while True:
    zt.publish_message("/spotipy/playback/trackname", "update")
    zt.publish_message("/spotipy/playback/progress", "update")
    zt.publish_message("/spotipy/playback/total_duration", "update")
    while zt.listen_message("/spotipy/playback/trackname") == "update":
        pass
    
    print(zt.listen_message("/spotipy/playback/trackname"))

    sleep(2)

