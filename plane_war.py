import pygame

# 定义一些常量
FPS = 120
WIDTH = 500
HEIGHT = 600
WHITE = (255,255,255)


# 游戏初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# 死循环,防止程序退出
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255,255,255))

    pygame.display.update()
pygame.quit()
