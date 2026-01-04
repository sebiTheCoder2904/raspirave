import PIL
from PIL import ImageDraw, ImageFont, Image


class Display:
    def __init__(self):
        self.img = Image.new('1', (128, 64), color=1)  # 1 for 1-bit pixels, black and white

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
        draw.text((32, 24), "TEST", font=ImageFont.load_default(), fill=1)
        return img

    def draw_current_time(self):
        from osTools import OSTool
        os_tool = OSTool()
        time_string = os_tool.get_current_time_string()
        img = Image.new('1', (128, 64), color=0)  # 1 for 1-bit pixels, black and white
        draw = ImageDraw.Draw(img)


        draw.text((10, 24), time_string, font=ImageFont.load_default(), fill=1)
        return img
        
