import pygame


class Ball:
    """Game Ball class"""
    def __init__(self, brick_size, start_speed):
        self.ball = pygame.image.load("img/ball_img.png")
        self.ball = pygame.transform.scale(self.ball, (12, 12))
        self.ballrect = self.ball.get_rect()
        self.speed = [0, 0]
        self.brick_size = brick_size
        self.status = 'catch'
        self.n_paddle_bounce = 0
        self.start_speed = start_speed

    def ball_move(self, screen, line_manager, paddle, scoreboard):
        """Ball movement fanctions:
        General movement.
        Catch / Release flags.
        Bouncing of walls / paddle / bricks.
        """

        def screen_bounce():
            """ ball bounce off screen boundaries.
            bottom boundary hit takes 1 life & switches ball & paddle 'catch' state.
            """

            if self.ballrect.left < 2 or self.ballrect.right > screen.get_size()[0] - 2:
                self.speed[0] = -self.speed[0]
            elif self.ballrect.top < 2:
                self.speed[1] = -self.speed[1]
            elif self.ballrect.bottom > screen.get_size()[1] - 2:
                scoreboard.lives -= 1
                scoreboard.blit_board(screen)
                pygame.event.clear()
                pygame.time.wait(1000)
                self.status = 'catch'
                paddle.status = 'catch'

        def brick_bounce():
            """ Checks ball collision with bricks &
            bounces ball accordingly, adding points relative to brick position.
            Removes brick that got hit and updates brick count in brick line manager object
            """

            line_index = 0
            for line in line_manager.brick_lines:
                line_index += 1
                for brick in line.brick_line:
                    collide = self.ballrect.colliderect(brick.brick_rect)
                    left = self.ballrect.right >= brick.brick_rect.left
                    right = self.ballrect.left <= brick.brick_rect.right
                    in_width = brick.brick_rect.left <= self.ballrect.x <= brick.brick_rect.right
                    top = self.ballrect.bottom >= brick.brick_rect.top and in_width
                    bottom = self.ballrect.top <= brick.brick_rect.bottom and in_width
                    if collide:
                        if top or bottom:
                            self.speed[1] = -self.speed[1]
                        elif left or right:
                            self.speed[0] = -self.speed[0]
                        line.brick_line.remove(brick)
                        scoreboard.score += 1 * (len(line_manager.brick_lines) - line_index + 1)
                        line_manager.brick_count -= 1

        def paddle_bounce():
            """ Bounces ball off paddle to opposite direction according to the paddle side."""

            collide_l = self.ballrect.colliderect(paddle.paddle_rect) and \
                        paddle.paddle_rect.left+3 < self.ballrect.x <= paddle.paddle_rect.center[0]
            collide_r = self.ballrect.colliderect(paddle.paddle_rect) and \
                        paddle.paddle_rect.center[0] < self.ballrect.x < paddle.paddle_rect.right-3
            in_width = paddle.paddle_rect.left < self.ballrect.x < paddle.paddle_rect.right
            if collide_r and in_width:
                self.speed = [abs(self.speed[0]), -self.speed[1]]
                self.n_paddle_bounce += 1
                pygame.event.clear()
            elif collide_l and in_width:
                self.speed = [-abs(self.speed[0]), -self.speed[1]]
                self.n_paddle_bounce += 1
                pygame.event.clear()

        def ball_play():
            """ A function for repetitive ball movement and check of any ball bouncing."""

            self.ballrect = self.ballrect.move(self.speed)
            brick_bounce()
            screen_bounce()
            paddle_bounce()
            # every n paddle-bounces, ball speeds-up and brick lines are lowered.
            if self.n_paddle_bounce == 5:
                for line in line_manager.brick_lines:
                    for brick in line.brick_line:
                        brick.brick_rect.bottom += brick.brick_rect.height
                if line_manager.brick_count > 0:
                    line_manager.get_bottom()
                line_manager.blit_lines(screen)
                self.speed[1] -= 0.33
                if self.speed[0] > 0:
                    self.speed[0] += 0.33
                elif self.speed[0] < 0:
                    self.speed[0] -= 0.33
                self.n_paddle_bounce = 0

        def ball_catch():
            """ Switches to catch state - 0 speed and position ball on paddle."""

            self.speed = [0, 0]
            self.ballrect.x = paddle.paddle_rect.center[0]
            self.ballrect.bottom = paddle.paddle_rect.top

        if self.status == 'play':
            ball_play()
        elif self.status == 'catch':
            ball_catch()

    def release(self):
        """ Starts ball movement with ball starting speed."""

        self.speed = [self.start_speed, -self.start_speed]
        self.status = 'play'

    def blit_ball(self, screen):
        """Repetitive function for Re-rendering ball position using pygame blit function"""
        screen.blit(self.ball, self.ballrect)

