import pygame
import sys
import random


def show_main_menu():
    pygame.init()

    width, height = 1000, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SNAKE")

    black = (0, 0, 0)
    green = (0, 255, 0)

    font = pygame.font.Font(None, 36)

    def draw_text(text, x, y, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    # Główna pętla programu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 400 <= x <= 600 and 200 <= y <= 250:
                    play_game_single()
                elif 400 <= x <= 600 and 270 <= y <= 320:
                    play_game_multi()
                elif 400 <= x <= 600 and 340 <= y <= 410:
                    play_game_ai()
                elif 400 <= x <= 600 and 540 <= y <= 610:
                    pygame.quit()
                    sys.exit()

        screen.fill(black)

        # Rysowanie przycisków
        pygame.draw.rect(screen, green, (400, 200, 200, 50))
        draw_text("SingleSnake", width // 2, 225, black)

        pygame.draw.rect(screen, green, (400, 270, 200, 50))
        draw_text("MultiSnake", width // 2, 295, black)

        pygame.draw.rect(screen, green, (400, 340, 200, 50))
        draw_text("AI-Snake", width // 2, 365, black)

        pygame.draw.rect(screen, green, (400, 540, 200, 50))
        draw_text("Exit", width // 2, 565, black)

        pygame.display.flip()

    # Zakończenie programu
    pygame.quit()
    sys.exit()


def end_game(mode: str, green_points, blue_points):
    pygame.init()

    width, height = 1000, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SNAKE")

    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    font = pygame.font.Font(None, 36)

    def draw_text(text, x, y, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    # Główna pętla programu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 400 <= x <= 600 and 400 <= y <= 450:
                    if mode == "single":
                        play_game_single()
                    elif mode == "multi":
                        play_game_multi()
                elif 400 <= x <= 600 and 470 <= y <= 520:
                    show_main_menu()
                elif 400 <= x <= 600 and 540 <= y <= 610:
                    pygame.quit()
                    sys.exit()

        screen.fill(black)

        # Rysowanie przycisków
        pygame.draw.rect(screen, green, (400, 400, 200, 50))
        draw_text("Play again", width // 2, 425, black)

        pygame.draw.rect(screen, green, (400, 470, 200, 50))
        draw_text("Main menu", width // 2, 495, black)

        pygame.draw.rect(screen, green, (400, 540, 200, 50))
        draw_text("Exit", width // 2, 565, black)

        draw_text("GAME OVER", width // 2, 100, green)
        if mode == 'multi':
            draw_text(f"BLUE SNAKE POINTS: {blue_points}", width // 4, 200, blue)
            draw_text(f"GREEN SNAKE POINTS: {green_points}", (width // 4) * 3, 200, green)
        elif mode == 'single':
            draw_text(f"POINTS: {green_points}", width // 2, 200, green)

        pygame.display.flip()

    # Zakończenie programu
    pygame.quit()
    sys.exit()

def play_game_single():

    pygame.init()

    width, height = 1000, 800
    block_size = 20
    fps = 15

    black = (0, 0, 0)
    red = (230, 20, 20)
    green = (0, 255, 0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('SinglePlayer Snake Game')

    clock = pygame.time.Clock()

    def generate_food_position(snake_list):
        while True:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            if [food_x, food_y] not in snake_list:
                return food_x, food_y


    def gameLoop():
        game_over = False
        first_move = True
        x, y = width / 2, height / 2
        x_change, y_change = 0, 0

        snake_list = []
        length_of_snake = 1

        food_x, food_y = generate_food_position(snake_list)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if first_move:
                        if event.key == pygame.K_UP:
                            x_change, y_change = 0, -block_size
                            first_move = False
                        elif event.key == pygame.K_DOWN:
                            x_change, y_change = 0, block_size
                            first_move = False
                        elif event.key == pygame.K_LEFT:
                            x_change, y_change = -block_size, 0
                            first_move = False
                        elif event.key == pygame.K_RIGHT:
                            x_change, y_change = block_size, 0
                            first_move = False
                    else:
                        if event.key == pygame.K_UP and (x_change != 0 and y_change != -block_size):
                            x_change, y_change = 0, -block_size
                        elif event.key == pygame.K_DOWN and (x_change != 0 and y_change != block_size):
                            x_change, y_change = 0, block_size
                        elif event.key == pygame.K_LEFT and (x_change != -block_size and y_change != 0):
                            x_change, y_change = -block_size, 0
                        elif event.key == pygame.K_RIGHT and (x_change != block_size and y_change != 0):
                            x_change, y_change = block_size, 0

            x += x_change
            y += y_change

            if x >= width or x < 0 or y >= height or y < 0:
                game_over = True

            screen.fill(black)
            pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

            snake_head = [x, y]
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_over = True

            for segment in snake_list:
                pygame.draw.rect(screen, green, [segment[0], segment[1], block_size, block_size])
                pygame.draw.rect(screen, black, [segment[0], segment[1], block_size, block_size], 1)

            pygame.display.update()

            if x == food_x and y == food_y:
                food_x, food_y = generate_food_position(snake_list)
                length_of_snake += 1

            clock.tick(fps)
            pygame.display.update()

        end_game('single', length_of_snake - 1, 0)
        pygame.quit()
        quit()

    gameLoop()


def play_game_multi():

    pygame.init()

    width, height = 1000, 800
    block_size = 20
    fps = 15

    black = (0, 0, 0)
    red = (230, 20, 20)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MultiPlayer Snake Game')

    clock = pygame.time.Clock()

    def generate_food_position(snake_list1, snake_list2, food_x1 = 0.0, food_y1 = 0.0):
        while True:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            if [food_x, food_y] not in snake_list1 and [food_x, food_y] not in snake_list2 and food_x1 != food_x and food_y1 != food_y:
                return food_x, food_y

    def draw_snake(snake_list, color):
        for segment in snake_list:
            pygame.draw.rect(screen, color, [segment[0], segment[1], block_size, block_size])
            pygame.draw.rect(screen, black, [segment[0], segment[1], block_size, block_size], 1)

    def gameLoop():
        game_over = False
        game_over_green = False
        game_over_blue = False

        green_first_move = True
        x_green, y_green = (width / 2) + block_size * 3, height / 2
        x_green_change, y_green_change = 0, 0

        blue_first_move = True
        x_blue, y_blue = (width / 2) - block_size * 3, height / 2
        x_blue_change, y_blue_change = 0, 0

        green_snake_list = []
        length_of_green_snake = 1

        blue_snake_list = []
        length_of_blue_snake = 1

        food_x1, food_y1 = generate_food_position(green_snake_list, blue_snake_list)
        food_x2, food_y2 = generate_food_position(green_snake_list, blue_snake_list,food_x1,food_y1)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                        # Pierwszy ruch zielonego
                        if event.key == pygame.K_UP and green_first_move and not game_over_green:
                            x_green_change, y_green_change = 0, -block_size
                            green_first_move = False
                        elif event.key == pygame.K_DOWN and green_first_move and not game_over_green:
                            x_green_change, y_green_change = 0, block_size
                            green_first_move = False
                        elif event.key == pygame.K_LEFT and green_first_move and not game_over_green:
                            x_green_change, y_green_change = -block_size, 0
                            green_first_move = False
                        elif event.key == pygame.K_RIGHT and green_first_move and not game_over_green:
                            x_green_change, y_green_change = block_size, 0
                            green_first_move = False

                        # Pierwszy ruch niebieskiego
                        elif event.key == pygame.K_w and blue_first_move and not game_over_blue:
                            x_blue_change, y_blue_change = 0, -block_size
                            blue_first_move = False
                        elif event.key == pygame.K_s and blue_first_move and not game_over_blue:
                            x_blue_change, y_blue_change = 0, block_size
                            blue_first_move = False
                        elif event.key == pygame.K_a and blue_first_move and not game_over_blue:
                            x_blue_change, y_blue_change = -block_size, 0
                            blue_first_move = False
                        elif event.key == pygame.K_d and blue_first_move and not game_over_blue:
                            blue_first_move = False
                            x_blue_change, y_blue_change = block_size, 0

                        # Nie pierwszy ruch zielonego
                        if event.key == pygame.K_UP and not green_first_move and (x_green_change != 0 and y_green_change != -block_size) and not game_over_green:
                            x_green_change, y_green_change = 0, -block_size
                        elif event.key == pygame.K_DOWN and not green_first_move and (x_green_change != 0 and y_green_change != block_size) and not game_over_green:
                            x_green_change, y_green_change = 0, block_size
                        elif event.key == pygame.K_LEFT and not green_first_move and (x_green_change != -block_size and y_green_change != 0) and not game_over_green:
                            x_green_change, y_green_change = -block_size, 0
                        elif event.key == pygame.K_RIGHT and not green_first_move and (x_green_change != -block_size and y_green_change != 0) and not game_over_green:
                            x_green_change, y_green_change = block_size, 0

                        # Nie pierwszy ruch niebieskiego
                        if event.key == pygame.K_w and not blue_first_move and (x_blue_change != 0 and y_blue_change != -block_size) and not game_over_blue:
                            x_blue_change, y_blue_change = 0, -block_size
                        elif event.key == pygame.K_s and not blue_first_move and (x_blue_change != 0 and y_blue_change != block_size) and not game_over_blue:
                            x_blue_change, y_blue_change = 0, block_size
                        elif event.key == pygame.K_a and not blue_first_move and (x_blue_change != -block_size and y_blue_change != 0) and not game_over_blue:
                            x_blue_change, y_blue_change = -block_size, 0
                        elif event.key == pygame.K_d and not blue_first_move and (x_blue_change != -block_size and y_blue_change != 0) and not game_over_blue:
                            x_blue_change, y_blue_change = block_size, 0

            x_green += x_green_change
            y_green += y_green_change

            x_blue += x_blue_change
            y_blue += y_blue_change

            # Sprawdzenie czy zielony nie wyjechał z planszy
            if x_green >= width or x_green < 0 or y_green >= height or y_green < 0:
                x_green_change, y_green_change = 0, 0
                game_over_green = True

            # Sprawdzenie czy niebieski nie wyjechał z planszy
            if x_blue >= width or x_blue < 0 or y_blue >= height or y_blue < 0:
                x_blue_change, y_blue_change = 0, 0
                game_over_blue = True

            screen.fill(black)
            pygame.draw.rect(screen, red, [food_x1, food_y1, block_size, block_size])
            pygame.draw.rect(screen, red, [food_x2, food_y2, block_size, block_size])

            green_snake_head = [x_green, y_green]
            green_snake_list.append(green_snake_head)

            blue_snake_head = [x_blue, y_blue]
            blue_snake_list.append(blue_snake_head)

            if len(green_snake_list) > length_of_green_snake and not game_over_green:
                del green_snake_list[0]

            if len(blue_snake_list) > length_of_blue_snake and not game_over_blue:
                del blue_snake_list[0]

            draw_snake(green_snake_list, green)
            draw_snake(blue_snake_list, blue)

            pygame.display.update()

            # Uderzenie zielonego w samego siebie
            for segment in green_snake_list[:-1]:
                if segment == green_snake_head:
                    x_green_change, y_green_change = 0, 0
                    game_over_green = True

            # Uderzenie zielonego w niebieskiego
            for segment in blue_snake_list[:-1]:
                if segment == green_snake_head:
                    x_green_change, y_green_change = 0, 0
                    game_over_green = True

            # Uderzenie niebieskiego w samego siebie
            for segment in blue_snake_list[:-1]:
                if segment == blue_snake_head:
                    x_blue_change, y_blue_change = 0, 0
                    game_over_blue = True

            # Uderzenie niebieskiego w zielonego
            for segment in green_snake_list[:-1]:
                if segment == blue_snake_head:
                    x_blue_change, y_blue_change = 0, 0
                    game_over_blue = True

            # Zielony zjada jedzenie1
            if x_green == food_x1 and y_green == food_y1:
                food_x1, food_y1 = generate_food_position(green_snake_list, blue_snake_list, food_x2, food_y2)
                length_of_green_snake += 1

            # Zielony zjada jedzenie2
            if x_green == food_x2 and y_green == food_y2:
                food_x2, food_y2 = generate_food_position(green_snake_list, blue_snake_list, food_x1, food_x2)
                length_of_green_snake += 1

            # Niebieski zjada jedzenie1
            if x_blue == food_x1 and y_blue == food_y1:
                food_x1, food_y1 = generate_food_position(green_snake_list, blue_snake_list, food_x2, food_y2)
                length_of_blue_snake += 1

            # Niebieski zjada jedzenie2
            if x_blue == food_x2 and y_blue == food_y2:
                food_x2, food_y2 = generate_food_position(green_snake_list, blue_snake_list, food_x1, food_y1)
                length_of_blue_snake += 1

            if game_over_green and game_over_blue:
                end_game('multi', length_of_green_snake - 1, length_of_blue_snake - 1)

            clock.tick(fps)
            pygame.display.update()

        show_main_menu()
        pygame.quit()
        quit()

    gameLoop()

def play_game_ai():

    pygame.init()

    width, height = 1000, 800
    block_size = 20
    fps = 15

    black = (0, 0, 0)
    red = (230, 20, 20)
    green = (0, 255, 0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake-AI')

    clock = pygame.time.Clock()

    def generate_food_position(snake_list):
        while True:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            if [food_x, food_y] not in snake_list:
                return food_x, food_y

    def next_block_in_snake(x,y,x_change, y_change, snake_list):
        next_x = x + x_change
        next_y = y + y_change
        next_block = [next_x, next_y]
        return next_block in snake_list


    def gameLoop():
        game_over = False
        x, y = width / 2, height / 2


        snake_list = []
        length_of_snake = 1

        food_x, food_y = generate_food_position(snake_list)

        # Początkowy ruch węża
        if x < food_x:
            x_change, y_change = block_size, 0
        elif x > food_x:
            x_change, y_change = -block_size, 0
        elif y < food_y:
            x_change, y_change = 0, block_size
        elif y > food_y:
            x_change, y_change = 0, -block_size

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True

            x += x_change
            y += y_change

            if x >= width or x < 0 or y >= height or y < 0:
                game_over = True

            screen.fill(black)
            pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

            snake_head = [x, y]
            snake_list.append(snake_head)

            if len(snake_list) > length_of_snake:
                del snake_list[0]

            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_over = True

            for segment in snake_list:
                pygame.draw.rect(screen, green, [segment[0], segment[1], block_size, block_size])
                pygame.draw.rect(screen, black, [segment[0], segment[1], block_size, block_size], 1)

            pygame.display.update()

            if x == food_x and y == food_y:
                food_x, food_y = generate_food_position(snake_list)
                length_of_snake += 1

            # Obsługa ominięcia węża
            if next_block_in_snake(x,y,x_change,y_change,snake_list):
                if x_change == block_size:
                    if not next_block_in_snake(x, y, 0, -block_size, snake_list):
                        y_change = -block_size
                    elif not next_block_in_snake(x, y, 0, block_size, snake_list):
                        y_change = block_size
                elif x_change == -block_size:
                    if not next_block_in_snake(x, y, 0, -block_size, snake_list):
                        y_change = -block_size
                    elif not next_block_in_snake(x, y, 0, block_size, snake_list):
                        y_change = block_size
                elif y_change == block_size:
                    if not next_block_in_snake(x, y, -block_size, 0, snake_list):
                        x_change = -block_size
                    elif not next_block_in_snake(x, y, block_size, 0, snake_list):
                        x_change = block_size
                elif y_change == -block_size:
                    if not next_block_in_snake(x, y, -block_size, 0, snake_list):
                        x_change = -block_size
                    elif not next_block_in_snake(x, y, block_size, 0, snake_list):
                        x_change = block_size

            # Heurystyka: obsługa do drogi do jabłka, zmiana tylko jeśli konieczna
            if x < food_x:
                if (x_change != block_size and y_change != 0):
                    x_change, y_change = block_size, 0
                else:
                    pass
            elif x > food_x:
                if (x_change != -block_size and y_change != 0):
                    x_change, y_change = -block_size, 0
                else:
                    pass
            elif y < food_y:
                if (x_change != 0 and y_change != block_size):
                    x_change, y_change = 0, block_size
                else:
                    pass
            elif y > food_y:
                if (x_change != 0 and y_change != -block_size):
                    x_change, y_change = 0, -block_size
                else:
                    pass

            clock.tick(fps)
            pygame.display.update()

        end_game('single', length_of_snake - 1, 0)
        pygame.quit()
        quit()

    gameLoop()

show_main_menu()