import pygame
import random
import menu
import os

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

        menu.end_game('multi', length_of_green_snake - 1, length_of_blue_snake - 1, size)
        pygame.quit()

    gameLoop()