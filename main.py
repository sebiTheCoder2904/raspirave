# this will get execute
from pygamelauncher import PygameLauncher
import threading
from zmqTool import ZmqTool
from updateManager import UpdateManager
from spotifyTools import SpotifyTool
from upsTools import UpsTools

pl = PygameLauncher()
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


if __name__ == "__main__":
    pl.run()
