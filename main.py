import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# 游戏初始化 and 创建视窗
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# 更改游戏标题
pygame.display.set_caption("FirstGame")
# 设置时钟，让游戏回圈在1秒内刷新一定的次数
clock = pygame.time.Clock()

#加载图片，要在初始化之后
#os.path -->  表示该py文件所在的位置
background_img = pygame.image.load(os.path.join("FirstGame//img","background.png")).convert()
player_img = pygame.image.load(os.path.join("FirstGame//img","player.png")).convert()
rock_img = pygame.image.load(os.path.join("FirstGame//img","rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("FirstGame//img","bullet.png")).convert()

# 创建一个类别
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50,40))
        # self.image.fill((0,255,0)) 
        self.image = pygame.transform.scale(player_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        #设置坐标
        # self.rect.x = 200
        # self.rect.y = 200
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        #移动速度
        self.speedx = 8

    def update(self):
        # 键盘操作
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((30,40))
        # self.image.fill(RED)
        self.image = rock_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.85/2
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        #设置坐标
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-400, -200)
        #移动速度
        self.speedy = random.randrange(3,10)
        self.speedx = random.randrange(-3,3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.y>HEIGHT or self.rect.right < 0 or self.rect.left>WIDTH:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-400, -200)
            self.speedy = random.randrange(3,10)
            self.speedx = random.randrange(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((10,20))
        # self.image.fill(YELLOW)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # 当子弹到达顶部时，删除
        if self.rect.bottom < 0:
            self.kill()
        

# sprite 群体， 存储所有的sprite
all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

# 游戏回圈
running = True
while running:
    clock.tick(FPS)
    # 取得输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新游戏
    all_sprites.update()
    hits = pygame.sprite.groupcollide(rocks,bullets,True,True)
    # 因为子弹和石头碰撞后消失了，需要重新创建石头
    for hit in hits:
        r = Rock()
        all_sprites.add(r)
        rocks.add(r)

    # 当飞船和石头发生碰撞时，结束游戏
    hit = pygame.sprite.spritecollide(player,rocks,False,pygame.sprite.collide_circle)
    if hit:
        running = False

    # 页面显示
    screen.fill(BLACK)
    screen.blit(background_img,(0,0))
    all_sprites.draw(screen)
    pygame.display.update()   # 需要对画面进行更新才能显示更改的内容

pygame.quit()