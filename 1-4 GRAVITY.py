import pygame
import time

#All hail the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#Screen sizes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    #Can I just import this?
    def __init__(self):
        super().__init__()

        #Create an image of a red SQUARE
        width = 40
        height = 40
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        #We need to tell pygame about the image we had it make.
        self.rect = self.image.get_rect()

        #Speed variables
        self.change_x = 0
        self.change_y = 0

        #What can we hit?
        self.level = None

    def update(self):
        #Gravity.
        self.calc_grav()

        #It moves to the left it moves to the right
        self.rect.x += self.change_x

        #The devil itself, collision
        block_hit_list = pygame.sprite.spritecollide(self,self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            #STOP! PLAYER!
            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        #Make the edge of the screen a wall as well
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            #We subtract our height because moving ourself moves based on the TOP LEFT CORNER
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        #Move down a bit so see if we have something to jump off of.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        #Jump if you can!
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        #Do I really have to tell you this?
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

    def stop(self):
        #Stop left and right motion
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    player = None

    level = None

    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """

        # Move left/right
        self.rect.x += self.change_x

        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.

            # Reset our position based on the top/bottom of the object.
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


class Level(object):
    # A generic level class, use its children to make levels
    def __init__(self, player):
        #Constructor, pass in a player please. Moving platforms
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        #BG Image
        self.background = None
        #How far we've come in the world of scrolling.
        self.world_shift = 0
        self.level_limit = -1000

    def update(self):
        #Update things.
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        #Draw a level
        screen.fill(BLUE)
        #Draw the sprites
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        #As we move, we need to scroll along with the player.
        self.world_shift += shift_x

        #Go through all the lists and render as needed
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
#WORLD 1-1
class Level_01(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -1500
        #An array of parameters of platforms
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]
        #Add the platforms from the list
        for platform in level:
            block = Platform(platform[0],platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

        #Add a moving platform.
        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
#WORLD 1-2
class Level_02(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -1000
        level = [[210, 70, 500, 550],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 ]
        #Add the platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        #Do we want another moving platform? Heck yes!
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


def main():
    #Main Program.
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('1-4 GRAVITY')
    #Make a player
    player = Player()
    #Create ALL THE LEVELS
    level_list =[]
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))

    #Set the current level, similar to the ROOMS
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
    #Loop until the player ends the game
    done = False

    #Manage the speed of "time"
    clock = pygame.time.Clock()

    #----------- MAIN PROGRAMATIC LOOP -----------#
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop()
                if event.key == pygame.K_RIGHT:
                    player.stop()
        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()
        #Scrolling
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)

        #End the level and move on at the goal
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no < len(level_list)-1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                #END THE GAME IN THE MOST ELABORATE FREAKING WAY POSSIBLE
                done = True
        #Keeping the player away from the edges
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
        elif player.rect.left < 0:
            player.rect.left = 0

        #ALL DRAWING BELOW THIS LINE

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        #ALL DRAWING ABOVE THIS LINE

        #60 FPS cap
        clock.tick(60)

        #Did you notice that everything was upside-down? OF COURSE NOT!
        pygame.display.flip()
    pygame.quit()
if __name__ == "__main__":
    main()