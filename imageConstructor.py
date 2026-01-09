from display import Display
from PIL import Image
from zmqTool import ZmqTool


class ImageConstructor:
    def __init__(self):
        self.display = Display()
        self.zt = ZmqTool()
        self.oled_width = 128
        self.oled_height = 64
        self.current_app = "draw_current_time"

    
    def drawImage(self, layers): # type: ignore
        base = Image.new("1", (self.oled_width, self.oled_height), 0)
        for layer in layers:
            base = Image.composite(layer, base, layer)
        return base

    def construct_image(self):
        # Use the Display class to create an image with "TEST" written on it
        self.showTopbar = self.zt.listen_message("/app/showTopbar")
        self.current_app = self.zt.listen_message("/app/current")

        if self.showTopbar == "true":
            draw_topbar = self.display.draw_topbar()
        else:
            draw_topbar = None

        if self.current_app == "draw_spotifyApp":
            draw_app = self.display.draw_spotifyApp
        else:
            draw_app = self.display.draw_current_time

        if draw_app and draw_topbar:
            img = self.drawImage([
                                self.display.draw_topbar(),
                                draw_app(),
                                ])
            return img
        elif draw_app:
            img = self.drawImage([
                                draw_app(),
                                ])
            return img
        elif draw_topbar:
            img = self.drawImage([
                                self.display.draw_topbar(),
                                ])
            return img
        else:
            img = self.display.draw_current_time()
            return img

