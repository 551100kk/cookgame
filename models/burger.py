import random

from models.image import Image


class Burger:
    ingredient_choice = [
        'beef_side', 'bacon_side', 'lettuce_side', 'cheese_side'
    ]

    def __init__(self, count, pos_x, pos_y, ingredient=None):
        if ingredient is None:
            self.ingredient = ['botbun_side']
            random.shuffle(Burger.ingredient_choice)
            self.ingredient += Burger.ingredient_choice[:count - 2]
            self.ingredient.append('topbun_side')
        else:
            self.ingredient = ingredient
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.burger = []
        self.build_burger()

    def equal(self, burger):
        return self.ingredient == burger.ingredient

    def build_burger(self):
        for layer in range(len(self.ingredient)):
            image = Image(self.ingredient[layer], (60, 25))
            image.rect.center = (self.pos_x, self.pos_y - layer * 13)
            self.burger.append(image)

    def update_burger(self, screen, speed=(0, 0)):
        for image in self.burger:
            image.rect = image.rect.move(speed)
            image.show_position(screen)

    def add_ingredient(self, ingredient):
        if len(self.ingredient) < 10:
            self.ingredient.append(ingredient)
        self.burger = []
        self.build_burger()

    def clear(self):
        self.ingredient = []
        self.burger = []
        self.build_burger()
