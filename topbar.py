import PIL
from PIL import ImageDraw, ImageFont, Image
from zmqTool import ZmqTool

class TopBar:
    def __init__(self):
        self.oled_width = 128
        self.oled_height = 64
        self.font = ImageFont.truetype("assets/W95FA.otf", 14)
        self.voltage = "idk V"  # Example voltage value
        
        from osTools import OSTool
        self.os_tool = OSTool()
        self.time_string = self.os_tool.get_current_time_string()
        self.zt = ZmqTool()

    def draw_topbar(self):
        img = Image.new('1', (128, 64), color=0)  # 1 for 1-bit pixels, black and white
        draw = ImageDraw.Draw(img)

        self.update()

        draw.rounded_rectangle(xy=[0, -20, 127, 12], fill=0, width=1, radius=7, outline="white")
        draw.text((self.oled_width-2, 0), self.voltage, font=self.font, fill=1, anchor="rt")
        draw.text((2, 0), self.time_string, font=self.font, fill=1, anchor="lt")

        return img

    def update(self):
        self.time_string = self.os_tool.get_current_time_string()
        voltage = self.zt.listen_message("/ups/voltage")
        if voltage == "none" or voltage == "update":
            pass
        else:
            self.voltage = voltage
