import os
import random

import pygame

import Data_List

# 游戏初始化
score = 0
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((Data_List.WIDTH, Data_List.HEIGHT))
pygame.display.set_caption("飞机大战")
clock = pygame.time.Clock()

# 引入相关图片
background_img = (pygame.image.load(os.path.join("img", "background.png")).convert())
player_img = (pygame.image.load
              (os.path.join("img", "player.png")).convert())
rock_img = (pygame.image.load
            (os.path.join("img", "rock.png")).convert())
bullet_img = (pygame.image.load
              (os.path.join("img", "bullet.png")).convert())
rock_images = []
for i in range(7):
    rock_images.append(pygame.image.load
                       (os.path.join("img", f"rock{i}.png")).convert())

player_mini_img = pygame.transform.scale(player_img,(25,20))
player_mini_img.set_colorkey(Data_List.BLACK)

# 引入相关音频
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))
pygame.mixer.music.set_volume(0.3)
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]

font_name = pygame.font.match_font('arial')

def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,Data_List.WIDTH)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_top = y
    surf.blit(text_surface,text_rect)

def draw_health(surf,hp,x,y):
    #对血量出现负数进行预防
    if hp < 0:
        hp = 0
    #基础属性
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    #填充血条
    fill = (hp/100)*BAR_LENGTH
    #画血条
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,Data_List.GREEN,fill_rect)
    pygame.draw.rect(surf,Data_List.WHITE,outline_rect,2)

def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + (30 * i)
        img_rect.y = y
        surf.blit(img,img_rect)

def new_rock():
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

# 定义一个玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 添加玩家的外观
        self.image = pygame.transform.scale(player_img, (50, 40))
        self.image.set_colorkey(Data_List.BLACK)

        # 设置玩家位置
        self.rect = self.image.get_rect()

        self.radius = 23

        self.rect.centerx = Data_List.WIDTH / 2
        self.rect.bottom = Data_List.HEIGHT - 20

        # 定义变量存储速度、生命值
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (Data_List.WIDTH / 2 , Data_List.HEIGHT + 500)

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

        #隐藏
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = Data_List.WIDTH / 2
            self.rect.bottom = Data_List.HEIGHT - 20

    def shoot(self):
        # 定义函数用于发射子弹
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()


# 定义一个陨石类
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # 添加陨石的外观
        self.image_origin = random.choice(rock_images)
        self.image_origin.set_colorkey(Data_List.BLACK)
        self.image = self.image_origin.copy()

        # 设置陨石位置
        self.rect = self.image_origin.get_rect()

        self.radius = self.rect.width / 2.2

        self.rect.x = random.randrange(0, Data_List.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, 100)

        # 定义变量存储速度
        self.speedy = 1
        self.speedx = random.randrange(-3, 3)

        # 定义变量存储旋转角度
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    #陨石旋转
    def rotate(self):
        self.total_degree = self.total_degree + self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_origin, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    # 控制角色移动
    def update(self):
        self.rotate()
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
        self.image = bullet_img
        self.image.set_colorkey(Data_List.BLACK)

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
# 开始播放背景音乐
pygame.mixer.music.play(-1)
# 循环生成陨石对象
for i in range(8):
    new_rock()

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

    # 对子弹与陨石进行碰撞检测
    hits_rockAndBullet = pygame.sprite.groupcollide(rocks, bullets, True, True)
    for hit in hits_rockAndBullet:
        random.choice(expl_sounds).play()
        new_rock()
        score = score + int(hit.radius)

    # 对玩家和陨石进行碰撞检测
    hits_playerAndRocks = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits_playerAndRocks:
        player.health = player.health - hit.radius
        new_rock()
        if player.health <= 0:
            player.lives = player.lives - 1
            player.health = 100
            player.hide()
        if player.lives == 0:
            running = False

    # 显示屏幕上的内容
    screen.fill(Data_List.BLACK)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,Data_List.WIDTH / 2,0)
    draw_health(screen,player.health,10,30)
    draw_lives(screen,player.lives,player_mini_img,Data_List.WIDTH - 100,15)

    # 更新游戏
    pygame.display.update()
pygame.quit()
