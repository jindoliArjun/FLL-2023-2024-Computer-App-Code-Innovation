import pygame

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

title_font = pygame.font.SysFont("Arial", 64)
button_font = pygame.font.SysFont("Arial", 32)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_RADIUS = 25
BUTTON_MARGIN = 20
BACK_WIDTH = 100
BACK_HEIGHT = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

pygame.display.set_caption("Pygame Example")

clock = pygame.time.Clock()

page = 0

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.VIDEORESIZE:
            SCREEN_WIDTH = event.w
            SCREEN_HEIGHT = event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if page == 0:
                for i in range(4):
                    button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
                    button_y = SCREEN_HEIGHT // 2 - (2 - i) * (BUTTON_HEIGHT + BUTTON_MARGIN)
                    if (mouse_x > button_x - BUTTON_RADIUS and mouse_x < button_x + BUTTON_WIDTH + BUTTON_RADIUS and
                        mouse_y > button_y and mouse_y < button_y + BUTTON_HEIGHT):
                        page = i + 1

            else:
                back_x = SCREEN_WIDTH // 2 - BACK_WIDTH // 2
                back_y = SCREEN_HEIGHT - BACK_HEIGHT - BUTTON_MARGIN
                if (mouse_x > back_x and mouse_x < back_x + BACK_WIDTH and
                    mouse_y > back_y and mouse_y < back_y + BACK_HEIGHT):
                    page = 0

    screen.fill(WHITE)

    if page == 0:
        title_text = title_font.render("Title", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        for i in range(4):
            button_x = SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2
            button_y = SCREEN_HEIGHT // 2 - (2 - i) * (BUTTON_HEIGHT + BUTTON_MARGIN)
            pygame.draw.rect(screen, RED, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
            pygame.draw.circle(screen, RED, (button_x, button_y + BUTTON_HEIGHT // 2), BUTTON_RADIUS)
            pygame.draw.circle(screen, RED, (button_x + BUTTON_WIDTH, button_y + BUTTON_HEIGHT // 2), BUTTON_RADIUS)
            button_text = button_font.render(f"Button {i + 1}", True, WHITE)
            button_rect = button_text.get_rect(center=(button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))
            screen.blit(button_text, button_rect)

    else:
        title_text = title_font.render(f"Title {page}", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)

        back_x = SCREEN_WIDTH // 2 - BACK_WIDTH // 2
        back_y = SCREEN_HEIGHT - BACK_HEIGHT - BUTTON_MARGIN
        pygame.draw.rect(screen, GREEN, (back_x, back_y, BACK_WIDTH, BACK_HEIGHT))
        back_text = button_font.render("BACK", True, WHITE)
        back_rect = back_text.get_rect(center=(back_x + BACK_WIDTH // 2, back_y + BACK_HEIGHT // 2))
        screen.blit(back_text, back_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
