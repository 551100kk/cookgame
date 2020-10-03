import random

from models.image import Image
from models.burger import Burger


class Customer:

    def __init__(self, customers, custype=None):
        if custype is None:
            custype, self.speed, self.count = random.choice(customers)
        else:
            custype, self.speed, self.count = customers[custype]

        self.show = True
        self.image = Image(custype, (110, 110))
        self.image.rect.center = (50, 205)
        self.cloud = Image('cloud', (150, 150))
        self.cloud.rect.center = (50, 120)
        self.burger = Burger(self.count, 50, 120)

    def move(self, screen):
        self.image.rect = self.image.rect.move(self.speed)
        self.cloud.rect = self.cloud.rect.move(self.speed)
        if self.image.rect.right > 800:
            self.image.image.fill((0, 0, 0, 0))
            self.show = False
        self.image.show_position(screen)
        self.cloud.show_position(screen)
        self.burger.update_burger(screen, self.speed)
