import pygame
# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# The Player. Without a player, what is a game?


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def changespeed(self, x, y):
        # WHAT DO YOU THINK THIS DOES YOU TWAT?
        # keff keff. It changes the player's speed.
        self.change_x += x
        self.change_y += y

    def update(self):
        # Update player position.
        # Move left/right
        self.rect.x += self.change_x

        # Did we run into a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Keep that player OUT!
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
        # Same thing for up and down, now we only have one variable to mess with
        self.rect.y += self.change_y

        # NOW did we run into a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Please leave the premises.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom


class Wall(pygame.sprite.Sprite):
    # Defines a wall. I mean what else can this do?
    def __init__(self, x, y, width, height):
        # Construction.
        super().__init__()
        # Make it blue, and not invisible
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        # Make the top left corner where we "center" the thing
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # That was easy. Most of the work is done by the player and not the walls.


# Initialize pygame
pygame.init()
# Create the pygame window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
# This line is fairly self explanitory...
pygame.display.set_caption('1-2 WALLS')
# Make a list of all the sprites, a census.
all_sprite_list = pygame.sprite.Group()
# Now we build our walls.
wall_list = pygame.sprite.Group()
# Each wall follows a format to be created
# You can copy-paste this over and over till you're happy
# Define a wall @ x, y, x2, y2
wall = Wall(0, 0, 10, 600)
# Put it in the appropirate lists
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10, 0, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(10, 200, 100, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

# Spawn a player at x 50 y 50.
player = Player(50, 50)
player.walls = wall_list

all_sprite_list.add(player)
# Start the clock
clock = pygame.time.Clock()

done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

    # Update our census
    all_sprite_list.update()

    screen.fill(BLACK)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()
