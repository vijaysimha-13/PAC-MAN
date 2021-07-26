import pygame
from pygame import mixer
import random
from pygame.math import Vector2 as Vec
from Walls import w as wall_list
from pygame.locals import (
    MOUSEBUTTONDOWN,
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_ESCAPE,
    QUIT,
)

# rgb values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (119, 136, 153)
YELLOW = (255, 255, 0)
RED_ORANGE = (255, 69, 0)
LIGHTSEAGREEN = (32, 178, 170)

# Pellets position in Row-Column format starting with 1's (1 to 30 Rows, 1 to 28 Columns)
# Only 1st element in this list represents Power Pellets position
play_again_coins_list = [[[14, 7], [14, 22], [12, 14], [23, 15], [29, 8], [29, 22]], [2, 22], [2, 23], [2, 24], [2, 25],
                         [2, 26], [2, 27], [3, 22], [3, 27], [4, 27], [4, 22], [5, 22], [5, 27], [6, 3], [6, 4], [6, 5],
                         [6, 6], [6, 8], [6, 9], [6, 11], [6, 12], [6, 22], [6, 23], [6, 24], [6, 25], [6, 26], [6, 27],
                         [9, 10], [9, 11], [9, 12], [9, 17], [9, 18], [9, 19], [10, 7], [10, 22], [11, 7], [11, 22],
                         [12, 7], [12, 10], [12, 11], [12, 12], [12, 13], [12, 15], [12, 16], [12, 17], [12, 18],
                         [12, 19], [12, 22], [13, 7], [13, 22], [15, 7], [15, 22], [16, 7], [16, 22], [17, 7], [17, 22],
                         [18, 7], [18, 22], [19, 7], [19, 22], [20, 2], [20, 8], [20, 9], [20, 10], [20, 11],
                         [20, 12], [20, 17], [20, 18], [20, 19], [20, 20], [20, 21], [20, 27], [21, 2], [21, 27],
                         [22, 2], [22, 27], [23, 2], [23, 27], [23, 11], [23, 12], [23, 13], [23, 14],
                         [23, 16], [23, 17], [23, 18], [29, 3], [29, 4], [29, 5], [29, 6], [29, 7],
                         [29, 9], [29, 10], [29, 11], [29, 12], [29, 18], [29, 19], [29, 20], [29, 21],
                         [29, 23], [29, 24], [29, 25], [29, 26], [6, 10]]

coins_list = list.copy(play_again_coins_list)
power_pellets_list = list.copy(play_again_coins_list[0])


class Player(pygame.sprite.Sprite):
    def __init__(self, cell_width, cell_height, grid_buffer, v, w):
        super(Player, self).__init__()
        self.score = 0
        self.start_time = False
        self.status = 'Weak'                        # Player's status becomes strong when he hits a Power Pellet
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.grid_buffer = grid_buffer
        self.w = w                                  # w stands for walls list
        self.grid_pos = Vec(v[0], v[1])             # This pos represents Pac-Man position in terms of Column-Row format
        self.next_pos = Vec(0, 0)                   # Pac-Man's next move position
        self.prev_update = False
        self.pixel_pos = self.get_pixelpos()        # Pac-Man's position in terms of screen-width and screen-height

        self.image = pygame.image.load('pacman.png')
        self.image = pygame.transform.scale(self.image, (self.cell_width, self.cell_height))
        self.rect = self.image.get_rect()
        self.rect.left = self.pixel_pos.x
        self.rect.top = self.pixel_pos.y

    def get_pixelpos(self):
        return Vec(self.grid_buffer + ((self.grid_pos.x - 1) * self.cell_width), self.grid_buffer +
                   ((self.grid_pos.y - 1) * self.cell_height))

    def update(self, direction):
        key = False
        """if self.grid_pos.y == 29 and self.grid_pos.x == 2:
            self.kill()"""
        self.next_pos.x = self.grid_pos.x
        self.next_pos.y = self.grid_pos.y

        self.next_pos.x += direction[0]                                             # Column
        self.next_pos.y += direction[1]                                             # Row

        # checking whether there is a wall or not
        if self.w[int(self.next_pos.y) - 1][int(self.next_pos.x) - 1] != 1:
            self.grid_pos.x = self.next_pos.x
            self.grid_pos.y = self.next_pos.y
            self.rect.left += direction[0] * self.cell_width
            self.rect.top += direction[1] * self.cell_height
            self.prev_update = direction
            if self.w[int(self.next_pos.y) - 1][int(self.next_pos.x) - 1] == 'c':
                if [int(self.next_pos.y), int(self.next_pos.x)] in coins_list:
                    coins_list.remove([int(self.next_pos.y), int(self.next_pos.x)])
                    self.score += 100
            elif self.w[int(self.next_pos.y) - 1][int(self.next_pos.x) - 1] == 'p':
                if [int(self.next_pos.y), int(self.next_pos.x)] in power_pellets_list:
                    power_pellets_list.remove([int(self.next_pos.y), int(self.next_pos.x)])
                    self.score += 150
                    self.start_time = pygame.time.get_ticks()
                    self.status = 'Strong'

            key = True
        elif self.w[int(self.next_pos.y) - 1][int(self.next_pos.x) - 1] == 1:
            key = False

        self.pixel_pos = self.get_pixelpos()
        return key


class Enemy(pygame.sprite.Sprite):
    def __init__(self, path, cell_width, cell_height, grid_buffer, int_position, w):
        super(Enemy, self).__init__()
        self.path = path                             # This path variable is for Enemy's image path
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.grid_buffer = grid_buffer
        self.int_position = int_position            # Enemy's starting position in Column-Row format
        self.grid_pos = Vec(self.int_position)
        self.pixel_pos = self.get_pixelpos()
        self.next_pos = Vec(0, 0)
        self.wall_list = w
        self.start = 0
        self.prev_move = False
        self.enemy_moves = False

        self.moves_list = ['up', 'down', 'left', 'right']
        self.moves_set = set(self.moves_list)
        self.moves_dict = {'up': [0, -1], 'down': [0, 1], 'left': [-1, 0], 'right': [1, 0]}

        self.image = pygame.image.load(self.path)
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (self.cell_width, self.cell_height))
        self.rect = self.image.get_rect()
        self.rect.left = self.pixel_pos.x
        self.rect.top = self.pixel_pos.y

    def get_pixelpos(self):
        return Vec(self.grid_buffer + ((self.grid_pos.x - 1) * self.cell_width), self.grid_buffer +
                   ((self.grid_pos.y - 1) * self.cell_height))

    def update(self, enemy_moves):
        valid_move = False
        moves_set = False
        movement = False
        prev_move = False
        self.enemy_moves = enemy_moves
        if self.start < 4:
            valid_move = self.enemy_moves[self.start]
            self.prev_move = valid_move
            self.start += 1
            movement = self.moves_dict[valid_move]
        else:
            if self.prev_move == 'up':
                prev_move = 'down'
            if self.prev_move == 'down':
                prev_move = 'up'
            if self.prev_move == 'left':
                prev_move = 'right'
            if self.prev_move == 'right':
                prev_move = 'left'
            prev_move = [prev_move]
            moves_set = self.moves_set - set(prev_move)
            moves_set = list(moves_set)
            valid_move = random.choice(moves_set)
            movement = self.moves_dict[valid_move]

        self.next_pos.x = self.grid_pos.x
        self.next_pos.y = self.grid_pos.y

        self.next_pos.x += movement[0]  # Column
        self.next_pos.y += movement[1]  # Row

        if self.wall_list[int(self.next_pos.y) - 1][int(self.next_pos.x) - 1] != 1:
            self.grid_pos.x = self.next_pos.x
            self.grid_pos.y = self.next_pos.y
            self.rect.left += movement[0] * self.cell_width
            self.rect.top += movement[1] * self.cell_height
            self.prev_move = valid_move


class Coins:
    def __init__(self, cell_width, cell_height, coin_pos, power=False):
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.coin_pos = coin_pos

        if power:
            self.image = pygame.image.load('dry-clean.png')
            self.image = pygame.transform.scale(self.image, (self.cell_width - 3, self.cell_height - 4))
        elif not power:
            self.image = pygame.image.load('coin.png')
            self.image = pygame.transform.scale(self.image, (self.cell_width - 4, self.cell_height - 5))

        self.rect = self.image.get_rect()
        self.pixel_pos = self.get_pixelpos()
        self.rect.left = self.pixel_pos.x + 1
        self.rect.top = self.pixel_pos.y

    def get_pixelpos(self):
        return Vec(50 + ((self.coin_pos[1] - 1) * self.cell_width), 50 +
                   ((self.coin_pos[0] - 1) * self.cell_height))


mixer.init()
pygame.init()


WIDTH, HEIGHT = 610, 670
GRID_BUFFER = 50
GRID_WIDTH = WIDTH - (GRID_BUFFER * 2)
GRID_HEIGHT = HEIGHT - (GRID_BUFFER * 2)
CELL_WIDTH = GRID_WIDTH // 28
CELL_HEIGHT = GRID_HEIGHT // 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pacman')
game_icon = pygame.image.load('Trollman.png')
pygame.display.set_icon(game_icon)

# SOUND EFFECTS #
mixer.music.load('pacman_beginning.wav')

# INTRO TEXTS #
font_1 = pygame.font.Font('LoveGlitch.ttf', 30)
font_2 = pygame.font.Font('SCOREBOARD.ttf', 30)
# font = pygame.font.SysFont('LoveGlitch', 30)
start_text = font_1.render('PUSH SPACE TO START THE GAME', True, RED_ORANGE)
start_text_rect = start_text.get_rect()
start_text_rect.center = (WIDTH / 2, HEIGHT - 55)

player_text = font_1.render('ONE PLAYER ONLY', True, LIGHTSEAGREEN)
player_text_rect = player_text.get_rect()
player_text_rect.center = (WIDTH / 2, HEIGHT - 25)

# PLAYER INFO #
pacman_image = pygame.image.load('pacman-left.png')
pacman_image = pygame.transform.scale(pacman_image, (25, 25))
pacman_lives = 3
player = Player(CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (2, 2), wall_list)           # Column-Row format
player_score = 0

# ENEMY INFO #
Blinky_image_path = 'Blinky.png'
Blinky = Enemy(Blinky_image_path, CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (13, 15), wall_list)
Clyde_image_path = 'Clyde.png'
Clyde = Enemy(Clyde_image_path, CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (17, 15), wall_list)

Enemies = pygame.sprite.Group()
Enemies.add(Blinky)
Enemies.add(Clyde)

pacman_prev_move = False
pacman_prev_img = False
move = False
enemy_starting_moves = False

clock = pygame.time.Clock()
running = True
game_status = 'intro'
game_ended = False

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                player.image = pygame.image.load('pacman-up.png')
                player.image = pygame.transform.scale(player.image, (CELL_WIDTH, CELL_HEIGHT))
                move = (0, -1)
            if event.key == K_DOWN:
                player.image = pygame.image.load('pacman-down.png')
                player.image = pygame.transform.scale(player.image, (CELL_WIDTH, CELL_HEIGHT))
                move = (0, 1)
            if event.key == K_LEFT:
                player.image = pygame.image.load('pacman-left.png')
                player.image = pygame.transform.scale(player.image, (CELL_WIDTH, CELL_HEIGHT))
                move = (-1, 0)
            if event.key == K_RIGHT:
                player.image = pygame.image.load('pacman.png')
                player.image = pygame.transform.scale(player.image, (CELL_WIDTH, CELL_HEIGHT))
                move = (1, 0)

            if event.key == K_SPACE:
                if game_status == 'PLAY-AGAIN':
                    player.kill()
                    coins_list = list.copy(play_again_coins_list)
                    power_pellets_list = list.copy(play_again_coins_list[0])

                    player = Player(CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (2, 2), wall_list)
                    pacman_lives = 3

                    Blinky.kill()
                    Clyde.kill()
                    Blinky = Enemy(Blinky_image_path, CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (13, 15), wall_list)
                    Clyde = Enemy(Clyde_image_path, CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (17, 15), wall_list)

                    Enemies.add(Blinky)
                    Enemies.add(Clyde)

                    # coins_list = list.copy(play_again_coins_list)

                mixer.music.play(loops=-1)
                game_status = 'playing'
                move = (1, 0)
                enemy_starting_moves = ['right', 'up', 'up', 'up']

            if event.key == K_ESCAPE:
                h = player.score
                running = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if game_status == 'intro':
                    mixer.music.play(loops=-1)
                    game_status = 'playing'
                    move = (1, 0)
                    enemy_starting_moves = ['right', 'up', 'up', 'up']

        elif event.type == QUIT:
            h = player.score
            running = False

    screen.fill(BLACK)

    if game_status == 'intro':
        background_art = pygame.image.load('Pacman_intro_art_2.jpg')
        background_art = pygame.transform.scale(background_art, (WIDTH, HEIGHT - 75))
        screen.blit(background_art, (0, 0))
        screen.blit(start_text, start_text_rect)
        screen.blit(player_text, player_text_rect)

    elif game_status == 'PLAY-AGAIN':
        Game_over = pygame.image.load('Game_over_11.jpg')
        Game_over = pygame.transform.scale(Game_over, (WIDTH, 275))
        screen.blit(Game_over, (0, 10))

        End_score_text = 'YOUR  SCORE: {}'.format(player_score)
        End_score = font_2.render(End_score_text, True, GRAY)
        End_score_rect = End_score.get_rect()
        End_score_rect.center = (WIDTH / 2, 310)
        screen.blit(End_score, End_score_rect)

        End_card = pygame.image.load('End_card.jpg')
        End_card = pygame.transform.scale(End_card, (WIDTH - 100, 150))
        screen.blit(End_card, (50, HEIGHT - 200))

        play_again_text = font_1.render('PUSH SPACE TO PLAY AGAIN', True, RED_ORANGE)
        play_again_text_rect = play_again_text.get_rect()
        play_again_text_rect.center = (WIDTH / 2, 360)
        screen.blit(play_again_text, play_again_text_rect)

    elif game_status == 'playing':
        current_score_text = 'CURRENT  SCORE: {}'.format(player.score)
        current_score = font_2.render(current_score_text, True, WHITE)
        screen.blit(current_score, (70, 15))

        grid = pygame.image.load('Pacman_Grid with gate.png')
        grid = pygame.transform.scale(grid, (GRID_WIDTH, GRID_HEIGHT))
        screen.blit(grid, (GRID_BUFFER, GRID_BUFFER))

        for i in range(29):                                                      # 28 Columns
            pygame.draw.line(screen, GRAY, (GRID_BUFFER + (i * CELL_WIDTH), GRID_BUFFER),
                             (GRID_BUFFER + (i * CELL_WIDTH),
                              HEIGHT - GRID_BUFFER))
        for j in range(31):                                                         # 30 Rows
            pygame.draw.line(screen, GRAY, (GRID_BUFFER, GRID_BUFFER + (j * CELL_HEIGHT)),
                             (WIDTH - GRID_BUFFER,
                              GRID_BUFFER + (j * CELL_HEIGHT)))

        if not player.update(move):
            move = pacman_prev_move
            player.image = pacman_prev_img

        if len(coins_list[1:]) == 0:
            game_status = 'PLAY-AGAIN'
            player_score = player.score
            mixer.music.stop()

        if player.start_time:
            Blinky.image = pygame.image.load('blue_ghost.jfif')
            Blinky.image.set_colorkey(WHITE)
            Blinky.image = pygame.transform.scale(Blinky.image, (CELL_WIDTH, CELL_HEIGHT))

            Clyde.image = pygame.image.load('blue_ghost.jfif')
            Clyde.image.set_colorkey(WHITE)
            Clyde.image = pygame.transform.scale(Clyde.image, (CELL_WIDTH, CELL_HEIGHT))

            seconds = (pygame.time.get_ticks() - player.start_time) / 1000
            if seconds > 5:
                Blinky.image = pygame.image.load('Blinky.png')
                Blinky.image = pygame.transform.scale(Blinky.image, (CELL_WIDTH, CELL_HEIGHT))

                Clyde.image = pygame.image.load('Clyde.png')
                Clyde.image = pygame.transform.scale(Clyde.image, (CELL_WIDTH, CELL_HEIGHT))

                player.start_time = False
                player.status = 'Weak'

        Blinky.update(enemy_starting_moves)
        Clyde.update(enemy_starting_moves)

        pacman_prev_move = move
        pacman_prev_img = player.image
        screen.blit(player.image, player.rect)
        screen.blit(Blinky.image, Blinky.rect)
        screen.blit(Clyde.image, Clyde.rect)

        for p in range(1, len(coins_list)):
            coin = Coins(CELL_WIDTH, CELL_HEIGHT, coins_list[p])
            screen.blit(coin.image, coin.rect)

        for pos in power_pellets_list:
            pellet = Coins(CELL_WIDTH, CELL_HEIGHT, pos, True)
            screen.blit(pellet.image, pellet.rect)

        if pygame.sprite.spritecollideany(player, Enemies):
            if player.status == 'Strong':
                if player.rect.colliderect(Blinky.rect):
                    Blinky.kill()
                    Blinky = Enemy(Blinky_image_path, CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (13, 15), wall_list)
                    enemy_starting_moves = ['right', 'up', 'up', 'up']
                    Enemies.add(Blinky)
                    player.score += 200
                elif player.rect.colliderect(Clyde.rect):
                    Clyde.kill()
                    Clyde = Enemy(Clyde_image_path, CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (17, 15), wall_list)
                    enemy_starting_moves = ['right', 'up', 'up', 'up']
                    Enemies.add(Clyde)
                    player.score += 200
            else:
                pacman_lives -= 1
                if pacman_lives == 0:
                    game_status = 'PLAY-AGAIN'
                    mixer.music.stop()
                    player_score = player.score

                else:
                    player_score = player.score
                    player.kill()

                    player = Player(CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (2, 2), wall_list)
                    player.score = player_score
                    move = (1, 0)

                    Blinky.kill()
                    Clyde.kill()
                    Blinky = Enemy(Blinky_image_path, CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (13, 15), wall_list)
                    Clyde = Enemy(Clyde_image_path, CELL_WIDTH, CELL_HEIGHT, GRID_BUFFER, (17, 15), wall_list)
                    enemy_starting_moves = ['right', 'up', 'up', 'up']
                    Enemies.add(Blinky)
                    Enemies.add(Clyde)

        for i in range(pacman_lives - 1):
            screen.blit(pacman_image, (30 + (i * 25), HEIGHT - 27))

    clock.tick(15)
    pygame.display.flip()
