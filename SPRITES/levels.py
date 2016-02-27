import pygame
import SPRITES.platforms
import SPRITES.constants
import SPRITES.collectables

class Level:
    #This is a blank level. Use at own risk.
    def __init__(self, player):
        #Meet the construction crew.
        self.platform_list = None
        self.enemy_list = None
        self.boss_list = None
        self.coin_list = None
        self.other_list = None
        self.health_drops = None
        self.mana_drops = None
        #BG Image
        self.background = None

        #World scrolling variables
        self.world_shift = 0
        self.level_limit = -1000
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.other_list = pygame.sprite.Group()
        self.mana_drops = pygame.sprite.Group()
        self.health_drops = pygame.sprite.Group()
        self.player = player

    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        #Draw the background
        #and don't shift it about as much as the level (thus creating depth)
        screen.fill(SPRITES.constants.BLUE)
        screen.blit(self.background,(self.world_shift // 3,0))

        #Draw everything we have to draw (sprites)
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.other_list.draw(screen)
        self.mana_drops.draw(screen)
        self.health_drops.draw(screen)

    def shift_world(self, shift_x):
        #Scroll through everything
        self.world_shift += shift_x

        #Move everything around on the screen
        for platform in self.platform_list:
            platform.rect.x += shift_x
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
        for coin in self.coin_list:
            coin.rect.x += shift_x
        for fire in self.other_list:
            fire.rect.x += shift_x
        for mana in self.mana_drops:
            mana.rect.x += shift_x
        for heal in self.health_drops:
            heal.rect.x += shift_x

#Create World 1-1
class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        #Set background image
        self.background = pygame.image.load("background_01.png").convert()
        self.background.set_colorkey(SPRITES.constants.WHITE)
        self.level_limit = -2500

        level = [
                  [SPRITES.platforms.GRASS, 500, 500],
                  [SPRITES.platforms.GRASS, 570, 500],
                  [SPRITES.platforms.GRASS, 640, 500],
                  [SPRITES.platforms.GRASS, 800, 400],
                  [SPRITES.platforms.GRASS, 870, 400],
                  [SPRITES.platforms.GRASS, 940, 400],
                  [SPRITES.platforms.GRASS, 1000, 500],
                  [SPRITES.platforms.GRASS, 1070, 500],
                  [SPRITES.platforms.GRASS, 1140, 500],
                  [SPRITES.platforms.STONE, 1120, 280],
                  [SPRITES.platforms.STONE, 1190, 280],
                  [SPRITES.platforms.STONE, 1260, 280],
        ]
        #Add platforms from the level list
        for platform in level:
            block = SPRITES.platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)
        #Add a moving platform
        block = SPRITES.platforms.MovingPlatform(SPRITES.platforms.STONE)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        #Add a enemy
        enemy = SPRITES.collectables.Basic_Enemy()
        enemy.rect.x = 570
        enemy.rect.y = 400
        enemy.change_x = -1
        enemy.change_y = 0
        enemy.level = self
        self.enemy_list.add(enemy)
        #add 2 coins
        coin = SPRITES.collectables.Coin()
        coin.rect.x = 400
        coin.rect.y = 280
        self.coin_list.add(coin)
        coin = SPRITES.collectables.Coin()
        coin.rect.x = 1600
        coin.rect.y = 310
        self.coin_list.add(coin)
        #add a mana drop
        mana = SPRITES.collectables.ManaDrop()
        mana.rect.x = 420
        mana.rect.y = 280
        self.mana_drops.add(mana)


#1-2
class Level_02(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.background = pygame.image.load("background_02.png").convert()
        self.background.set_colorkey(SPRITES.constants.WHITE)
        self.level_limit = -1600
        #Define a platform. [type, x, y]
        level = [
                  [SPRITES.platforms.STONE, 500, 550],
                  [SPRITES.platforms.STONE, 570, 550],
                  [SPRITES.platforms.STONE, 640, 550],
                  [SPRITES.platforms.GRASS, 800, 400],
                  [SPRITES.platforms.GRASS, 870, 400],
                  [SPRITES.platforms.GRASS, 940, 400],
                  [SPRITES.platforms.GRASS, 1000, 500],
                  [SPRITES.platforms.GRASS, 1070, 500],
                  [SPRITES.platforms.GRASS, 1140, 500],
                  [SPRITES.platforms.STONE, 1120, 280],
                  [SPRITES.platforms.STONE, 1190, 280],
                  [SPRITES.platforms.STONE, 1260, 280],
        ]
        for platform in level:
            block = SPRITES.platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        #Add a moving platform.
        block = SPRITES.platforms.MovingPlatform(SPRITES.platforms.STONE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
        coin = SPRITES.collectables.Coin()
        coin.rect.x = 400
        coin.rect.y = 280
        self.coin_list.add(coin)
        #Health to heal
        heal = SPRITES.collectables.HPBoost()
        heal.rect.x = 1520
        heal.rect.y = 85
        self.health_drops.add(heal)
        #GHAST GOES SHOOT
        enemy = SPRITES.collectables.GhastlyBlimp()
        enemy.level = self
        enemy.player = self.player
        enemy.rect.x = 1400
        enemy.rect.y = 150
        enemy.change_y = -2
        enemy.change_x = 0
        enemy.direction = 'L'
        enemy.boundary_top = 100
        enemy.boundary_bottom = 550
        self.enemy_list.add(enemy)