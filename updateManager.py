from zmqTool import ZmqTool
from time import sleep

class UpdateManager:
    def __init__(self):
        self.zt = ZmqTool()

    def update(self):
        while True:
            self.current_app = self.zt.listen_message("/app/current")
            self.showTopbar = self.zt.listen_message("/app/showTopbar")

            if self.current_app == "draw_spotifyApp":
                self.zt.publish_message("/spotipy/playback/trackname", "update")
                self.zt.publish_message("/spotipy/playback/progress", "update")
                self.zt.publish_message("/spotipy/playback/total_duration", "update")

            if self.showTopbar == "true":
                self.zt.publish_message("/ups/voltage", "update")
                self.zt.publish_message("/ups/power", "update")
            
            sleep(2)

