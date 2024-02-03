import pygame
import random
import os


def ai_play_game(size):

    pygame.init()

    width, height = size[0], size[1]
    block_size = 20
    fps = 15

    black = (0, 0, 0)
    red = (230, 20, 20)
    green = (0, 255, 0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Snake-AI')

    main_theme = pygame.mixer.Sound(os.getcwd() + '\\sounds\\sound_track.mp3')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(main_theme, loops=-1)

    get_point = pygame.mixer.Sound(os.getcwd() + '\\sounds\\get_point.mp3')
    channel1 = pygame.mixer.Channel(1)

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
                channel1.play(get_point)

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

        end_game('ai',length_of_snake - 1, 0,size)
        pygame.quit()

    gameLoop()

def mp_play_game(size):

    pygame.init()

    width, height = size[0], size[1]
    block_size = 20
    fps = 15

    black = (0, 0, 0)
    red = (230, 20, 20)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('MultiPlayer Snake Game')

    main_theme = pygame.mixer.Sound(os.getcwd() + '\\sounds\\sound_track.mp3')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(main_theme, loops=-1)

    get_point = pygame.mixer.Sound(os.getcwd() + '\\sounds\\get_point.mp3')
    channel1 = pygame.mixer.Channel(1)

    clock = pygame.time.Clock()

    def display_points(b_points,g_points):
        font = pygame.font.Font(None, 36)
        blue_text_surface = font.render(f"Points: {b_points}", True, blue)
        green_text_surface = font.render(f"Points: {g_points}",True,green)
        blue_text_rect = blue_text_surface.get_rect(topleft=(10,10))
        screen.blit(blue_text_surface, blue_text_rect)
        green_text_rect = green_text_surface.get_rect(topright=(width-10, 10))
        screen.blit(green_text_surface, green_text_rect)

    def pause_game(current_direction_green, current_direction_blue):
        paused = True
        pause_font = pygame.font.Font(None, 72)
        toggle_text = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

            clock.tick(5)
            pause_text = pause_font.render("GAME PAUSED", True, black)
            screen.blit(pause_text,
                        (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))

            if toggle_text:
                pause_text = pause_font.render("GAME PAUSED", True, green)
                screen.blit(pause_text,
                            (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))

            toggle_text = not toggle_text

            pygame.display.update()

        return paused, current_direction_green,current_direction_blue



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
        game_paused = False
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
        food_x2, food_y2 = generate_food_position(green_snake_list, blue_snake_list, food_x1, food_y1)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_paused, last_direction_green, last_direction_blue = pause_game((x_green_change, y_green_change),(x_blue_change,y_blue_change))

                    if not game_paused:
                        if not game_over_green:
                            if green_first_move:
                                # Pierwszy ruch zielonego
                                if event.key == pygame.K_UP:
                                    x_green_change, y_green_change = 0, -block_size
                                    green_first_move = False
                                elif event.key == pygame.K_DOWN:
                                    x_green_change, y_green_change = 0, block_size
                                    green_first_move = False
                                elif event.key == pygame.K_LEFT:
                                    x_green_change, y_green_change = -block_size, 0
                                    green_first_move = False
                                elif event.key == pygame.K_RIGHT:
                                    x_green_change, y_green_change = block_size, 0
                                    green_first_move = False
                            else:
                                # Nie pierwszy ruch zielonego
                                if event.key == pygame.K_UP and not green_first_move and (
                                        x_green_change != 0 and y_green_change != -block_size):
                                    x_green_change, y_green_change = 0, -block_size
                                elif event.key == pygame.K_DOWN and not green_first_move and (
                                        x_green_change != 0 and y_green_change != block_size):
                                    x_green_change, y_green_change = 0, block_size
                                elif event.key == pygame.K_LEFT and not green_first_move and (
                                        x_green_change != -block_size and y_green_change != 0):
                                    x_green_change, y_green_change = -block_size, 0
                                elif event.key == pygame.K_RIGHT and not green_first_move and (
                                        x_green_change != -block_size and y_green_change != 0):
                                    x_green_change, y_green_change = block_size, 0

                        if not game_over_blue:
                            if blue_first_move:
                                # Pierwszy ruch niebieskiego
                                if event.key == pygame.K_w:
                                    x_blue_change, y_blue_change = 0, -block_size
                                    blue_first_move = False
                                elif event.key == pygame.K_s:
                                    x_blue_change, y_blue_change = 0, block_size
                                    blue_first_move = False
                                elif event.key == pygame.K_a:
                                    x_blue_change, y_blue_change = -block_size, 0
                                    blue_first_move = False
                                elif event.key == pygame.K_d:
                                    blue_first_move = False
                                    x_blue_change, y_blue_change = block_size, 0
                            else:
                                # Nie pierwszy ruch niebieskiego
                                if event.key == pygame.K_w and not blue_first_move and (x_blue_change != 0 and y_blue_change != -block_size):
                                    x_blue_change, y_blue_change = 0, -block_size
                                elif event.key == pygame.K_s and not blue_first_move and (x_blue_change != 0 and y_blue_change != block_size):
                                    x_blue_change, y_blue_change = 0, block_size
                                elif event.key == pygame.K_a and not blue_first_move and (x_blue_change != -block_size and y_blue_change != 0):
                                    x_blue_change, y_blue_change = -block_size, 0
                                elif event.key == pygame.K_d and not blue_first_move and (x_blue_change != -block_size and y_blue_change != 0):
                                    x_blue_change, y_blue_change = block_size, 0

            if not game_paused:
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

            display_points(length_of_blue_snake - 1, length_of_green_snake - 1)

            pygame.display.flip()

            # Zielony zjada jedzenie1
            if x_green == food_x1 and y_green == food_y1:
                food_x1, food_y1 = generate_food_position(green_snake_list, blue_snake_list, food_x2, food_y2)
                length_of_green_snake += 1
                channel1.play(get_point)

            # Zielony zjada jedzenie2
            if x_green == food_x2 and y_green == food_y2:
                food_x2, food_y2 = generate_food_position(green_snake_list, blue_snake_list, food_x1, food_x2)
                length_of_green_snake += 1
                channel1.play(get_point)

            # Niebieski zjada jedzenie1
            if x_blue == food_x1 and y_blue == food_y1:
                food_x1, food_y1 = generate_food_position(green_snake_list, blue_snake_list, food_x2, food_y2)
                length_of_blue_snake += 1
                channel1.play(get_point)

            # Niebieski zjada jedzenie2
            if x_blue == food_x2 and y_blue == food_y2:
                food_x2, food_y2 = generate_food_position(green_snake_list, blue_snake_list, food_x1, food_y1)
                length_of_blue_snake += 1
                channel1.play(get_point)

            if game_over_green and game_over_blue:
                game_over = True

            clock.tick(fps)
            pygame.display.update()

        end_game('multi', length_of_green_snake - 1, length_of_blue_snake - 1, size)
        pygame.quit()

    gameLoop()

def sp_play_game(size):

    pygame.init()

    width, height = size[0], size[1]
    block_size = 20

    black = (0, 0, 0)
    red = (230, 20, 20)
    green = (0, 255, 0)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('SinglePlayer Snake Game')


    main_theme = pygame.mixer.Sound(os.getcwd() + '\\sounds\\sound_track.mp3')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(main_theme, loops=-1)

    get_point = pygame.mixer.Sound(os.getcwd() + '\\sounds\\get_point.mp3')
    channel1 = pygame.mixer.Channel(1)

    clock = pygame.time.Clock()

    def pause_game(current_direction):
        paused = True
        pause_font = pygame.font.Font(None, 72)
        toggle_text = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False

            clock.tick(5)
            pause_text = pause_font.render("GAME PAUSED", True, black)
            screen.blit(pause_text,
                        (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))

            if toggle_text:
                pause_text = pause_font.render("GAME PAUSED", True, green)
                screen.blit(pause_text,
                            (width // 2 - pause_text.get_width() // 2, height // 2 - pause_text.get_height() // 2))

            toggle_text = not toggle_text

            pygame.display.update()

        return paused, current_direction

    def display_points(points,color):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Points: {points}", True, color)
        text_rect = text_surface.get_rect(topleft=(10, 10))
        screen.blit(text_surface, text_rect)

    def generate_food_position(snake_list):
        while True:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0
            if [food_x, food_y] not in snake_list:
                return food_x, food_y
    def gameLoop():
        fps = 12
        game_over = False
        game_paused = False
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
                    if event.key == pygame.K_ESCAPE:
                        game_paused, last_direction = pause_game((x_change, y_change))

                    if not game_paused:
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

            if not game_paused:
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

            display_points(length_of_snake - 1,green)

            pygame.display.update()

            if x == food_x and y == food_y:
                food_x, food_y = generate_food_position(snake_list)
                length_of_snake += 1
                channel1.play(get_point)
                if fps < 20:
                    fps += 2

            clock.tick(fps)
            pygame.display.update()

        end_game('single', length_of_snake - 1, 0,size)
        pygame.quit()
        quit()

    gameLoop()

def show_main_menu(size):
    pygame.init()

    width, height = size[0], size[1]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("SNAKE")

    main_theme = pygame.mixer.Sound(os.getcwd() + '\\sounds\\sound_track.mp3')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(main_theme, loops=-1)

    black = (0, 0, 0)
    green = (0, 255, 0)

    font = pygame.font.Font(None, 36)

    def draw_text(text, x, y, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    def scale_factor(factor):
        return int(factor * min(width, height) / 800)

    # Główna pętla programu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                button_height = scale_factor(50)
                button_y_offset = scale_factor(70)


                if width // 2 - scale_factor(100) <= x <= width // 2 + scale_factor(100):
                    if height // 2 - button_y_offset <= y <= height // 2 - button_y_offset + button_height:
                        sp_play_game(size)
                    elif height // 2 <= y <= height // 2 + button_height:
                        mp_play_game(size)
                    elif height // 2 + button_y_offset <= y <= height // 2 + button_y_offset + button_height:
                        ai_play_game(size)
                    elif height // 2 + 3 * button_y_offset <= y <= height // 2 + 3 * button_y_offset + button_height:
                        pygame.quit()
                        quit()

        screen.fill(black)

        title_font = pygame.font.Font(None, scale_factor(300))
        title_text = title_font.render("SNAKE", True, green)
        title_rect = title_text.get_rect(center=(width // 2, scale_factor(100)))
        screen.blit(title_text, title_rect)

        subtitle_font = pygame.font.Font(None, scale_factor(25))
        subtitle_text = subtitle_font.render("by Jacob Digital Entertainment", True, green)
        subtitle_rect = subtitle_text.get_rect(center=(width // 2, scale_factor(190)))
        screen.blit(subtitle_text, subtitle_rect)


        button_height = scale_factor(50)
        button_y_offset = scale_factor(70)

        pygame.draw.rect(screen, green, (
        width // 2 - scale_factor(100), height // 2 - button_y_offset, scale_factor(200), button_height))
        draw_text("SingleSnake", width // 2, height // 2 - button_y_offset + button_height // 2, black)

        pygame.draw.rect(screen, green, (width // 2 - scale_factor(100), height // 2, scale_factor(200), button_height))
        draw_text("MultiSnake", width // 2, height // 2 + button_height // 2, black)

        pygame.draw.rect(screen, green, (
        width // 2 - scale_factor(100), height // 2 + button_y_offset, scale_factor(200), button_height))
        draw_text("AI-Snake", width // 2, height // 2 + button_y_offset + button_height // 2, black)

        pygame.draw.rect(screen, green, (
        width // 2 - scale_factor(100), height // 2 + 3 * button_y_offset, scale_factor(200), button_height))
        draw_text("Exit", width // 2, height // 2 + 3 * button_y_offset + button_height // 2, black)

        pygame.display.flip()

    pygame.quit()

def end_game(mode : str, green_points, blue_points,size):
    pygame.init()

    width, height = size[0], size[1]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("SNAKE")

    game_over_sound = pygame.mixer.Sound(os.getcwd() + '\\sounds\\game_over.mp3')
    channel0 = pygame.mixer.Channel(0)
    channel0.play(game_over_sound)

    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    font = pygame.font.Font(None, 36)

    def draw_text(text, x, y, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    def scale_factor(factor):
        return int(factor * min(width, height) / 800)

    # Główna pętla programu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                button_height = scale_factor(50)
                button_y_offset = scale_factor(70)

                if width // 2 - scale_factor(100) <= x <= width // 2 + scale_factor(100):
                    if height // 2 - button_y_offset <= y <= height // 2 - button_y_offset + button_height:
                        if mode == "single":
                            sp_play_game(size)
                        elif mode == "multi":
                            mp_play_game(size)
                        elif mode == 'ai':
                            ai_play_game(size)
                    elif height // 2 <= y <= height // 2 + button_height:
                        show_main_menu(size)
                    elif height // 2 + button_y_offset <= y <= height // 2 + button_y_offset + button_height:
                        pygame.quit()
                        quit()

        screen.fill(black)

        button_height = scale_factor(50)
        button_y_offset = scale_factor(70)

        pygame.draw.rect(screen, green, (
        width // 2 - scale_factor(100), height // 2 - button_y_offset, scale_factor(200), button_height))
        draw_text("Play again", width // 2, height // 2 - button_y_offset + button_height // 2, black)

        pygame.draw.rect(screen, green, (width // 2 - scale_factor(100), height // 2, scale_factor(200), button_height))
        draw_text("Main menu", width // 2, height // 2 + button_height // 2, black)

        pygame.draw.rect(screen, green, (
        width // 2 - scale_factor(100), height // 2 + button_y_offset, scale_factor(200), button_height))
        draw_text("Exit", width // 2, height // 2 + button_y_offset + button_height // 2, black)

        draw_text("GAME OVER", width // 2, scale_factor(100), green)
        if mode == 'multi':
            draw_text(f"BLUE SNAKE POINTS: {blue_points}", scale_factor(250), scale_factor(200), blue)
            draw_text(f"GREEN SNAKE POINTS: {green_points}", width - scale_factor(250), scale_factor(200), green)
        elif mode == 'single' or mode == 'ai':
            draw_text(f"POINTS: {green_points}", width // 2, scale_factor(200), green)

        pygame.display.flip()

    # Zakończenie programu
    pygame.quit()

def display_menu(screen, font, options):

    black = (0, 0, 0)
    green = (0, 255, 0)

    screen.fill(black)

    title_text = font.render("Choose resolution:", True, green)
    screen.blit(title_text, (200, 100))

    option_rects = []

    button_height = 50
    spacing = 10

    for i, option in enumerate(options):
        option_text = font.render(option, True, black)
        rect = pygame.Rect(200, 200 + i * (button_height + spacing), 200, button_height)
        pygame.draw.rect(screen, green, rect)
        screen.blit(option_text, rect.move(10, 10).topleft)
        option_rects.append(rect)

    pygame.display.flip()
    return option_rects

def get_screen_size(option):
    pygame.init()
    if option == "800x600":
        return (800, 600)
    elif option == "1000x800":
        return (1000, 800)
    elif option == "1280x720":
        return (1280, 720)
    elif option == "Fullscreen":
        info = pygame.display.Info()
        fullscreen_width = ((info.current_w + 19) // 20) * 20
        fullscreen_height = ((info.current_h + 19) // 20) * 20
        return (fullscreen_width,fullscreen_height)

pygame.init()

options = ["800x600", "1000x800", "1280x720", "Fullscreen"]
screen_size_option = None

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Snake Game')

font = pygame.font.Font(None, 36)

while not screen_size_option:
    option_rects = display_menu(screen, font, options)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_x, mouse_y):
                    screen_size_option = options[i]

pygame.quit()

size = get_screen_size(screen_size_option)
show_main_menu(size)
pygame.display.set_caption('SNAKE')
