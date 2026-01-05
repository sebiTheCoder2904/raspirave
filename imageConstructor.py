from display import Display
from PIL import Image

class ImageConstructor:
    def __init__(self):
        self.display = Display()
        self.oled_width = 128
        self.oled_height = 64

    
    def drawImage(self, layers): # type: ignore
        base = Image.new("1", (self.oled_width, self.oled_height), 0)
        for layer in layers:
            base = Image.composite(layer, base, layer)
        return base

    def construct_image(self):
        # Use the Display class to create an image with "TEST" written on it
        img = self.drawImage([
                            self.display.draw_current_time(),
                            self.display.draw_topbar()
                            ])
        return img   

