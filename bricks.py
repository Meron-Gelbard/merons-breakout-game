import pygame
import random

brick_colors = ['red', 'blue', 'cyan', 'pink', 'orange', 'green']


class Brick:
    """Brick class to be placed in a brick line list object"""
    def __init__(self, img_color, brick_size):
        # brick object with specified color and brick size (arg),
        img_color = f"img/{img_color}_brick.png"
        self.brick_size = brick_size
        self.brick = pygame.image.load(img_color)
        self.brick = pygame.transform.scale(self.brick, self.brick_size)
        self.brick_rect = self.brick.get_rect()


class BrickLine:
    """ A class of a list of Brick objects of random color.
     The number of bricks defined by screen width"""

    def __init__(self, b_color, row, screen, brick_size):
        spacing = brick_size[0] / 3
        # Calculation of maximum bricks that fit current screen size.
        brick_count = (screen.get_size()[0] - brick_size[0]) // brick_size[0]
        self.brick_line = [Brick(b_color, brick_size) for _ in range(brick_count)]
        for brick in self.brick_line:
            y_cor = (brick.brick_rect.height * row) + (screen.get_size()[1] * 0.05)
            brick.brick_rect.left += spacing
            brick.brick_rect.top = y_cor
            spacing += brick.brick_size[0]

    def blit_bricks(self, screen):
        """For repetitive rendering of brick lines on screen. (per line)"""

        for brick in self.brick_line:
            screen.blit(brick.brick, brick.brick_rect)


class LineManager:
    """ A management class for controlling bricks in brick-lines.
        Gets bottom most brick line position.
        Call brick-line rendering.
        Holds current brick count"""

    def __init__(self, line_count, screen, brick_size):
        self.brick_count = 0
        self.brick_lines = []
        self.bottom = 0

        for row in range(1, line_count+1):
            color = random.choice(brick_colors)
            self.brick_lines.append(BrickLine(b_color=color, row=row, screen=screen, brick_size=brick_size))
            self.brick_count += len(self.brick_lines[row-1].brick_line)

    def blit_lines(self, screen):
        """For repetitive rendering of a brick-line with updated state."""

        for line in self.brick_lines:
            if len(line.brick_line) == 0:
                self.brick_lines.remove(line)
            line.blit_bricks(screen=screen)

    def start_blit(self, screen):
        """ Visual effect for first render of bricks line on new level"""

        pygame.time.wait(1000)
        for line in self.brick_lines:
            for brick in line.brick_line:
                screen.blit(brick.brick, brick.brick_rect)
                pygame.display.flip()
                pygame.time.wait(10)

    def get_bottom(self):
        """ update the lowest brick position """
        self.bottom = self.brick_lines[-1].brick_line[0].brick_rect.bottom
        return self.bottom


