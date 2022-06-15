import pygame, random
from pygame.locals import *


def on_grid_random():  # ajust the apples position to be in the 10x10 grade
    x = random.randrange(0, 880, 20)
    y = random.randrange(0, 680, 20)
    return (x // 10 * 10, y // 10 * 10)


def collision(c1, c2):
    return (
        c1[0] == c2[0] and c1[1] == c2[1]
    )  # when cell 1 (snakes head) and cell 2 (apple) ocuppate the same x,y position


def hold():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return False


def choose_difficulty():
    global speed
    screen.fill((46, 46, 46))
    print_on_screen(
        60, "Choose game's difficulty:", (0, 255, 0), (980 // 2, 720 // 2 - 50)
    )
    print_on_screen(
        40,
        "Easy (1)    Medium (2)  Diffucult(3)",
        (0, 255, 0),
        (980 // 2, 720 // 2 + 50),
    )
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    speed = 10
                    return False
                if event.key == K_2:
                    speed = 20
                    return False
                if event.key == K_3:
                    speed = 30
                    return False


def print_on_screen(
    font_size, words, color, position, update=True, font="arial", bold=True, italic=True
):
    introdution_font = pygame.font.SysFont(font, font_size, bold, italic)
    introdution_screen = introdution_font.render(
        words,
        bold,
        color,
    )
    introdution_rect = introdution_screen.get_rect()
    introdution_rect.center = position
    screen.blit(introdution_screen, introdution_rect)
    if update == True:
        pygame.display.update()


def restart_game():
    global snake, score, my_direction, game_over, apple_pos
    snake = [(200, 720 // 2), (210, 720 // 2), (220, 720 // 2)]
    score = 0
    my_direction = RIGHT
    game_over = False
    apple_pos = on_grid_random()
    pygame.display.update()


pygame.init()  # begining

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

screen = pygame.display.set_mode((980, 720))  # tamanho da tela
pygame.display.set_caption("Snake by Eduardo Boor")
screen.fill((46, 46, 46))


snake = [(200, 720 // 2), (210, 720 // 2), (220, 720 // 2)]  # snake's length
snake_skin = pygame.Surface((20, 20))  # squares of 10x10 pixels
snake_skin.fill((20, 255, 100))  # snake's color

apple_pos = (
    on_grid_random()
)  # we're using 20x20 squares, so the last possible position to plot the apple is 590p
apple = pygame.Surface((20, 20))  # apple size
apple.fill((255, 0, 0))  # apple colour


my_direction = RIGHT

clock = pygame.time.Clock()

score = 0

pause = False

game_over = False

game = True

speed = 15

print_on_screen(
    60, "Welcome to Snake's Game!", (0, 255, 0), (980 / 2, 720 / 2 - 100), False
)
print_on_screen(40, "Press Enter to start", (0, 255, 0), (980 // 3, 720 / 2), False)
print_on_screen(40, "Press Esc to pause", (0, 255, 0), (980 // 3 - 3, 720 / 2 + 50))


snake_image = pygame.image.load("snake-image.png")
w, h = snake_image.get_size()
image_ajusted = pygame.transform.smoothscale(
    snake_image, (int(w * 0.25), int(h * 0.25))
)


image_rect = snake_image.get_rect()
image_rect.midleft = (550, 850)
screen.blit(image_ajusted, image_rect)
pygame.display.update()

hold()

choose_difficulty()


while game:

    while not game_over or pause:

        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN:  # if the event is pressing a key
                if (
                    event.key == K_UP and my_direction != DOWN
                ):  # if the key pressed is == to 'key up'
                    my_direction = UP  # the direction changes to 'up'
                if event.key == K_DOWN and my_direction != UP:
                    my_direction = DOWN
                if event.key == K_RIGHT and my_direction != LEFT:
                    my_direction = RIGHT
                if event.key == K_LEFT and my_direction != RIGHT:
                    my_direction = LEFT
                if event.key == K_ESCAPE:
                    pause = True
                    break

        if pause:
            break

        if collision(snake[0], apple_pos):
            apple_pos = on_grid_random()
            snake.append((0, 0))
            score += 1

        if (
            snake[0][0] == 980
            or snake[0][1] == 720
            or snake[0][0] < 0
            or snake[0][1] < 0
        ):  # hits final of map
            game_over = True
            break

        for i in range(1, len(snake) - 1):  # hits its self
            if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
                game_over = True
                break

        if game_over:
            break

        for i in range(len(snake) - 1, 0, -1):
            snake[i] = (snake[i - 1][0], snake[i - 1][1])

        if my_direction == UP:
            snake[0] = (snake[0][0], snake[0][1] - 20)  # heads position = (x , y-10p)
        if my_direction == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + 20)
        if my_direction == RIGHT:
            snake[0] = (snake[0][0] + 20, snake[0][1])
        if my_direction == LEFT:
            snake[0] = (snake[0][0] - 20, snake[0][1])

        screen.fill((0, 0, 0))
        screen.blit(apple, apple_pos)

        for x in range(0, 980, 20):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 980))
        for y in range(0, 720, 20):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (980, y))

        print_on_screen(30, "Score: %s" % (score), (255, 255, 255), (880, 20), False)

        for pos in snake:
            screen.blit(snake_skin, pos)  # plot on screen

        pygame.display.update()

    while game_over:
        screen.fill((158, 166, 154))
        print_on_screen(90, "Game Over", (220, 0, 0), (980 / 2, 720 / 2 - 100), False)
        print_on_screen(
            50, "Press 'R' to restart", (150, 0, 0), (980 / 2, 700 / 2), False
        )
        print_on_screen(
            50,
            "Press 'Esc' to change the difficulty",
            (150, 0, 0),
            (980 / 2, 700 / 2 + 65),
            False,
        )
        print_on_screen(
            50,
            "Press 'Backspace' to exit",
            (150, 0, 0),
            (980 / 2, 700 / 2 + 130),
        )
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    restart_game()
                    game_over = False
                if event.key == K_ESCAPE:
                    choose_difficulty()
                    restart_game()
                    game_over = False
                if event.key == K_BACKSPACE:
                    pygame.quit()
                    exit()

    while pause:
        screen.fill((0, 0, 0))
        print_on_screen(75, "Game Paused", (0, 255, 0), (980 / 2, 700 / 2))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pause = False
