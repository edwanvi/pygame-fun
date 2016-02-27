import pygame
import random
from SPRITES.spritesheet_functions import SpriteSheet
from SPRITES import constants, collectables


# Basic boss. subclass to make it your own!
class Boss(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data):
        super().__init__()

        self.change_x = 0
        self.change_y = 0
        self.level = None
        self.player = None
        self.called_times = 0

        #Level information
        self.level = None
        self.player = None

        sprite_sheet = SpriteSheet("boss_sheet.png")
        # we use the same formula as the platforms here: X location of sprite, Y location of sprite, Width of sprite,
        #Height of sprite
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])
        self.rect = self.image.get_rect()

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        #see if we are on the bottom of the screen.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

class GasterBlaster(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.origin_x = 0
        self.origin_y = 0

class BossW1(Boss):
    def __init__(self):
        sprite_sheet_data = ()
        super().__init__(sprite_sheet_data)

    def attack1(self):
        #something something murder the player something something
        print("Starting Fireball Barrage")
        barrage = self.player.health/10
        while barrage >= self.player.health/10:
            run = self.rect.x - self.player.rect.x
            rise = self.rect.y - self.player.rect.y
            flame = collectables.EnemyFire(run, rise, self.player)
            flame.rect.x = self.rect.x
            flame.rect.y = self.rect.y
    #HEY YOUNG BLOOD
    def attack2(self):
        #DOESN'T IT FEEL
        gasterx = self.player.rect.x
        gastery= self.player.y
        gasterxlogic = bool(random.getrandbits(1))
        gasterFaceLeftBool = bool(random.getrandbits(1))
        if gasterFaceLeftBool:
            gasteryDirection = "left"
        else:
            gasteryDirection= "right"
        if gasterxlogic:
            print("BLAST IT")
            return GasterBlaster(gasterx, 0, "up")
        else:
            return GasterBlaster(0, gastery, gasteryDirection)