import pygame
import sys
import csv
import pygame.locals as K


class ScoreBoard:
    """Game Scoreboard class holding life count, points count,
    player name and UI messaging functionality.
    """

    def __init__(self):
        self.board_font = pygame.font.SysFont("monospace", 25, bold=True)
        self.score = 0
        self.lives = 0
        self.player_name = ''
        self.lives_img = pygame.image.load('img/paddle.png')
        self.lives_img = pygame.transform.scale(self.lives_img, (60, 15))
        self.lives_rect = self.lives_img.get_rect()
        self.ui_font = pygame.font.SysFont("monospace", 25, bold=True)
        self.quit_msg = "OK LOVE YA BYE-BYE !"
        # Gets current high scores table from csv
        with open('score_table.csv', 'r') as current_scores:
            self.current_high_scores = [row for row in current_scores]

    def log_in(self, screen, font, mid_screen):
        """Welcome screen with player sign-in system and current high scores."""

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                elif event.key == K.K_RETURN:
                    return 'start'
                else:
                    if len(self.player_name) < 15:
                        self.player_name = self.player_name + event.unicode
            if event.type == pygame.QUIT:
                sys.exit()

        welcome_l = font.render("WELCOME TO MERON's BREAK-OUT GAME!", False, (255, 255, 0))
        screen.blit(welcome_l, (mid_screen[0] - 75, mid_screen[1] - 300))
        self.msg_blit(text="Please enter your name:", screen=screen, row=1, color=(255, 255, 255))
        self.msg_blit(text=f"{self.player_name}_", screen=screen, row=2.5, color=(250, 250, 250))
        self.msg_blit(text="Current high scores:", screen=screen, row=5, color=(255, 255, 255))

        high_scores = self.get_high_scores()

        for row in range(len(high_scores)):
            row_text = ''
            row_length = 25
            row_text += f"{high_scores[row][0]}"
            for _ in range(row_length - len(row_text)):
                row_text += ' '
            row_text = row_text[:-len(high_scores[row][1])] + high_scores[row][1]
            self.msg_blit(text=row_text, screen=screen, row=6.5 + row*1.2, color=(255, 255, 255))

    def blit_board(self, screen):
        """For repetitive update of scoreboard display with current lives & score."""
        #
        y_player = screen.get_size()[1] * 0.04
        x_player = screen.get_size()[0] * 0.05
        lives_xy = (screen.get_size()[0] - 80, y_player + 3)
        player_l = self.board_font.render(f"{self.player_name} | ", False, (255, 255, 255))
        score_l = self.board_font.render(f"SCORE: {self.score}", False, (255, 255, 0))
        lives_l = self.board_font.render(f"{self.lives} X ", False, (255, 255, 0))
        screen.blit(player_l, (x_player, y_player))
        screen.blit(score_l, (x_player + player_l.get_width() + 10, y_player))
        screen.blit(self.lives_img, lives_xy)
        screen.blit(lives_l, (lives_xy[0] - 75, y_player))

    def game_over(self, screen):
        """Generates GAME-OVER message on screen"""
        self.msg_blit(screen=screen, text="GAME OVER", row=2, color=(255, 255, 255))

    def quit_question(self, screen):
        """Generates quit question on screen"""
        self.msg_blit(screen=screen, text="Start new game?  Y/N", row=4, color=(255, 255, 255))

    def new_high(self, screen):
        """Generates 'New High Score' message if a high score was received.
        Calls update high scores function
        """
        #
        if self.score > int(self.get_high_scores()[-1][1]):
            self.update_high_score()
            pygame.time.wait(1000)
            self.msg_blit(screen=screen, text="New high score!", row=1, color=(255, 255, 255))

    def byebye(self, screen):
        """Generates 'goodbye' message with typing effect"""

        message = self.quit_msg.split(" ")
        for i in range(len(message) + 1):
            screen.fill((0, 0, 0))
            pygame.time.wait(400)
            self.msg_blit(screen=screen, row=5, text=f"{' '.join(message[:i])}", color=(255, 255, 255))
            pygame.display.flip()

    def update_high_score(self):
        """Gets current high scores file. Adds new score.
        Re-sorts list & shortens to 10 high scores. Re-writes csv.
        """
        #
        updated_scores = []
        with open('score_table.csv', 'r') as score_table:
            for row in csv.reader(score_table):
                updated_scores.append(row)

        with open('score_table.csv', 'w', newline='') as new_score_table:
            updated_scores.append([self.player_name, self.score])
            updated_scores.sort(key=lambda x: int(x[1]), reverse=True)
            if len(updated_scores) > 10:
                updated_scores = updated_scores[:10]
            for row in updated_scores:
                csv.writer(new_score_table).writerow(row)

    @staticmethod
    def get_high_scores():
        """ Gets current high scores """
        with open('score_table.csv', 'r', newline='') as current_scores:
            scores = []
            for row in csv.reader(current_scores):
                scores.append(row)
            return scores

    def msg_blit(self, text, screen, row, color):
        """ Renders a message on screen with a padded black background. """

        center_surface = pygame.Surface(size=(5, 5))
        label = self.ui_font.render(text, False, color)
        center_surface = pygame.transform.scale(center_surface,
                                                (label.get_size()[0] + 10, label.get_size()[1] + 8))
        center_surface.fill((0, 0, 0))
        xy = (screen.get_size()[0] / 2 - label.get_width() / 2, screen.get_size()[1] / 3 + label.get_size()[1] * row)
        screen.blit(center_surface, (xy[0] - 5, xy[1] - 4))
        screen.blit(label, xy)
