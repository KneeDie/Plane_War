import random

import pygame

import Data_List

# 游戏初始化
pygame.init()
screen = pygame.display.set_mode((Data_List.WIDTH, Data_List.HEIGHT))
pygame.display.set_caption("飞机大战")
clock = pygame.time.Clock()


# 定义一个玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 添加玩家的外观
        self.image = pygame.Surface((50, 40))
        self.image.fill(Data_List.GREEN)

        # 设置玩家位置
        self.rect = self.image.get_rect()
        self.rect.centerx = Data_List.WIDTH / 2
        self.rect.bottom = Data_List.HEIGHT - 20

        # 定义变量存储速度
        self.speedx = 8

    # 控制角色移动
    def update(self):
        # 使用左右键控制角色移动
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        # 固定位置，防止穿墙
        if self.rect.right > Data_List.WIDTH:
            self.rect.right = Data_List.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        # 定义函数用于发射子弹
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)


# 定义一个陨石类
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 添加陨石的外观
        self.image = pygame.Surface((30, 30))
        self.image.fill(Data_List.RED)

        # 设置陨石位置
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, Data_List.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)

        # 定义变量存储速度
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)

    # 控制角色移动
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > Data_List.HEIGHT or self.rect.left > Data_List.WIDTH or self.rect.right < 0:
            # 再次设置陨石降落位置
            self.rect.x = random.randrange(0, Data_List.WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            # 定义变量存储速度
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)


# 定义一个子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # 添加子弹的外观
        self.image = pygame.Surface((10, 20))
        self.image.fill(Data_List.YELLOW)

        # 设置陨石位置
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 定义变量存储速度
        self.speedy = -10

    # 控制角色移动
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# 定义一个列表存储所有对象
all_sprites = pygame.sprite.Group()
# 定义一个列表存储陨石
rocks = pygame.sprite.Group()
# 定义一个列表存储子弹
bullets = pygame.sprite.Group()

# 生成玩家对象
player = Player()
all_sprites.add(player)
# 循环生成陨石对象
for i in range(8):
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# 死循环,防止程序退出
running = True
while running:
    # 设置帧率
    clock.tick(Data_List.FPS)
    for event in pygame.event.get():
        # 判断是否退出
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # 判断书否按下空格
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新所有角色
    all_sprites.update()

    #对子弹和陨石进行碰撞检测
    hits_rockAndbullet = pygame.sprite.spritecollide(player,rocks,False)
    if hits_rockAndbullet:
        running = False

    #对玩家与陨石进行碰撞检测

    # 显示屏幕上的内容
    screen.fill(Data_List.BLACK)
    all_sprites.draw(screen)

    # 更新游戏
    pygame.display.update()
pygame.quit()
