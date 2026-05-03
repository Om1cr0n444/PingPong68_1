from pygame import *

init()

win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-Pong")

back = (200, 200, 255)
font.init()
score_font = font.Font(None, 36)
game_over_font = font.Font(None, 70)

score1 = 0
score2 = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

racket1 = Player('racket1.png', 30, 200, 3, 40, 120)
racket2 = Player('racket2.png', 530, 200, 3, 40, 120)
ball = GameSprite('ball2.png', 200, 200, 4, 40, 40)

lose1 = game_over_font.render('Левый игрок проиграл!', True, (180, 0, 0))
lose2 = game_over_font.render('Правый игрок проиграл!', True, (180, 0, 0))

speed_x = 3
speed_y = 3

clock = time.Clock()
FPS = 120
WINNING_SCORE = 5

game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    window.fill(back)

    game_is_over = score1 >= WINNING_SCORE or score2 >= WINNING_SCORE

    if not game_is_over:
        racket1.update_l()
        racket2.update_r()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        if ball.rect.y > win_height - 40 or ball.rect.y < 0:
            speed_y *= -1

        if sprite.collide_rect(racket1, ball) or sprite.collide_rect(racket2, ball):
            speed_x *= -1

        if ball.rect.x < 0:
            score1 += 1
            ball.rect.x, ball.rect.y = win_width//2, win_height//2
            speed_x *= -1 

        elif ball.rect.x > win_width - 40:
            score2 += 1
            ball.rect.x, ball.rect.y = win_width//2, win_height//2
            speed_x *= -1

    else:
        if score1 >= WINNING_SCORE:
            window.blit(lose1, (win_width // 2 - lose1.get_width() // 2, win_height // 2))
        else:
            window.blit(lose2, (win_width // 2 - lose2.get_width() // 2, win_height // 2))
        
        keys_pressed = key.get_pressed()
        if any(keys_pressed): 
            game = False

    text_score1 = score_font.render(f'{score1}', True, (0, 0, 0))
    text_score2 = score_font.render(f'{score2}', True, (0, 0, 0))
    window.blit(text_score1, (win_width // 2 - 40, 20))
    window.blit(text_score2, (win_width // 2 + 20, 20))
    
    if not game_is_over:
        racket1.reset()
        racket2.reset()
        ball.reset()
    
    display.update()
    clock.tick(FPS)