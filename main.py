import sys, pygame
from bricks import LineManager
from ball import Ball
from player import Paddle
from scoreboard import Scoreboard
import pygame.locals as K


class Game:
    # game object with game state machine, elements and variables.
    def __init__(self):
        pygame.init()
        # Game constants
        screen_size = (1280, 900)
        self.BG_COLOR = 0, 0, 0
        self.BRICK_SIZE = (80, 30)
        self.START_SPEED = 7.0

        # Game elements
        self.screen = pygame.display.set_mode(screen_size)
        self.MID_SCREEN = self.screen.get_size()[0] / 3, self.screen.get_size()[1] / 2
        self.ui_font = pygame.font.SysFont("monospace", 25, bold=True)
        self.ball = Ball(brick_size=self.BRICK_SIZE, start_speed=self.START_SPEED)
        self.paddle = Paddle(self.screen)
        self.scoreboard = Scoreboard()
        self.line_manager = None
        self.clock = pygame.time.Clock()

        # Game variables
        self.game_level = 15
        self.lives = 5
        self.player_name = ''
        self.game_status = 'login'

        # State machine dict
        self.GAME_STATES = {'login': self.login,
                            'start': self.start,
                            'play': self.play,
                            'catch': self.catch,
                            'level cleared': self.level_cleared,
                            'game over': self.game_over
                            }

    def flip_n_delay(self, delay):
        #   update display + delay
        pygame.display.flip()
        pygame.time.wait(delay)

    def blit_elements(self):
        #   update element states
        self.ball.blit_ball(self.screen)
        self.scoreboard.blit_board(self.screen)
        self.paddle.blit_paddle(self.screen)
        self.line_manager.blit_lines(self.screen)

    def login(self):
        #     create new Bricklines set, reset scoreboard & life. move to 'start'.
        pygame.key.set_repeat(500, 60)
        self.line_manager = LineManager(line_count=self.  game_level, screen=self.screen, brick_size=self.BRICK_SIZE)
        self.scoreboard.score = 0
        self.scoreboard.lives = self.lives
        self.screen.fill(self.BG_COLOR)
        if self.scoreboard.log_in(screen=self.screen, font=self.ui_font, mid_screen=self.MID_SCREEN) == 'start':
            self.game_status = 'start'

    def start(self):
        # display bricks, update line manager with new level, move to 'catch' state.
        self.screen.fill(self.BG_COLOR)
        self.scoreboard.blit_board(screen=self.screen)
        self.line_manager = LineManager(line_count=self.game_level, screen=self.screen, brick_size=self.BRICK_SIZE)
        self.line_manager.start_blit(self.screen)
        self.game_status = 'catch'
        self.ball.status = 'catch'
        self.clock.tick(60)

    def level_cleared(self):
        # Level up +1, reset ball speed, life +1, score + 2 x game level, move to 'start'.
        self.screen.fill(self.BG_COLOR)
        self.game_level += 1
        self.ball.speed = [self.START_SPEED, self.START_SPEED]
        self.scoreboard.lives += 1
        self.scoreboard.score += self.game_level * 2
        self.blit_elements()
        self.game_status = 'start'

    def catch(self):
        # paddle and ball movement on 'catch' state. update all elements.
        self.screen.fill(self.BG_COLOR)
        pygame.key.set_repeat(1, 3)
        self.game_status = self.paddle.update_status(line_manager=self.line_manager, ball=self.ball, scoreboard=self.scoreboard)
        self.ball.ball_move(screen=self.screen, line_manager=self.line_manager, paddle=self.paddle, scoreboard=self.scoreboard)
        self.blit_elements()
        self.clock.tick(60)

    def play(self):
        # paddle and ball on 'play' state, update all elements, if 0 lives check for new high score and move to 'game over' state.
        self.screen.fill(self.BG_COLOR)
        self.blit_elements()
        self.ball.ball_move(screen=self.screen, line_manager=self.line_manager, paddle=self.paddle, scoreboard=self.scoreboard)
        self.game_status = self.paddle.update_status(line_manager=self.line_manager, ball=self.ball, scoreboard=self.scoreboard)
        self.clock.tick(60)
        if self.scoreboard.lives == 0:
            self.screen.fill(self.BG_COLOR)
            self.blit_elements()
            self.scoreboard.game_over(self.screen)
            self.flip_n_delay(300)
            self.scoreboard.new_high(self.screen)
            self.flip_n_delay(500)
            self.game_status = 'game over'

    def game_over(self):
        # stop ball and paddle movement, announce game over, ask if new game - yes => 'login' no=> bye-bye function,
        self.scoreboard.game_over(self.screen)
        self.scoreboard.quit_question(self.screen)
        self.paddle.blit_paddle(self.screen)
        self.game_level = 3
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K.K_y:
                    self.scoreboard.player_name = ''
                    self.game_status = 'login'
                    pygame.time.wait(500)
                    pygame.event.clear()
                if event.key == K.K_n:
                    self.screen.fill(self.BG_COLOR)
                    self.scoreboard.babye(self.screen)
                    pygame.time.wait(2000)
                    sys.exit()
            if event.type == pygame.QUIT:
                sys.exit()


# create game object
game = Game()
while True:
    # execute Game function according to game status. update display.
    game.GAME_STATES[game.game_status]()
    pygame.display.flip()

