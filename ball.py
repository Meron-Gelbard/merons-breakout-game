import pygame

class Ball:
    def __init__(self, brick_size, start_speed):
        self.ball = pygame.image.load("img/ball_img.png")
        self.ball = pygame.transform.scale(self.ball, (12, 12))
        self.ballrect = self.ball.get_rect()
        self.speed = [0, 0]
        self.brick_size = brick_size
        self.status = 'catch'
        self.paddle_bounce = 0
        self.start_speed = start_speed

    def ball_move(self, screen, line_manager, paddle, scoreboard):
        def screen_bounce():
            screen_width = screen.get_size()[0]
            screen_height = screen.get_size()[1]
            if self.ballrect.left < 2 or self.ballrect.right > screen_width - 2:
                self.speed[0] = -self.speed[0]
            elif self.ballrect.top < 2:
                self.speed[1] = -self.speed[1]
            elif self.ballrect.bottom > screen_height - 2:
                scoreboard.lives -= 1
                scoreboard.blit_board(screen)
                pygame.time.wait(1000)
                self.status = 'catch'
                paddle.status = 'catch'

        def brick_bounce():
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
            collide_l = self.ballrect.colliderect(paddle.paddle_rect) and \
                        paddle.paddle_rect.left < self.ballrect.x < paddle.paddle_rect.center[0]
            collide_r = self.ballrect.colliderect(paddle.paddle_rect) and \
                        paddle.paddle_rect.center[0] < self.ballrect.x < paddle.paddle_rect.right
            if collide_r:
                self.speed = [abs(self.speed[0]), -self.speed[1]]
                self.paddle_bounce += 1
            elif collide_l:
                self.speed = [-abs(self.speed[0]), -self.speed[1]]
                self.paddle_bounce += 1

        def ball_play():
            self.ballrect = self.ballrect.move(self.speed)
            brick_bounce()
            screen_bounce()
            paddle_bounce()
            # screen.blit(self.ball, self.ballrect)
            if self.paddle_bounce == 5:
                for line in line_manager.brick_lines:
                    for brick in line.brick_line:
                        brick.brick_rect.bottom += brick.brick_rect.height
                line_manager.get_bottom()
                line_manager.blit_lines(screen)
                self.speed[1] -= 0.33
                if self.speed[0] > 0:
                    self.speed[0] += 0.33
                elif self.speed[0] < 0:
                    self.speed[0] -= 0.33
                self.paddle_bounce = 0

        def ball_catch():
            self.speed = [0, 0]
            self.ballrect.x = paddle.paddle_rect.center[0]
            self.ballrect.bottom = paddle.paddle_rect.top

        if self.status == 'play':
            ball_play()
            # self.blit_ball(screen)

        if self.status == 'catch':
            ball_catch()
            # self.blit_ball(screen)

    def release(self):
        self.speed = [self.start_speed, -self.start_speed]
        self.status = 'play'

    def blit_ball(self, screen):
        screen.blit(self.ball, self.ballrect)

