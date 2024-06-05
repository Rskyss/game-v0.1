import pygame

def load_images(screen_width, screen_height):
    try:
        player_img = pygame.image.load("player.png")
        enemy_img = pygame.image.load("enemy.png")
        bullet_img = pygame.image.load("bullet.png")
        background_img = pygame.image.load("background.png")

        # 缩放图像
        player_img = pygame.transform.scale(player_img, (50, 50))
        enemy_img = pygame.transform.scale(enemy_img, (60, 60))
        bullet_img = pygame.transform.scale(bullet_img, (10, 10))
        background_img = pygame.transform.scale(background_img, (screen_width, screen_height * 2))  # 背景图片设置为两倍高度以便垂直滚动

        return player_img, enemy_img, bullet_img, background_img
    except pygame.error as e:
        print(f"Error loading images: {e}")
        pygame.quit()
        exit()

def load_sounds():
    try:
        shoot_sound = pygame.mixer.Sound("shoot.wav")
        enemy_hit_sound = pygame.mixer.Sound("enemy_hit.wav")
        print("Sounds loaded successfully")
        return shoot_sound, enemy_hit_sound
    except pygame.error as e:
        print(f"Error loading sounds: {e}")
        pygame.quit()
        exit()