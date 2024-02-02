import pygame
import sys
import menu


def display_menu(screen, font, options):
    screen.fill((0, 0, 0))

    green = (0, 255, 0)

    title_text = font.render("Choose resolution:", True, green)
    screen.blit(title_text, (200, 100))

    option_rects = []

    button_height = 50
    spacing = 10

    for i, option in enumerate(options):
        option_text = font.render(option, True, (0, 0, 0))
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
        return pygame.display.list_modes()[0]

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
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for i, rect in enumerate(option_rects):
                if rect.collidepoint(mouse_x, mouse_y):
                    screen_size_option = options[i]

pygame.quit()

size = get_screen_size(screen_size_option)
menu.show_main_menu(size)
pygame.display.set_caption('SNAKE')


'''
[IDEAS]
 [] możliwośc zapauzowania i wznowienia gry
 [] dodanie dodatkowej muzyki (po najechaniu na kafelek)
 [] dodanie ramki do tekstu z punktami
 [] dodanie możliwości zalogowania
 [] dodanie wyboru customowej rozdzielczości
[ZREALIZOWANO]
 [X] możliwość wyboru wielkości ekranu
 [X] spowolnienie i zmiana prędkości wraz ze wzrostem punktów
 [X] wyświetlanie punktów w czasie rzeczywistym
 [X] dodanie muzyki
 [X] ekran końcowy z ilością punktów
 [X] możliwośc gry drugiego gracza po śmierci pierwszego
 [X] możliwośc zagrania ponownie po skończeniu gry
'''
