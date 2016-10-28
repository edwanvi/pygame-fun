# Space orbit in my space suit

import pygame
import constants

class SpriteSheet(object):
    def __init__(self, file_name):
        # Make the sprite sheet usable for pygame
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        # Creates a single image from a sheet of images
        # We start with nothing, a entirely blank image just the right size for what we need
        image = pygame.Surface([width, height]).convert()
        # Copy from the sheet to the single image
        # sheet, location to copy to, location to copy from
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # We need to change what "transparent" is
        image.set_colorkey(constants.GREY)
        # aaand send it to space. "Orbit. Space orbit. In my spacesuit."
        return image
