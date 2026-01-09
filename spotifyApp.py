import PIL
from PIL import ImageDraw, ImageFont, Image
from datetime import timedelta
from zmqTool import ZmqTool

class SpotifyApp:
    def __init__(self):
        self.oled_width = 128
        self.oled_height = 64
        self.font = ImageFont.truetype("assets/W95FA.otf", 14)
        self.font_large = ImageFont.truetype("assets/W95FA.otf", 25)
        
        from osTools import OSTool
        self.ot = OSTool()
        self.time_string = self.ot.get_current_time_string()

        self.zt = ZmqTool()

        self.trackname = "Track Name"
        self.progress_ms = 155
        self.total_duration_ms = 300000
        self.progress_hr = str(timedelta(milliseconds=self.progress_ms))[2:7]
        self.total_duration_hr = str(timedelta(milliseconds=self.total_duration_ms))[2:7] # MM:SS format

    def draw_spotifyApp(self):
        img = Image.new('1', (128, 64), color=0)  # 1 for 1-bit pixels, black and white
        draw = ImageDraw.Draw(img)
        self.update_info()

        if int(self.total_duration_ms) == 0:
            drawlinecoordinate = 0
        else:
            drawlinecoordinate = round((int(self.progress_ms) / int(self.total_duration_ms)) * self.oled_width)

        draw.line((0, self.oled_height-1, drawlinecoordinate, self.oled_height-1), fill=1, width=1)  # spotify playback progress bar

        draw.text((self.oled_width/2, self.oled_height/2), self.trackname, font=self.font_large, fill=1, anchor="mm")
        draw.text((2, self.oled_height-3), self.progress_hr, font=self.font, fill=1, anchor="lb")
        draw.text((self.oled_width-2, self.oled_height-3), self.total_duration_hr, font=self.font, fill=1, anchor="rb")

        return img

    def update_info(self):
        trackname = self.zt.listen_message("/spotipy/playback/trackname")
        progress = self.zt.listen_message("/spotipy/playback/progress")
        total_duration = self.zt.listen_message("/spotipy/playback/total_duration")

        if trackname == "none" or trackname == "update":
            pass
        else:
            self.trackname = trackname

        if total_duration == "none" or total_duration == "update":
            pass
        else:
            self.total_duration_ms = int(total_duration)
            self.total_duration_hr = str(timedelta(milliseconds=int(self.total_duration_ms)))[2:7]


        if progress == "none" or progress == "update":
            pass
        else:
            self.progress_ms = int(progress)
            self.progress_hr = str(timedelta(milliseconds=int(self.progress_ms)))[2:7]

