import os
import pygame
import single_player as SP
import multi_player as MP
import AI_snake as AI

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
                        SP.sp_play_game(size)
                    elif height // 2 <= y <= height // 2 + button_height:
                        MP.mp_play_game(size)
                    elif height // 2 + button_y_offset <= y <= height // 2 + button_y_offset + button_height:
                        AI.ai_play_game(size)
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
                            SP.sp_play_game(size)
                        elif mode == "multi":
                            MP.mp_play_game(size)
                        elif mode == 'ai':
                            AI.ai_play_game(size)
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