import pygame
import random
import menu

def play_game():

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

        menu.end_game('single', length_of_snake - 1, 0)
        pygame.quit()
        quit()

    gameLoop()
