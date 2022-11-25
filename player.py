import pygame
import sys
import pygame.locals as K

class Paddle:
    def __init__(self, screen):
        self.paddle = pygame.image.load("img/paddle.png")
        self.paddle = pygame.transform.scale(self.paddle, (140, 20))
        self.paddle_rect = self.paddle.get_rect()
        self.screen_size = screen.get_size()
        self.paddle_rect.center = (self.screen_size[0] / 2, self.screen_size[1] - 50)
        self.status = 'catch'

    def blit_paddle(self, screen):
        # update paddle position on display
        screen.blit(self.paddle, self.paddle_rect)

    def update_status(self, line_manager, ball, scoreboard):
        # listen to left/right key presses initiating paddle movement functions accordingly.
        # catches ball when brick count is 0 and returns 'level cleared' to game status
        # checks for brick lines hitting bottom limit and returns scoreboard.lives = 0
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K.K_RIGHT:
                    self.move_right(ball)
                elif event.key == K.K_LEFT:
                    self.move_left(ball)
                if event.key == K.K_SPACE and self.status == 'catch':
                    self.status = 'play'
                    ball.release()
                    return self.status
            if event.type == pygame.QUIT:
                sys.exit()
        if line_manager.brick_count == 0 and self.paddle_rect.colliderect(ball.ballrect):
            self.status = 'level cleared'
        elif ball.status == 'catch':
            self.status = 'catch'
        elif line_manager.bottom >= self.paddle_rect.top:
            scoreboard.lives = 0
        return self.status

    def move_left(self, ball):
        # move paddle left with left screen boundary
        if self.paddle_rect.left > 0:
            if ball.status == 'play':
                self.paddle_rect.x -= abs(ball.speed[0]) * 0.3
            else:
                self.paddle_rect.x -= 3

    def move_right(self, ball):
        # move paddle right with right screen boundary
        if self.paddle_rect.right < self.screen_size[0]:
            if ball.status == 'play':
                self.paddle_rect.x += abs(ball.speed[0]) * 0.3
            else:
                self.paddle_rect.x += 3
