import pygame
from imageConstructor import ImageConstructor
from time import sleep

class PygameLauncher:
    def __init__(self):
        self.scale_factor = 4
        pygame.init()
        self.screen = pygame.display.set_mode((128*self.scale_factor, 64*self.scale_factor))
        pygame.display.set_caption("Pygame Display Emulator")
        self.image_constructor = ImageConstructor()

    def pil_to_pygame(self, pil_image):
        """Convert a PIL image to a Pygame surface."""
        if pil_image.mode not in ("RGB", "RGBA"):
            pil_image = pil_image.convert("RGBA")

        mode = pil_image.mode
        size = pil_image.size
        data = pil_image.tobytes()

        return pygame.image.fromstring(data, size, mode)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False

            # Construct the test image using ImageConstructor
            image = self.image_constructor.construct_image()

            # Convert PIL image to Pygame surface
            pygame_image = self.pil_to_pygame(image)
            pygame_image = pygame.transform.scale_by(pygame_image, self.scale_factor)

            # Blit the image to the screen
            self.screen.blit(pygame_image, (0, 0))
            pygame.display.flip()

            clock.tick(30)  # Limit to 30 FPS
        pygame.quit()


