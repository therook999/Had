import pygame
import random
import sys

pygame.init()

# ===== NASTAVENÍ =====
WINDOW_SIZE = 700
TILE_SIZE = 20
GRID_COUNT = WINDOW_SIZE // TILE_SIZE

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Had")
icon = pygame.image.load("favicon.ico")
pygame.display.set_icon(icon)

clock = pygame.time.Clock()

font_big = pygame.font.SysFont(None, 70)
font_medium = pygame.font.SysFont(None, 40)

# ===== BARVY =====
BLACK = (25, 25, 25)
GREEN = (0, 150, 0)
LIME = (0, 255, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
GRAY = (70, 70, 70)
GREEN_1 = (50,225,50)
GREEN_2 = (50,215,50)
PURPLE = (128, 0, 128)
Purple2 = (170, 0, 170)
PURPLE_3 = (200, 0, 200)


def reset_game():
    global snake, direction, apple, score, game_over_state
    snake = [(5, 5), (4, 5), (3, 5)]
    direction = (1, 0)
    score = 0
    apple = generate_apple()
    game_over_state = False

def generate_apple():
    while True:
        pos = (random.randint(0, GRID_COUNT - 1),
               random.randint(0, GRID_COUNT - 1))
        if pos not in snake:
            return pos
def draw_game():
    for row in range(GRID_COUNT):
        for col in range(GRID_COUNT):
            # Pokud je součet řádku a sloupce sudý, použij GREEN, jinak GREEN_1
            color = GREEN_2 if (row + col) % 2 == 0 else GREEN_1
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    

    # jablko

    apple_x = apple[0] * TILE_SIZE + TILE_SIZE // 2
    apple_y = apple[1] * TILE_SIZE + TILE_SIZE // 2

# poloměr o něco menší než políčko
    apple_img = pygame.image.load("apple.ico")
    apple_img = pygame.transform.scale(apple_img, (TILE_SIZE, TILE_SIZE))

    apple_rect = (apple[0] * TILE_SIZE, apple[1] * TILE_SIZE)
    screen.blit(apple_img, apple_rect)

    # had
    for i, segment in enumerate(snake):
        x_pixel = segment[0] * TILE_SIZE
        y_pixel = segment[1] * TILE_SIZE

        if i == 0:
            # ===== HLAVA =====
            pygame.draw.rect(screen, PURPLE_3,
                            (x_pixel, y_pixel, TILE_SIZE, TILE_SIZE))
        
            eye_size = 4
            tongue_length = 10

            dx, dy = direction

            # OČI podle směru
            if direction == (1, 0):  # doprava
                eye1 = (x_pixel + 14, y_pixel + 5)
                eye2 = (x_pixel + 14, y_pixel + 15)
                tongue_start = (x_pixel + TILE_SIZE, y_pixel + TILE_SIZE//2)
                tongue_end = (x_pixel + TILE_SIZE + tongue_length, y_pixel + TILE_SIZE//2)

            elif direction == (-1, 0):  # doleva
                eye1 = (x_pixel + 2, y_pixel + 5)
                eye2 = (x_pixel + 2, y_pixel + 15)
                tongue_start = (x_pixel, y_pixel + TILE_SIZE//2)
                tongue_end = (x_pixel - tongue_length, y_pixel + TILE_SIZE//2)

            elif direction == (0, -1):  # nahoru
                eye1 = (x_pixel + 5, y_pixel + 2)
                eye2 = (x_pixel + 15, y_pixel + 2)
                tongue_start = (x_pixel + TILE_SIZE//2, y_pixel)
                tongue_end = (x_pixel + TILE_SIZE//2, y_pixel - tongue_length)

            elif direction == (0, 1):  # dolů
                eye1 = (x_pixel + 5, y_pixel + 14)
                eye2 = (x_pixel + 15, y_pixel + 14)
                tongue_start = (x_pixel + TILE_SIZE//2, y_pixel + TILE_SIZE)
                tongue_end = (x_pixel + TILE_SIZE//2, y_pixel + TILE_SIZE + tongue_length)

            # vykreslení očí
            pygame.draw.circle(screen, WHITE, eye1, eye_size)
            pygame.draw.circle(screen, WHITE, eye2, eye_size)

            pupil_size = 2
            # Posuneme zorničku o 1 pixel ve směru dx, dy
            pupil1 = (eye1[0] + dx, eye1[1] + dy)
            pupil2 = (eye2[0] + dx, eye2[1] + dy)
            
            pygame.draw.circle(screen, BLACK, pupil1, pupil_size)
            pygame.draw.circle(screen, BLACK, pupil2, pupil_size)

            # vykreslení jazyka
            pygame.draw.line(screen, (255, 0, 0),
                            tongue_start, tongue_end, 3)

        else:
            # ===== TĚLO =====
            body_length = len(snake) - 1  # bez hlavy
            color = (200 - (200*i/body_length), 50 - (50*i/body_length), 200 - (200*i/body_length))
            

            pygame.draw.rect(screen, color,
                            (x_pixel, y_pixel, TILE_SIZE, TILE_SIZE))


    # score
    score_text = font_medium.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over():
    overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    game_over_text = font_big.render("GAME OVER", True, RED)
    score_text = font_medium.render(f"Score: {score}", True, WHITE)

    screen.blit(game_over_text, (WINDOW_SIZE//2 - game_over_text.get_width()//2, 250))
    screen.blit(score_text, (WINDOW_SIZE//2 - score_text.get_width()//2, 330))

    # tlačítko
    button_rect = pygame.Rect(WINDOW_SIZE//2 - 100, 400, 200, 60)
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 2)

    button_text = font_medium.render("NEW GAME", True, WHITE)
    screen.blit(button_text,
                (button_rect.x + button_rect.width//2 - button_text.get_width()//2,
                 button_rect.y + button_rect.height//2 - button_text.get_height()//2))

    return button_rect

# ===== START =====
reset_game()

# ===== HLAVNÍ SMYČKA =====
while True:
    clock.tick(6)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over_state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                if event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                if event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                if event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    reset_game()

    if not game_over_state:
        # pohyb
        new_head = (snake[0][0] + direction[0],
                    snake[0][1] + direction[1])

        # kolize zeď
        if (new_head[0] < 0 or new_head[0] >= GRID_COUNT or
            new_head[1] < 0 or new_head[1] >= GRID_COUNT):
            game_over_state = True

        # kolize tělo
        if new_head in snake:
            game_over_state = True

        if not game_over_state:
            snake.insert(0, new_head)

            if new_head == apple:
                score += 1
                apple = generate_apple()
            else:
                snake.pop()
    draw_game()

    if game_over_state:
        button = draw_game_over()

    pygame.display.flip()