from typing import Tuple

import pygame
import Tank as pl
from controller import Controller
import background as bg
import assets


def checkWallCollision(points: Tuple[int, int, int, int]):
    return any((wall_coll1.rect_collide(points)[0], wall_coll2.rect_collide(points)[0],
                wall_coll3.rect_collide(points)[0], wall_coll4.rect_collide(points)[0],
               wall_coll5.rect_collide(points)[0], wall_coll6.rect_collide(points)[0]))


def update_spawn_pos():
    global spawn_lst
    bg_rect = background.getPos()
    pre_bg = background.previousPos()
    bg_x, bg_y = bg_rect[0] - pre_bg[0], bg_rect[1] - pre_bg[1]
    spawn_lst = [(bg_x + x[0], bg_y + x[1]) for x in spawn_lst]


def main():

    global running, max_enemy

    time = 0
    game_over = False
    score = 0

    time_rect = pygame.Rect(50, 50, 100, 100)
    score_rect = pygame.Rect(50, 50, 100, 100)

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                player.fire(event.pos)

            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                game_over = False
                max_enemy = 1
                score = 0
                time = 0

        if not game_over:
            key_press = pygame.key.get_pressed()

            background.resetprevPos()
            # background.keyEvent(key_press, player.pos())

            player.keyEvent(key_press)
            player.mouseEvent(pygame.mouse.get_pos())

            if controller.getEnemyCount() < max_enemy or (time + 1) % 8500 == 0:
                controller.spawnEnemy()

            if score < controller.getScore():
                score = controller.getScore()

            if (score+1) % 25 == 0:
                max_enemy += 1
                score += 1

            if checkWallCollision(player.getBbox()):
                player.resetPreviousPos()
                background.resetPreviousPos()
                background.resetprevPos()

            controller.setSpawnlst(spawn_lst)

            time += 1

            if controller.getLives() == 0:
                game_over = True
                score = controller.getScore()
                controller.reset()

            update_spawn_pos()
            controller.setBgPos(background.getPos(), background.previousPos())

        background.update()
        controller.update()

        for x in range(controller.getLives()):
            screen.blit(life_image, (50 + ((life_image.get_width() + 10) * x), 10))

        time_rect = screen.blit(score_font.render(f"{time}", True, (255, 255, 255)),
                                (screen.get_width()-time_rect.width-100, 20))
        score_rect = screen.blit(score_font.render(f"Kills: {controller.getScore()}", True, (255, 255, 255)),
                                 (screen.get_width()-score_rect.width-100, 50))

        if game_over:
            screen.blit(game_over_font.render("GAME OVER", True, (255, 255, 255)), (300, 50))
            screen.blit(game_over_font.render(f"SCORE: {score}", True, (255, 255, 255)), (350, 200))
            screen.blit(game_over_font.render("Click anywhere to restart", True, (255, 255, 255)), (200, 300))

        pygame.display.update()


if __name__ == "__main__":

    pygame.init()
    pygame.display.set_caption("Tank Game")
    pygame.display.set_icon( pygame.image.load(assets.PLAYER_TANK))

    screen = pygame.display.set_mode((900, 700))

    running = True

    max_enemy = 1
    lives = 3

    life_image = pygame.image.load(assets.LIFE)

    controller = Controller(screen, lives=lives)
    player = pl.Player(assets.PLAYER_TANK, screen, (250, 200), controller=controller, speed=2, fire_speed=2,
                       fire_delay=100, fire_radius=250)

    controller.setPlayer(player)

    background = bg.Background(assets.BACKGROUND, screen, (-5, -5))
    bg_rect = background.getRect()

    split = (20, 20)

    backg_wall = bg.BackgroundWall(assets.BACKGROUND_WALL1, screen, bg_rect, (0, 0), split=split)
    wall_coll1 = backg_wall.getCollisionObject()

    backg_wall2 = bg.BackgroundWall(assets.BACKGROUND_WALL2, screen, bg_rect, split=split)
    rect = backg_wall2.get_rect()
    backg_wall2.setPos(bg_rect.width - rect.width, 0)
    wall_coll2 = backg_wall2.getCollisionObject()

    backg_wall3 = bg.BackgroundWall(assets.BACKGROUND_WALL3, screen, bg_rect, split=split)
    rect = backg_wall3.get_rect()
    backg_wall3.setPos(0, bg_rect.height - rect.height)
    wall_coll3 = backg_wall3.getCollisionObject()

    backg_wall4 = bg.BackgroundWall(assets.BACKGROUND_WALL4, screen, bg_rect, split=split)
    rect = backg_wall4.get_rect()
    backg_wall4.setPos(bg_rect.width - rect.width, bg_rect.height - rect.height)
    wall_coll4 = backg_wall4.getCollisionObject()

    backg_wall5 = bg.BackgroundWall(assets.BACKGROUND_WALL5, screen, bg_rect, split=split)
    backg_wall5.setPos(400, 400)
    wall_coll5 = backg_wall5.getCollisionObject()

    backg_wall6 = bg.BackgroundWall(assets.BACKGROUND_WALL6, screen, bg_rect, split=split)
    backg_wall6.setPos(500, 150)
    wall_coll6 = backg_wall6.getCollisionObject()

    for wall in [(backg_wall, wall_coll1), (backg_wall2, wall_coll2), (backg_wall3, wall_coll3),
                 (backg_wall4, wall_coll4), (backg_wall5, wall_coll5), (backg_wall6, wall_coll6)]:

        controller.addObstacle(*wall)

    spawn_lst = [(650, 120), (250, 450), (650, 450)]

    controller.setSpawnlst(spawn_lst)

    game_over_font = pygame.font.SysFont('Times', 50, True)
    score_font = pygame.font.SysFont('Consolas', 30)
    main()
