import pygame
import random

# 全局变量定义
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height):
        super().__init__()
        self.image = image
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.speed = 5
        self.lives = 3
        self.invincible = False
        self.invincible_time = 2000  # 不可击中时间（毫秒）
        self.flash_duration = 150  # 闪烁时间间隔
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < self.screen_height:
            self.rect.y += self.speed

        if self.invincible:
            now = pygame.time.get_ticks()
            if now - self.hit_time > self.invincible_time:
                self.invincible = False
                self.image = self.original_image
            else:
                # 闪烁效果
                if (now // self.flash_duration) % 2 == 0:
                    self.image.set_alpha(255)
                else:
                    self.image.set_alpha(0)
        else:
            self.image.set_alpha(255)

    def shoot(self, shoot_sound, Bullet, all_sprites, player_bullets):
        shoot_sound.play()
        bullet = Bullet(self.rect.centerx, self.rect.top, self.screen_height)
        all_sprites.add(bullet)
        player_bullets.add(bullet)

    def hit(self):
        if not self.invincible:
            self.lives -= 1
            self.invincible = True
            self.hit_time = pygame.time.get_ticks()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, screen_width, screen_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 4)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.rect.x = random.randint(0, self.screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(1, 4)

    def shoot(self, all_sprites, enemy_bullets):
        if random.random() < 0.01:  # 1% 机率发射子弹
            num_bullets = random.randint(1, 2)
            for _ in range(num_bullets):
                bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.screen_height)
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_height):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (15, 15))  # 缩小子弹图像
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -10
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_height):
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (15, 15))  # 缩小子弹图像
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.screen_height = screen_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.kill()