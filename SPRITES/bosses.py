import pygame
import random
from spritesheet_functions import SpriteSheet
import constants, collectables


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
        #We use the same formula as the platforms here: X location of sprite, Y location of sprite, Width of sprite,
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


class GasterBlast(pygame.sprite.Sprite):
    def __init__(self, x, y, player):
        super().__init__()
        sheet = SpriteSheet("gaster_sheet.png")
        self.image = sheet.get_image()
        self.rect = self.image.get_rect()
        self.updates = 0

    def update(self):
        self.updates += 1
        if self.updates > 85:
            self.kill()


class GasterBlaster(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, player):
        super().__init__()
        sheet = SpriteSheet("gaster_sheet.png")
        self.firing = False
        self.Fired = False

    def update(self):
        if not self.Fired:
            if self.direction == "left":
                #shoot left
                return GasterBlast(self.rect.x + 10, self.rect.y, self.player)
            if self.direction == "right":
                #shoot right
                return GasterBlast(self.rect.x - 10, self.rect.y, self.player)
            if self.direction == "up":
                #shoot up
                return GasterBlast(self.rect.x, self.rect.y + 10, self.player)
            self.Fired = True
        else:
            # die
            self.kill()


class BossW1(Boss):
    def __init__(self, player):
        sprite_sheet_data = ([0, 0, 32, 32])
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

    #Use a gaster blaster on the player
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
            return GasterBlaster(gasterx, 0, "up", self.player)
        elif gasteryDirection == "right":
            print("BLAST IT")
            return GasterBlaster(0, gastery, gasteryDirection, self.player)
        elif gasteryDirection == "left":
            print("BLAST IT")
            return GasterBlaster(850, gastery, gasteryDirection, self.player)
    def Run(self):
        #LIKE OUR TIME IS RUNNING OUT
        attacknumber = random.randint(0, 1)
        if attacknumber == 0:
            self.attack1()
        elif attacknumber == 1:
            self.attack2()
