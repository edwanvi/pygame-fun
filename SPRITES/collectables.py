import pygame
from spritesheet_functions import SpriteSheet
import constants, platforms
import random
import time


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        sprite_sheet = SpriteSheet("platform_sheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(156, 15, 40, 40)
        self.rect = self.image.get_rect()


class Basic_Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.change_x = 0
        self.change_y = 0
        self.frames = []

        self.level = None
        self.player = None
        self.called_times = 0
        self.sheet = SpriteSheet("platform_sheet.png")
        image = self.sheet.get_image(8, 85, 48, 48)
        self.frames.append(image)
        image = pygame.transform.flip(self.frames[0], True, False)
        self.frames.append(image)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        frame = (pos // 30) % len(self.frames)
        self.image = self.frames[frame]
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x = 1
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.change_x = -1
        self.rect.y += self.change_y
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            # Stop our vertical movement
            self.change_y = 0
            if isinstance(block, platforms.MovingPlatform):
                self.rect.x += block.change_x

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        #see if we are on the bottom of the screen.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height


class Fireball(pygame.sprite.Sprite):
    def __init__(self, cx, cy, player):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(constants.RED)
        self.rect = self.image.get_rect()
        self.change_x = cx
        self.change_y = cy
        self.Player = player
        self.level = self.Player.level
        self.rect.y = self.Player.rect.y
        self.rect.x = self.Player.rect.x

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        if len(block_hit_list) > 0:
            self.kill()
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, True)
        for enemy in enemy_hit_list:
            self.Player.killed_enemies += 1
            self.kill()


class ManaDrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet = SpriteSheet("platform_sheet.png")
        self.image = sprite_sheet.get_image(235, 18, 26, 35)
        self.rect = self.image.get_rect()


class HPBoost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        sprite_sheet = SpriteSheet("platform_sheet.png")
        self.image = sprite_sheet.get_image(240, 92, 28, 28)
        self.rect = self.image.get_rect()


class EnemyFire(pygame.sprite.Sprite):
    def __init__(self, cx, cy, player):
        super().__init__()
        sheet = SpriteSheet("enemy_sheet.png")
        self.image = sheet.get_image(0, 208, 48, 48)
        self.rect = self.image.get_rect()
        self.change_x = cx
        self.change_y = cy
        self.player = player
        self.player_g = pygame.sprite.Group()
        self.player_g.add(self.player)
        self.level = self.player.level
        self.rect.y = 0
        self.rect.x = 0

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.kill()
        player_hit_list = pygame.sprite.spritecollide(self, self.player_g, False)
        for player in player_hit_list:
            self.player.health -= 10
            self.kill()


class GhastlyBlimp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #Motion variables
        self.change_x = 0
        self.change_y = 0
        self.boundary_top = 0
        self.boundary_bottom = 0
        self.boundary_left = 0
        self.boundary_right = 0
        #Level information
        self.level = None
        self.player = None
        #How fast this sprite attacks, in number of frames. 5 = every 5 frames
        self.attack_speed = 10
        #How many times updated has been called. reset to zero when it = attack speed
        self.updates = 0
        self.firing = False
        self.fired_ticks = 0
        sheet = SpriteSheet("enemy_sheet.png")
        self.frames_l = []
        self.frames_r = []
        image = sheet.get_image(0, 48, 64, 132)
        self.frames_l.append(image)
        image = sheet.get_image(68, 48, 64, 132)
        self.frames_l.append(image)
        image = pygame.transform.flip(self.frames_l[0], True, False)
        self.frames_r.append(image)
        image = pygame.transform.flip(self.frames_l[1], True, False)
        self.frames_r.append(image)
        self.direction = 'L'
        if self.direction == 'R':
            self.image = self.frames_r[0]
        if self.direction == 'L':
            self.image = self.frames_l[0]
        self.rect = self.image.get_rect()

    def FIRE(self):
        if self.direction == 'L':
            return EnemyFire(-6.5, 0, self.player)
        else:
            return EnemyFire(6.5, 0, self.player)

    def update(self):
        if self.firing:
            self.fired_ticks += 1
        self.updates += 1
        #Move left and right, and check boundaries
        self.rect.x += self.change_x
        if self.change_x <= 0:
            self.direction = 'L'
        elif self.change_x > 0:
            self.direction = 'R'
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
        if self.player.rect.x > self.rect.x:
            self.direction = 'R'
        else:
            self.direction = 'L'
        #Same, for up and down
        self.rect.y += self.change_y
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
        #If we are on the same Y level as the player, FIRE!
        if self.rect.y + 10 > self.player.rect.y and self.rect.y - 10 < self.player.rect.y and self.firing == False:
            if self.direction == 'L':
                self.image = self.frames_l[1]
                self.firing = True
            else:
                self.image = self.frames_r[1]
                self.firing = True
            flame = self.FIRE()
            flame.rect.x = self.rect.x
            flame.rect.y = self.rect.y
            self.level.other_list.add(flame)
            self.level.enemy_list.add(flame)
        if self.fired_ticks == 20 and self.direction == 'L':
            self.image = self.frames_l[0]
            self.firing = False
            self.fired_ticks = 0
        elif self.fired_ticks == 20:
            self.image = self.frames_r[0]
            self.firing = False
            self.fired_ticks = 0
