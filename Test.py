import pygame

pygame.init()

screen = pygame.display.set_mode((800, 500))

running = True
fill_color = (255, 255, 255)


def check_left_right(line_rect, point):
    return ((line_rect.width - line_rect.x) * (point[0] - line_rect.y) -
            (line_rect.height - line_rect.y) * (point[1] - line_rect.y)) > 0


while running:

    screen.fill(fill_color)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()

    rect = pygame.draw.rect(screen, (0, 0, 200), (100, 100, 250, 250))

    start_pos = (mouse_pos[0] - 100, mouse_pos[1] - 100)
    end_pos = (mouse_pos[0] + 100, mouse_pos[1] + 100)

    line_rect = pygame.draw.line(screen, (0, 200, 0), start_pos, end_pos, width=3)

    if line_rect.colliderect(rect):
        print("Collision: ", check_left_right(line_rect, rect.topleft))

        center = line_rect.center

        if center >= rect.topleft and center <= rect.bottomright:
            print("Collision22")
            fill_color = (255, 0, 0)

    else:
        fill_color = (255, 255, 255)

    pygame.display.flip()