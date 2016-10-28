#CORE FILE FOR GAME
#useless comment

import pygame
import constants, levels
from player import Player
import time

def main():
    pygame.init()
    font = pygame.font.Font(None, 36)
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('1-4 GRAVITY')
    text = pygame.font.Font('C:\Windows\Fonts\Minecraftia.ttf', 20)
    cycles = 0

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    score = 0

    done = False
    game_over = False

    clock = pygame.time.Clock()
    Player.score = 0
    # -------- Main Program Loop -----------
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
                if event.key == pygame.K_SPACE:
                    fire = player.attack()
                    if fire is not None:
                        active_sprite_list.add(fire)
                        current_level.other_list.add(fire)
                        player.mana -= 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop()
                if event.key == pygame.K_RIGHT:
                    player.stop()
        #Coins.
        coin_hit_list = pygame.sprite.spritecollide(player, current_level.coin_list, True)
        for coin in coin_hit_list:
            score += 200
            print(score)
        #mana
        mana_gained = pygame.sprite.spritecollide(player, current_level.mana_drops, True)
        for mana in mana_gained:
            player.mana += 10
            print('Player gained 10 mana for a drop')
        # Update the player.
        active_sprite_list.update()
        score += player.killed_enemies *100
        player.killed_enemies = 0
        if player.health <= 0:
            game_over = True
        # Update items in the level
        cycles += 1
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
                for fire in current_level.other_list:
                    fire.kill()
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                #END THE GAME IN THE MOST ELABORATE FREAKING WAY POSSIBLE
                game_over = True
        #Keeping the player away from the edges
        if player.rect.right > constants.SCREEN_WIDTH:
            player.rect.right = constants.SCREEN_WIDTH
        elif player.rect.left < 0:
            player.rect.left = 0

        #ALL DRAWING BELOW THIS LINE

        current_level.draw(screen)
        current_level.coin_list.draw(screen)
        active_sprite_list.draw(screen)
        textsurf = text.render('Score: ' + str(score), True, constants.WHITE)
        screen.blit(textsurf, [10, 10])
        healthsurf = text.render('HP: ' + str(player.health), True, constants.WHITE)
        screen.blit(healthsurf, [10, 35])
        manasurf = text.render('Mana: ' + str(player.mana), True, constants.WHITE)
        screen.blit(manasurf, [10, 55])
        if game_over:
            screen.fill(constants.BLACK)
            textsurf = text.render('- GG NO RE -', True, constants.WHITE)
            text_rect = textsurf.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(textsurf, [text_x, text_y])
        #ALL DRAWING ABOVE THIS LINE

        #60 FPS cap
        clock.tick(60)

        #Did you notice that everything was upside-down? OF COURSE NOT!
        pygame.display.flip()
    pygame.quit()
if __name__ == "__main__":
    main()
