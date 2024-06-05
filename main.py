import pygame
import random
from load_assets import load_images, load_sounds
from entities import Player, Enemy, Bullet, EnemyBullet, all_sprites, enemies, player_bullets, enemy_bullets
from cloud import Cloud  # 引入 Cloud 类


def show_game_over_screen(screen, font, replay_button_img):
    screen.fill((0, 0, 0))
    game_over_text = font.render("Game Over", True, (255, 255, 255))

    game_over_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 3))
    replay_button_rect = replay_button_img.get_rect(center=(screen_width / 2, screen_height / 1.5))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(replay_button_img, replay_button_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if replay_button_rect.collidepoint(event.pos):
                    waiting = False
                    return True
    return False


def start_new_game():
    global player, score
    score = 0

    # 清空所有组
    all_sprites.empty()
    enemies.empty()
    player_bullets.empty()
    enemy_bullets.empty()

    # 创建玩家对象并添加到 all_sprites
    player = Player(player_img, screen_width, screen_height)
    all_sprites.add(player)

    # 创建敌机对象并添加到 all_sprites 和 enemies
    for _ in range(10):
        enemy = Enemy(enemy_img, screen_width, screen_height)
        all_sprites.add(enemy)
        enemies.add(enemy)


# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("打飞机游戏")

# 加载图片和声音
player_img, enemy_img, bullet_img, background_img = load_images(screen_width, screen_height)
shoot_sound, enemy_hit_sound = load_sounds()
replay_button_img = pygame.image.load("replay_button.png")
cloud_img = pygame.image.load("clouds.png")  # 假设这是一张透明背景的云层图像

# 初始化分数
score = 0
font = pygame.font.Font(None, 36)


# 防止重叠的函数
def is_overlapping(sprite1, sprite2):
    return sprite1.rect.colliderect(sprite2.rect)


# 创建云层组
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()  # 创建一个新的组，包含所有飞机和云

for _ in range(10):  # 初始化10个随机大小和位置的云
    while True:
        cloud = Cloud(cloud_img, screen_width, screen_height)
        # 检查新云是否与现有的云或敌机重叠
        overlap = any(is_overlapping(cloud, existing_sprite) for existing_sprite in all_sprites)
        if not overlap:
            clouds.add(cloud)
            all_sprites.add(cloud)
            break

print("Starting game loop")
start_new_game()

# 游戏主循环
running = True
while running:
    print("Game loop iteration")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Player shoot")
                player.shoot(shoot_sound, Bullet, all_sprites, player_bullets)

    # 更新玩家和敌人的对象
    all_sprites.update()

    # 更新云层对象
    clouds.update()

    # 敌机发射子弹
    for enemy in enemies:
        enemy.shoot(all_sprites, enemy_bullets)

    # 检测玩家子弹和敌机的碰撞
    hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
    for hit in hits:
        enemy_hit_sound.play()
        score += 1
        print(f"Enemy hit. Score: {score}")
        enemy = Enemy(enemy_img, screen_width, screen_height)
        all_sprites.add(enemy)
        enemies.add(enemy)

    # 检测敌机子弹和玩家的碰撞
    hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
    for hit in hits:
        player.hit()
        print(f"Player hit. Lives are now: {player.lives}")
        if player.lives == 0:
            print("Player has no lives left. Game over.")
            if not show_game_over_screen(screen, font, replay_button_img):
                running = False
            else:
                start_new_game()

    # 检测玩家和敌机的碰撞
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.hit()
        print(f"Player collided with enemy. Lives are now: {player.lives}")
        if player.lives == 0:
            print("Player has no lives left. Game over.")
            if not show_game_over_screen(screen, font, replay_button_img):
                running = False
            else:
                start_new_game()

    # 绘制纯蓝色背景
    screen.fill((135, 206, 250))  # 天空蓝色

    # 绘制云层
    clouds.draw(screen)

    # 绘制精灵
    all_sprites.draw(screen)

    # 显示分数和生命值
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    # 更新显示
    pygame.display.flip()

    # 控制帧率
    pygame.time.Clock().tick(60)

print("Exiting game loop")
pygame.quit()