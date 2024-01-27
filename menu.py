import pygame
import sys
import single_player as SP
import multi_player as MP
import AI_snake as AI

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
                    SP.play_game()
                elif 400 <= x <= 600 and 270 <= y <= 320:
                    MP.play_game()
                elif 400 <= x <= 600 and 340 <= y <= 410:
                    AI.play_game()

        screen.fill(black)

        # Rysowanie przycisków
        pygame.draw.rect(screen, green, (400, 200, 200, 50))
        draw_text("SingleSnake", width // 2, 225, black)

        pygame.draw.rect(screen, green, (400, 270, 200, 50))
        draw_text("MultiSnake", width // 2, 295, black)

        pygame.draw.rect(screen, green, (400, 340, 200, 50))
        draw_text("AI-Snake", width // 2, 365, black)

        pygame.display.flip()

    # Zakończenie programu
    pygame.quit()
    sys.exit()

def end_game(mode : str):
    pygame.init()

    width, height = 1000, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("SNAKE")

    black = (0, 0, 0)
    green = (0, 255, 0)
    blue = (50, 153, 213)
    red = (230, 20, 20)

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
                        SP.play_game()
                    elif mode == "multi":
                        MP.play_game()
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
            draw_text("BLUE SNAKE POINTS: []", width // 4, 200, blue)
            draw_text("GREEN SNAKE POINTS: []", (width // 4) * 3, 200, green)
        elif mode == 'single':
            draw_text("POINTS: []", width // 2, 200, green)

        pygame.display.flip()

    # Zakończenie programu
    pygame.quit()
    sys.exit()
    