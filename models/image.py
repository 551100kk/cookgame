import pygame

image_cache = {}
image_dir = './image/'


class Image(pygame.sprite.Sprite):

    def __init__(self, name, size=None, pos=None, alpha_delta=None):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        if name not in image_cache:
            image_cache[name] = pygame.image.load(image_dir + name + '.png')
        self.image = image_cache.get(name)
        if size:
            self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        if pos:
            self.rect.center = (pos[0], pos[1])
        self.alpha = 255
        self.alpha_delta = 1
        if alpha_delta is not None:
            self.alpha_delta = alpha_delta

    def show_position(self, screen, pos=None, size=None):
        if size is not None:
            self.image = pygame.transform.scale(self.image, size)
        if pos is None:
            pos = self.rect
        screen.blit(self.image, pos)

    def fade_out(self, screen):
        if self.alpha > 0:
            self.alpha -= self.alpha_delta
        surf = pygame.surface.Surface((self.rect.width, self.rect.height))
        surf.set_colorkey((0, 0, 0))
        surf.set_alpha(self.alpha)
        surf.blit(self.image, (0, 0))
        screen.blit(surf, self.rect)
        return self.alpha <= 0
