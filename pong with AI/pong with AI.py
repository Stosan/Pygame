import pygame, sys, random

Cap_string = input('Enter Your name and press enter: ')
yournm = Cap_string
# initialize pygame setup
pygame.init()
clock = pygame.time.Clock()
ffont = pygame.font.SysFont('Arial', 18, True)
basic_font2 = pygame.font.SysFont('Arial', 120, True)

# General setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()
nm = "y"
# Main Window
screen_width = 1280
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong with AI')

# Global Variables with our sounds
bg_color = pygame.Color(255, 234, 244)
accent_color = (27, 35, 43)
blue = pygame.Color(59, 13, 211)
basic_font = pygame.font.SysFont('Garamond', 32)
plob_sound = pygame.mixer.Sound("sounds/pong.ogg")
score_sound = pygame.mixer.Sound("sounds/score.ogg")
middle_strip = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

itd ="AI: "
game_over = False


class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
pat = "R"



class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.restart_counter()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(plob_sound)
            self.speed_y *= -1


        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(plob_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        pygame.mixer.Sound.play(score_sound)

    def restart_counter(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3

        if current_time - self.score_time <= 700:
            countdown_number = 3
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 2
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 1
        if 2100 < current_time - self.score_time <= 2800:
            countdown_number = "go"
        if current_time - self.score_time >= 2800:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)


axt = "ah"
# design the AI opponent
class AI_Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed


    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height


class GameManager:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.AI_opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.AI_opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()
        if self.AI_opponent_score == 10:
            alert_AI = "AI wins!"
            AI_alt = basic_font2.render(f'{alert_AI}', False, blue)
            AI_rect_alt = AI_alt.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
            screen.blit(AI_alt, AI_rect_alt)
            pygame.display.update()
            self.reset_scores()
        if self.player_score == 20:
            alert_U = "YOU win!"
            U_alt = basic_font2.render(f'{alert_U}', False, blue)
            U_rect_alt = U_alt.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
            screen.blit(U_alt, (screen_width / 2, screen_height / 2))
            self.reset_scores()

    def draw_score(self):
        global axt, nm, pat, yournm, itd
        U_name = ffont.render(f'{yournm}', False, blue)
        U_rect = U_name.get_rect(midright=(screen_width / 2, screen_height / 2))
        screen.blit(U_name, (1118, screen_height / 50))

        player_score = basic_font.render(str(self.player_score), True, accent_color)
        AI_opponent_score = basic_font.render(str(self.AI_opponent_score), True, accent_color)


        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 40, screen_height / 2))
        AI_opponent_score_rect = AI_opponent_score.get_rect(midright=(screen_width / 2 - 40, screen_height / 2))

        screen.blit(player_score, player_score_rect)
        screen.blit(AI_opponent_score, AI_opponent_score_rect)

        Rmm = itd+pat+nm+axt
        AI_name = ffont.render(f'{Rmm}', False, blue)
        AI_rect = AI_name.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(AI_name, (screen_width / 50, screen_height / 50))
    def reset_scores(self):
        pygame.time.delay(2000)
        self.player_score = 0
        self.AI_opponent_score = 0


# Game objects with images
player = Player('imgs/Paddle.png', screen_width - 20, screen_height / 2, 5)
AI_opponent = AI_Opponent('imgs/Paddle.png', 20, screen_width / 2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(AI_opponent)

ball = Ball('imgs/Ball.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

game_manager = GameManager(ball_sprite, paddle_group)

def pong():

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.movement -= player.speed
                if event.key == pygame.K_DOWN:
                    player.movement += player.speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.movement += player.speed
                if event.key == pygame.K_DOWN:
                    player.movement -= player.speed

        # Background Stuff
        screen.fill(bg_color)
        pygame.draw.rect(screen, accent_color, middle_strip)

        # Run the game
        game_manager.run_game()

        # Rendering
        pygame.display.flip()
        clock.tick(120)

pong()