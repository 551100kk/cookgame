import pygame

from models.image import Image
from models.burger import Burger

audio_dir = './audio/'


class Player:

    def __init__(self, game, name, pos_x, cooldown):
        self.game = game
        self.name = name
        self.score = 0
        self.max_cooldown = cooldown
        self.cooldown = cooldown
        self.pos_x = pos_x
        self.burger = Burger(3, pos_x, 370, [])

    def show(self):
        Image('plate', (150, 150)).show_position(
            self.game.screen, (self.pos_x - 75, 275))
        self.game.display_text(
            self.name + ': ' + str(self.score), (self.pos_x, 20))
        if self.cooldown:
            self.game.display_text(
                'Cool Down: ' + str(self.cooldown), (self.pos_x, 460))
        else:
            self.game.display_text('Attack!', (self.pos_x, 460))

        self.burger.update_burger(self.game.screen)

    def fire_plate(self):
        fire = Image('fire', (150, 200), (self.pos_x, 300), 3)
        self.game.fadeout_list.append(fire)

    def do_serve(self):
        customer_list = self.game.customer_list
        pygame.mixer.Sound(audio_dir + 'sound_serve.wav').play()
        is_served = False
        for cust_id in range(len(customer_list)):
            if customer_list[cust_id].burger.equal(self.burger):
                is_served = True
                self.score += customer_list[cust_id].count * 10
                dollar_pos = list(customer_list[cust_id].image.rect.center)
                dollar_pos[1] -= 50
                dollar = Image('dollar', (100, 100), dollar_pos, 3)
                self.game.fadeout_list.append(dollar)
                del customer_list[cust_id]
                break
        if not is_served:
            self.score -= 50
        self.burger.clear()

    def do_trash(self):
        pygame.mixer.Sound(audio_dir + 'sound_trash.wav').play()
        self.burger.clear()

    def do_fire(self, enemy):
        if not self.cooldown:
            pygame.mixer.Sound(audio_dir + 'sound_fire.wav').play()
            enemy.burger.clear()
            enemy.fire_plate()
            self.cooldown = self.max_cooldown
