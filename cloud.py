import pygame
import random

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height):
        super().__init__()
        self.image = pygame.transform.scale(image, (
            random.randint(50, 150), random.randint(30, 90)))  # 随机大小
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width)
        self.rect.y = random.randint(-screen_height, 0)
        self.speed = random.randint(1, 3)  # 随机速度

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:  # 当云移动到屏幕底部以下时，重新生成在顶部
            self.rect.x = random.randint(0, 800)
            self.rect.y = random.randint(-600, 0)
            self.speed = random.randint(1, 3)  # 随机速度