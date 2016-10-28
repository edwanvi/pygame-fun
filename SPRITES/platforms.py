# Platforms you can jump off of, what did you expect

import pygame
from spritesheet_functions import SpriteSheet

# To define a type of platform, we use the formula
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite
GRASS = (0, 0, 70, 70)
STONE = (71, 0, 70, 70)
OBSIDIAN = (142, 71, 70, 70)


class Platform(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_data):
        super().__init__()

        sprite_sheet = SpriteSheet("platform_sheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    #SO YOU MEAN TO TELL ME
    #THIS ONE MOVES?!
    def __init__(self, sprite_sheet_data):

        super().__init__(sprite_sheet_data)

        self.change_x = 0
        self.change_y = 0

        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0

        self.level = None
        self.player = None

    def update(self):
        #DON'T PUSH A PLAYER INTO AN OBSTACLE

        #LEFT AND RIGHT
        self.rect.x += self.change_x

        #See if we hit the player and shove 'em around
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        self.rect.y += self.change_y
        #Shoving players!
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
