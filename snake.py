import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)
GRAY = (169, 169, 169)
PLAYER_1_COLOR = (0, 255, 255)
PLAYER_2_COLOR = (255, 165, 0)
POWER_UP_SLOW = (128, 0, 128)
POWER_UP_SHIELD = (255, 215, 0)

# Snake block size and speed
BLOCK_SIZE = 20
SNAKE_SPEED = 10

SKINS = {
    "Classic": {"body": PLAYER_1_COLOR, "head": (0, 200, 200)},
    "Rainbow": {"body": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), "head": (255, 255, 255)},
    "Fire": {"body": (255, 69, 0), "head": (255, 0, 0)},
    "Ice": {"body": (135, 206, 235), "head": (240, 248, 255)}
}

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Display setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

def display_score(score1, score2):
    score_text1 = score_font.render(f"Player 1 Score: {score1}", True, PLAYER_1_COLOR)
    score_text2 = score_font.render(f"Player 2 Score: {score2}", True, PLAYER_2_COLOR)
    screen.blit(score_text1, [10, 10])
    screen.blit(score_text2, [10, 50])

# [Previous imports and constants remain the same]

def draw_snake(snake_list, skin):
    # Draw fancy tail effect with particle system
    if len(snake_list) > 1:
        # Create trailing particles
        tail_particles = []
        time = pygame.time.get_ticks() * 0.001
        
        for i in range(len(snake_list) - 1):
            current = snake_list[i]
            next_block = snake_list[i + 1]
            
            # Particle effect parameters
            particle_count = 5
            particle_size = BLOCK_SIZE // 4
            fade_factor = i / len(snake_list)
            
            # Generate particles along snake body
            for p in range(particle_count):
                t = p / particle_count
                x = current[0] + (next_block[0] - current[0]) * t
                y = current[1] + (next_block[1] - current[1]) * t
                
                # Add wave motion
                wave = math.sin(time * 5 + i * 0.5) * (BLOCK_SIZE / 4)
                spiral = math.cos(time * 3 + i * 0.3) * (BLOCK_SIZE / 4)
                
                if next_block[0] - current[0] != 0:  # Horizontal
                    y += wave
                    x += spiral
                else:  # Vertical
                    x += wave
                    y += spiral
                
                # Calculate particle alpha and size
                alpha = int(255 * (1 - fade_factor))
                current_size = int(particle_size * (1 - fade_factor))
                
                # Create particle surface
                particle = pygame.Surface((current_size, current_size))
                particle.set_alpha(alpha)
                particle.fill(skin["body"])
                screen.blit(particle, (x, y))
        
        # Draw main snake body with glow effect
        for i, block in enumerate(snake_list):
            # Main body
            color = skin["head"] if i == len(snake_list) - 1 else skin["body"]
            if skin == SKINS["Rainbow"]:
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
            # Draw glowing outline
            glow_size = int(BLOCK_SIZE * 1.2)
            glow_surface = pygame.Surface((glow_size, glow_size))
            glow_surface.set_alpha(100)
            pygame.draw.rect(glow_surface, color, [0, 0, glow_size, glow_size])
            screen.blit(glow_surface, (block[0] - BLOCK_SIZE//4, block[1] - BLOCK_SIZE//4))
            
            # Main block
            pygame.draw.rect(screen, color, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])
            
            # Draw animated eyes for head
            if i == len(snake_list) - 1:
                eye_color = (255, 255, 255)
                eye_size = BLOCK_SIZE // 4
                eye_offset = BLOCK_SIZE // 4
                
                # Determine eye positions based on movement direction
                if len(snake_list) > 1:
                    prev_block = snake_list[-2]
                    dx = block[0] - prev_block[0]
                    dy = block[1] - prev_block[1]
                    
                    # Blink effect
                    blink = math.sin(time * 2) > 0.95
                    if not blink:
                        if dx > 0:  # Right
                            pygame.draw.circle(screen, eye_color, (block[0] + BLOCK_SIZE - eye_offset, block[1] + eye_offset), eye_size)
                            pygame.draw.circle(screen, eye_color, (block[0] + BLOCK_SIZE - eye_offset, block[1] + BLOCK_SIZE - eye_offset), eye_size)
                        elif dx < 0:  # Left
                            pygame.draw.circle(screen, eye_color, (block[0] + eye_offset, block[1] + eye_offset), eye_size)
                            pygame.draw.circle(screen, eye_color, (block[0] + eye_offset, block[1] + BLOCK_SIZE - eye_offset), eye_size)
                        elif dy > 0:  # Down
                            pygame.draw.circle(screen, eye_color, (block[0] + eye_offset, block[1] + BLOCK_SIZE - eye_offset), eye_size)
                            pygame.draw.circle(screen, eye_color, (block[0] + BLOCK_SIZE - eye_offset, block[1] + BLOCK_SIZE - eye_offset), eye_size)
                        else:  # Up
                            pygame.draw.circle(screen, eye_color, (block[0] + eye_offset, block[1] + eye_offset), eye_size)
                            pygame.draw.circle(screen, eye_color, (block[0] + BLOCK_SIZE - eye_offset, block[1] + eye_offset), eye_size)

# [Rest of the code remains the same]

def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(0,0,0)
    screen.blit(overlay, (0, 0))
    
    pause_text = font_style.render("PAUSED", True, WHITE)
    continue_text = font_style.render("Press P to Continue", True, WHITE)
    screen.blit(pause_text, [WIDTH/2 - 60, HEIGHT/2 - 30])
    screen.blit(continue_text, [WIDTH/2 - 100, HEIGHT/2 + 30])



def skin_selection_menu():
    selected = "Classic"
    selecting = True
    
    while selecting:
        screen.fill(WHITE)
        y_pos = HEIGHT // 4
        title = font_style.render("Select Snake Skin (Use Arrow Keys, Press Enter)", True, BLACK)
        screen.blit(title, [WIDTH // 4, y_pos - 50])
        
        for i, skin in enumerate(SKINS.keys()):
            color = GREEN if skin == selected else BLACK
            text = font_style.render(skin, True, color)
            screen.blit(text, [WIDTH // 3, y_pos + i * 50])
            
            # Preview snake
            preview_blocks = [[WIDTH * 2 // 3 + j * 20, y_pos + i * 50] for j in range(3)]
            draw_snake(preview_blocks, SKINS[skin])
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return SKINS[selected]
                elif event.key == pygame.K_UP:
                    keys = list(SKINS.keys())
                    current_index = keys.index(selected)
                    selected = keys[(current_index - 1) % len(keys)]
                elif event.key == pygame.K_DOWN:
                    keys = list(SKINS.keys())
                    current_index = keys.index(selected)
                    selected = keys[(current_index + 1) % len(keys)]



def main_menu():
    menu = True
    while menu:
        screen.fill(WHITE)
        menu_text = font_style.render("Choose Game Mode: 1. Single Player  2. Multiplayer", True, BLACK)
        screen.blit(menu_text, [WIDTH // 6, HEIGHT // 3])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Single player mode
                    skin = skin_selection_menu()
                    game_loop(single_player=True, skin1=skin)
                    menu = False
                elif event.key == pygame.K_2:
                    # Multiplayer mode
                    skin1 = skin_selection_menu()
                    skin2 = skin_selection_menu()
                    game_loop(single_player=False, skin1=skin1, skin2=skin2)
                    menu = False

# [Rest of the code remains the same]


def game_loop(single_player, skin1, skin2=None):
    game_over = False
    paused = False
    current_speed = SNAKE_SPEED

    # Initial positions
    x1, y1 = WIDTH / 4, HEIGHT / 2
    x2, y2 = 3 * WIDTH / 4, HEIGHT / 2

    x1_change, y1_change = BLOCK_SIZE, 0  # Start moving right
    x2_change, y2_change = -BLOCK_SIZE, 0 if not single_player else 0  # Start moving left in multiplayer

    # Initialize snakes with proper starting positions
    snake1 = [[x1 - (i * BLOCK_SIZE), y1] for i in range(3)]  # Start with 3 blocks
    snake2 = [[x2 + (i * BLOCK_SIZE), y2] for i in range(3)] if not single_player else []
    snake1_length, snake2_length = len(snake1), len(snake2)

    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    obstacles = [
        (round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE,
         round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE)
        for _ in range(10)
    ]

    power_up_x, power_up_y = None, None
    power_up_type = None
    power_up_timer = 0
    shield_active = {"player1": False, "player2": False}

    def spawn_power_up():
        nonlocal power_up_x, power_up_y, power_up_type
        power_up_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        power_up_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        power_up_type = random.choice(["slow", "shield"])

    spawn_power_up()

    # Initial draw
    screen.fill(WHITE)
    pygame.draw.rect(screen, YELLOW, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
    for obs in obstacles:
        pygame.draw.rect(screen, GRAY, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])
    if power_up_x is not None and power_up_y is not None:
        color = POWER_UP_SLOW if power_up_type == "slow" else POWER_UP_SHIELD
        pygame.draw.rect(screen, color, [power_up_x, power_up_y, BLOCK_SIZE, BLOCK_SIZE])
    draw_snake(snake1, skin1)
    if not single_player:
        draw_snake(snake2, skin2)
    display_score(snake1_length - 1, snake2_length - 1 if not single_player else 0)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if not paused:
                    if single_player:
                        # Single player controls remain the same
                        if event.key == pygame.K_UP and y1_change == 0:
                            x1_change, y1_change = 0, -BLOCK_SIZE
                        elif event.key == pygame.K_DOWN and y1_change == 0:
                            x1_change, y1_change = 0, BLOCK_SIZE
                        elif event.key == pygame.K_LEFT and x1_change == 0:
                            x1_change, y1_change = -BLOCK_SIZE, 0
                        elif event.key == pygame.K_RIGHT and x1_change == 0:
                            x1_change, y1_change = BLOCK_SIZE, 0
                    else:
                        # Multiplayer controls remain the same
                        if event.key == pygame.K_w and y1_change == 0:
                            x1_change, y1_change = 0, -BLOCK_SIZE
                        elif event.key == pygame.K_s and y1_change == 0:
                            x1_change, y1_change = 0, BLOCK_SIZE
                        elif event.key == pygame.K_a and x1_change == 0:
                            x1_change, y1_change = -BLOCK_SIZE, 0
                        elif event.key == pygame.K_d and x1_change == 0:
                            x1_change, y1_change = BLOCK_SIZE, 0
                        
                        if event.key == pygame.K_UP and y2_change == 0:
                            x2_change, y2_change = 0, -BLOCK_SIZE
                        elif event.key == pygame.K_DOWN and y2_change == 0:
                            x2_change, y2_change = 0, BLOCK_SIZE
                        elif event.key == pygame.K_LEFT and x2_change == 0:
                            x2_change, y2_change = -BLOCK_SIZE, 0
                        elif event.key == pygame.K_RIGHT and x2_change == 0:
                            x2_change, y2_change = BLOCK_SIZE, 0


        if not paused:
            x1 += x1_change
            y1 += y1_change
            if not single_player:
                x2 += x2_change
                y2 += y2_change

            if not shield_active["player1"] and (x1 < 0 or x1 >= WIDTH or y1 < 0 or y1 >= HEIGHT):
                game_over = True
            if not single_player and not shield_active["player2"] and (x2 < 0 or x2 >= WIDTH or y2 < 0 or y2 >= HEIGHT):
                game_over = True

            for obs in obstacles:
                if not shield_active["player1"] and (x1, y1) == obs:
                    game_over = True
                if not single_player and not shield_active["player2"] and (x2, y2) == obs:
                    game_over = True

            if not single_player and ([x1, y1] in snake2 or [x2, y2] in snake1):
                game_over = True

            if x1 == food_x and y1 == food_y:
                food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                snake1_length += 1
            if not single_player and x2 == food_x and y2 == food_y:
                food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                snake2_length += 1

            if power_up_x is not None and power_up_y is not None:
                if x1 == power_up_x and y1 == power_up_y:
                    if power_up_type == "slow":
                        current_speed = max(5, current_speed - 5)
                        power_up_timer = 200
                    elif power_up_type == "shield":
                        shield_active["player1"] = True
                        power_up_timer = 200
                    spawn_power_up()
                if not single_player and x2 == power_up_x and y2 == power_up_y:
                    if power_up_type == "slow":
                        current_speed = max(5, current_speed - 5)
                        power_up_timer = 200
                    elif power_up_type == "shield":
                        shield_active["player2"] = True
                        power_up_timer = 200
                    spawn_power_up()

            if power_up_timer > 0:
                power_up_timer -= 1
                if power_up_timer == 0:
                    current_speed = SNAKE_SPEED
                    shield_active["player1"] = False
                    shield_active["player2"] = False

            snake1.append([x1, y1])
            if not single_player:
                snake2.append([x2, y2])

            if len(snake1) > snake1_length:
                del snake1[0]
            if not single_player and len(snake2) > snake2_length:
                del snake2[0]

            screen.fill(WHITE)
            pygame.draw.rect(screen, YELLOW, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])
            for obs in obstacles:
                pygame.draw.rect(screen, GRAY, [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])
            if power_up_x is not None and power_up_y is not None:
                color = POWER_UP_SLOW if power_up_type == "slow" else POWER_UP_SHIELD
                pygame.draw.rect(screen, color, [power_up_x, power_up_y, BLOCK_SIZE, BLOCK_SIZE])
            draw_snake(snake1, skin1)
            if not single_player:
                draw_snake(snake2, skin2)
            display_score(snake1_length - 1, snake2_length - 1 if not single_player else 0)

            if paused:
                draw_pause_menu()
                

            pygame.display.update()
            clock.tick(current_speed)

    pygame.quit()
    quit()

main_menu()