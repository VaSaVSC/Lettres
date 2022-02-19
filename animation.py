import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name, mode=0, change_dim=False, width=0,  height=0):
        super().__init__()
        self.mode = mode
        self.sprite_sheet = pygame.image.load(f"./sprites/{name}{mode}.png")
        if change_dim:
            self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (width, height))
        self.animation_index = 0
        self.animation_bool = True
        self.speed = 3
        self.clock = 0
        self.images = {
            'down': self.get_images(0),
            'left': self.get_images(32),
            'right': self.get_images(64),
            'up': self.get_images(96)
        }

    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed * 8

        if self.clock >= 100:

            if self.animation_bool:
                self.animation_index += 1
                if self.animation_index == 2:
                    self.animation_bool = False

            else:
                self.animation_index -= 1
                if self.animation_index == 0:
                    self.animation_bool = True

            self.clock = 0

    def get_images(self, y):
        images = []

        for i in range(0, 3):
            x = i * 32
            image = self.get_image(x, y)
            images.append(image)

        return images

    def get_image(self, x, y, w=32, h=32):
        image = pygame.Surface([w, h])
        image.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return image
