import pygame
import sys
import single_player as SP
import multi_player as MP
import AI_snake as AI

pygame.init()

width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SNAKE")

black = (0, 0, 0)
red = (230, 20, 20)
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
            if 400 <= x <= 600 and 50 <= y <= 100:
                SP.play_game()
            elif 400 <= x <= 600 and 120 <= y <= 170:
                MP.play_game()
            elif 400 <= x <= 600 and 190 <= y <= 240:
                AI.play_game()

    screen.fill(black)

    # Rysowanie przycisków
    pygame.draw.rect(screen, green, (400, 50, 200, 50))
    draw_text("Singleplayer", width // 2, 75, black)

    pygame.draw.rect(screen, green, (400, 120, 200, 50))
    draw_text("Multiplayer", width // 2, 145, black)

    pygame.draw.rect(screen, green, (400, 190, 200, 50))
    draw_text("Snake-AI", width // 2, 215, black)

    pygame.display.flip()

# Zakończenie programu
pygame.quit()
sys.exit()
