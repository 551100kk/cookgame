import pygame
import random
import sys
import time

from models.image import Image
from models.burger import Burger
from models.customer import Customer
from models.player import Player

setting = {
    'tick': 60,
    'duration': 120,
    'cooldown': 30,
    'customer': [
        ('man', (1, 0), 3),
        ('superhero', (2, 0), 4),
        ('wizard', (3, 0), 5)
    ]
}

audio_dir = './audio/'


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('我是廚神')
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.time.Clock().tick(setting.get('tick'))
        self.prev_customer_tick = -1000
        self.now_tick = 0
        self.game_time = setting.get('duration')
        self.player1 = Player(self, 'Player1', 140, setting.get('cooldown'))
        self.player2 = Player(self, 'Player2', 660, setting.get('cooldown'))

        pygame.mixer.init()
        pygame.mixer.music.load(audio_dir + 'sound_background.mp3')
        pygame.mixer.music.play(1, 0)
        self.font = pygame.font.SysFont('Consolas', 30)
        self.screen = pygame.display.set_mode((800, 480))
        self.customer_list = []
        self.fadeout_list = []

    def display_background(self):
        Image('background').show_position(self.screen, (-300, -600))
        Image('ring', (50, 50)).show_position(self.screen, (300, 385))
        Image('trashcan', (50, 50)).show_position(self.screen, (380, 385))
        Image('match', (50, 50)).show_position(self.screen, (460, 385))

        chair = Image('chair', (150, 150))
        for i in range(3):
            chair.show_position(self.screen, (100 + 230 * i, 60))
        squareplate = Image('squareplate', (90, 90))
        for i in range(3):
            for j in range(2):
                squareplate.show_position(
                    self.screen, (280 + 80 * i, 250 + 60 * j))

        Image('topbun', (50, 20)).show_position(self.screen, (299, 285))
        Image('botbun', (50, 20)).show_position(self.screen, (380, 288))
        Image('beef', (50, 50)).show_position(self.screen, (460, 275))
        Image('bacon', (90, 90)).show_position(self.screen, (280, 315))
        Image('lettuce', (50, 50)).show_position(self.screen, (380, 330))
        Image('cheese', (80, 80)).show_position(self.screen, (445, 320))

        if self.game_time:
            self.display_text(str(self.game_time), (400, 20))
        else:
            self.display_text('Time\'s up!', (400, 20))

    def display_text(self, text, pos):
        text = self.font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=pos)
        self.screen.blit(text, text_rect)

    def display_fadeout(self):
        for image_id in range(len(self.fadeout_list))[::-1]:
            if self.fadeout_list[image_id].fade_out(self.screen):
                del self.fadeout_list[image_id]

    def update_customer(self):
        if random.random() < 1.0 / 40 and self.now_tick - self.prev_customer_tick > 120:
            self.prev_customer_tick = self.now_tick
            self.customer_list.append(Customer(setting.get('customer')))

        for cust_id in range(len(self.customer_list)):
            self.customer_list[cust_id].move(self.screen)
        for cust_id in range(len(self.customer_list))[::-1]:
            if not self.customer_list[cust_id].show:
                del self.customer_list[cust_id]

    def catch_keyboard(self, game_event):
        keys = pygame.key.get_pressed()
        action = {
            pygame.K_q: lambda: self.player1.burger.add_ingredient('topbun_side'),
            pygame.K_w: lambda: self.player1.burger.add_ingredient('botbun_side'),
            pygame.K_e: lambda: self.player1.burger.add_ingredient('beef_side'),
            pygame.K_a: lambda: self.player1.burger.add_ingredient('bacon_side'),
            pygame.K_s: lambda: self.player1.burger.add_ingredient('lettuce_side'),
            pygame.K_d: lambda: self.player1.burger.add_ingredient('cheese_side'),
            pygame.K_z: lambda: self.player1.do_serve(),
            pygame.K_x: lambda: self.player1.do_trash(),
            pygame.K_c: lambda: self.player1.do_fire(self.player2),


            pygame.K_i: lambda: self.player2.burger.add_ingredient('topbun_side'),
            pygame.K_o: lambda: self.player2.burger.add_ingredient('botbun_side'),
            pygame.K_p: lambda: self.player2.burger.add_ingredient('beef_side'),
            pygame.K_k: lambda: self.player2.burger.add_ingredient('bacon_side'),
            pygame.K_l: lambda: self.player2.burger.add_ingredient('lettuce_side'),
            pygame.K_SEMICOLON: lambda: self.player2.burger.add_ingredient('cheese_side'),
            pygame.K_COMMA: lambda: self.player2.do_serve(),
            pygame.K_PERIOD: lambda: self.player2.do_trash(),
            pygame.K_SLASH: lambda: self.player2.do_fire(self.player1),
        }

        for key, event in action.items():
            if game_event.key == key:
                event()

    def start_game(self):
        while True:
            random.seed(time.time())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.USEREVENT:
                    if self.game_time:
                        self.game_time -= 1
                    if self.player1.cooldown:
                        self.player1.cooldown -= 1
                    if self.player2.cooldown:
                        self.player2.cooldown -= 1
                if event.type == pygame.KEYDOWN:
                    self.catch_keyboard(event)

            self.now_tick += 1
            self.display_background()
            self.update_customer()
            self.player1.show()
            self.player2.show()
            self.display_fadeout()
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    Game().start_game()
