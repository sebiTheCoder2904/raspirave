import PIL
from PIL import ImageDraw, ImageFont, Image


class Display:
    def __init__(self):
        self.oled_width = 128
        self.oled_height = 64
        self.img = Image.new('1', (128, 64), color=1)  # 1 for 1-bit pixels, black and white
        self.font = ImageFont.truetype("assets/W95FA.otf", 14)
        self.font_large = ImageFont.truetype("assets/W95FA.otf", 35)

        from spotifyApp import SpotifyApp
        self.spotify_app = SpotifyApp()

        from topbar import TopBar
        self.topbar = TopBar()

    def update_display(self, new_image):
        # Update the display with a new image
        self.img.paste(new_image)

    def clear_display(self):
        # Clear the display
        draw = ImageDraw.Draw(self.img)
        draw.rectangle((0, 0, 128, 64), fill=0)  # Fill with white

    def get_image(self):
        return self.img

    def draw_TEST(self):    # make it return a image with TEST written on it
        img = Image.new('1', (128, 64), color=0)  # 1 for 1-bit pixels, black and white
        draw = ImageDraw.Draw(img)
        draw.text((32, 24), "TEST", font=self.font_large, fill=1)
        return img

    def draw_current_time(self):
        from osTools import OSTool
        os_tool = OSTool()
        time_string = os_tool.get_current_time_string()
        img = Image.new('1', (128, 64), color=0)  # 1 for 1-bit pixels, black and white
        draw = ImageDraw.Draw(img)

        text_size = self.font_large.getbbox(time_string)
        text_width = text_size[2] - text_size[0]
        text_height = text_size[3] - text_size[1]

        text = draw.text((self.oled_width/2, self.oled_height/2), time_string, font=self.font_large, fill=1, anchor="mm")
        return img

    def draw_topbar(self):
        topbar_image = self.topbar.draw_topbar()
        return topbar_image

    def draw_spotifyApp(self):
        spotify_image = self.spotify_app.draw_spotifyApp()
        return spotify_image
        
