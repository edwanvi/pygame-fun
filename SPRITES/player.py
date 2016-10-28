#This file holds the player class
import pygame
import constants, spritesheet_functions, collectables
from platforms import MovingPlatform


class Player(pygame.sprite.Sprite):
    def __init__(self):
        #Call the sprite constructor
        super().__init__()
        # -- Attributes
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        #Smart things. Killed enemies and gathered mana
        self.killed_enemies = 0
        self.mana = 100
        self.health = 100
        # This holds all the images for the animated walk left/right
        # of our player
        self.walking_frames_l = []
        self.walking_frames_r = []
        #Direction of player
        self.direction = "R"
        #Frames of walking animation, RIGHT FACE!
        sprite_sheet = spritesheet_functions.SpriteSheet("player.png")
        image = sprite_sheet.get_image(18, 9, 35, 52)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(88, 11, 35, 50)
        self.walking_frames_r.append(image)

        #LEFT FACE!
        image = sprite_sheet.get_image(18, 9, 35, 52)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(88, 11, 35, 50)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        #starting frame
        self.image = self.walking_frames_r[0]
        #Set player hitbox
        self.rect = self.image.get_rect()

    def update(self):
        #Gravity, a bad movie so I hear
        self.calc_grav()
        #Motion.
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]
        #See if we hit anything and handle it
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
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
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
        #See if we hit an enemy, and subtract some health
        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, True)
        for enemy in enemy_hit_list:
            self.health -= 10
        health_gained = pygame.sprite.spritecollide(self, self.level.health_drops, True)
        for heal in health_gained:
            if self.health < 100:
                self.health += 10

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        #see if we are on the bottom of the screen.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self):
        #Called when you, well, jump
        #make sure we have something to jump off of
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -10
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
        self.direction = "L"

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
        self.direction = "R"

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

    def attack(self):
        if self.direction == "R" and self.mana > 0:
            return collectables.Fireball(1, 0, self)
        elif self.mana > 0:
            return collectables.Fireball(-1, 0, self)
