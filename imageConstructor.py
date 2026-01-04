from display import Display

class ImageConstructor:
    def __init__(self):
        self.display = Display()

    def construct_image(self):
        # Use the Display class to create an image with "TEST" written on it
        image = self.display.draw_current_time()
        return image
