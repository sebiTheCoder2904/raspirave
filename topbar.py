import PIL
from PIL import ImageDraw, ImageFont, Image

class TopBar:
    def __init__(self):
        self.oled_width = 128
        self.oled_height = 64
        self.font = ImageFont.truetype("assets/W95FA.otf", 14)
        self.voltage = 4.2  # Example voltage value
        
        from osTools import OSTool
        self.os_tool = OSTool()
        self.time_string = self.os_tool.get_current_time_string()

    def draw_topbar(self):
        img = Image.new('1', (128, 64), color=0)  # 1 for 1-bit pixels, black and white
        draw = ImageDraw.Draw(img)

        draw.rounded_rectangle(xy=[0, -20, 127, 12], fill=0, width=1, radius=7, outline="white")

        return img
