import sys, pygame
from bricks import LineManager
from ball import Ball
from player import Paddle
from scoreboard import Scoreboard
import pygame.locals as K

pygame.init()

SCREEN_SIZE = width, height = 1280, 900
BG_COLOR = 0, 0, 0
BRICK_SIZE = (80, 30)
START_SPEED = 7.0
screen = pygame.display.set_mode(SCREEN_SIZE)
MID_SCREEN = screen.get_size()[0] / 3, screen.get_size()[1] / 2
game_level = 3
lives = 5

ball = Ball(brick_size=BRICK_SIZE, start_speed=START_SPEED)
paddle = Paddle(screen)
scoreboard = Scoreboard()

ui_font = pygame.font.SysFont("monospace", 25, bold=True)
player_name = ''
game_status = 'login'
clock = pygame.time.Clock()


def flip_n_delay(delay):
    pygame.display.flip()
    pygame.time.wait(delay)


while True:

    if game_status == 'login':
        line_manager = LineManager(line_count=game_level, screen=screen, brick_size=BRICK_SIZE)
        scoreboard.score = 0
        scoreboard.lives = lives
        pygame.key.set_repeat(500, 60)
        screen.fill(BG_COLOR)
        if scoreboard.log_in(screen=screen, font=ui_font, mid_screen=MID_SCREEN) == 'start':
            game_status = 'start'

    elif game_status == 'start':
        screen.fill(BG_COLOR)
        scoreboard.blit_board(screen=screen)
        line_manager = LineManager(line_count=game_level, screen=screen, brick_size=BRICK_SIZE)
        line_manager.start_blit(screen)
        game_status = 'catch'
        ball.status = 'catch'
        clock.tick(60)

    elif game_status == 'level cleared':
        game_level += 1
        ball.speed = [START_SPEED, START_SPEED]
        ball.blit_ball(screen)
        scoreboard.lives += 1
        scoreboard.score += game_level * 2
        game_status = 'start'

    elif game_status == 'catch':
        screen.fill(BG_COLOR)
        pygame.key.set_repeat(1, 3)
        game_status = paddle.update_status(screen=screen, line_manager=line_manager, ball=ball, scoreboard=scoreboard)
        ball.ball_move(screen=screen, line_manager=line_manager, paddle=paddle, scoreboard=scoreboard)
        line_manager.blit_lines(screen=screen)
        scoreboard.blit_board(screen=screen)
        clock.tick(60)

    elif game_status == 'play':
        screen.fill(BG_COLOR)
        line_manager.blit_lines(screen=screen)
        scoreboard.blit_board(screen=screen)
        ball.ball_move(screen=screen, line_manager=line_manager, paddle=paddle, scoreboard=scoreboard)
        game_status = paddle.update_status(screen=screen, line_manager=line_manager, ball=ball, scoreboard=scoreboard)
        if scoreboard.lives == 0:
            screen.fill(BG_COLOR)
            paddle.blit_paddle(screen)
            scoreboard.blit_board(screen)
            line_manager.blit_lines(screen)
            scoreboard.game_over(screen)
            flip_n_delay(300)
            scoreboard.new_high(screen)
            flip_n_delay(500)
            game_status = 'game over'
        clock.tick(60)

    elif game_status == 'game over':
        scoreboard.game_over(screen)
        scoreboard.quit_question(screen)
        paddle.blit_paddle(screen)
        game_level = 3
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K.K_y:
                    scoreboard.player_name = ''
                    game_status = 'login'
                    pygame.time.wait(500)
                    pygame.event.clear()
                if event.key == K.K_n:
                    screen.fill(BG_COLOR)
                    scoreboard.babye(screen)
                    pygame.time.wait(2000)
                    sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()

    pygame.display.flip()
