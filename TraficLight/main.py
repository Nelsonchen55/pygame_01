"""
    制作一个红绿灯的小游戏，行人过马路
        1. 具有 GO 和 STOP 按钮 来选择 是否 前进
        2. 即使是绿灯也有看是否由行车 强行通过红灯， 所以 要 左右观看
        3. 绿灯的时间，60s, 差不多转灯就不要经过了
        4. 积分

    
    12/2/2021
        马路和斑马线弄出来，并且每辆汽车不应该重叠在各自的路上行驶

    12/3/2021
        车与人发生碰撞，弹出哭脸。按空白键再次开始

    12/6/2021
        红绿灯，红灯时人需要等待，汽车正常行驶， 绿灯时汽车停在斑马线前等待

    12/7/2021
        红绿灯与斑马线的相对位置时一定的，而汽车的停止应该也是和斑马线相关的
        所以创建斑马线的时候给其一个坐标。但是斑马线只是一张图片而已，并不是一个对象
        应该用一个元组来记录它的坐标比较好
        以后地图会更加复杂，会有多个斑马线。 用list记录他们的位置
"""



import pygame
import os
import random

FPS = 60
WIDTH = 720
HEIGHT = 650
CAR_WIDTH,CAR_HEIGHT = 60,20

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

# 游戏初始化 和 创建窗口
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
# 设置时钟，让游戏回圈在1秒内刷新一定的次数，要不然刷新的次数会非常快
clock = pygame.time.Clock()

# 加载图片
go_stop_img = pygame.image.load(os.path.join("TraficLight//img","GO&STOP.jpg")).convert()
gs_img_width = 520
gs_img_height = 233
car_imgs = []
orange_car_img = pygame.transform.scale(pygame.image.load(os.path.join("TraficLight//img","orange_car.png")).convert(),(CAR_WIDTH,CAR_HEIGHT))
white_car_img = pygame.transform.scale(pygame.image.load(os.path.join("TraficLight//img","white_car.png")).convert(),(CAR_WIDTH,CAR_HEIGHT))
yellow_car_img = pygame.transform.scale(pygame.image.load(os.path.join("TraficLight//img","yellow_car.jpg")).convert(),(CAR_WIDTH,CAR_HEIGHT))
car_imgs.append(orange_car_img)
car_imgs.append(white_car_img)
car_imgs.append(yellow_car_img)
road_img = pygame.image.load(os.path.join("TraficLight//img","road.bmp")).convert()
crossing_img = pygame.image.load(os.path.join("TraficLight//img","crossing.bmp")).convert()
goodjob_img = pygame.image.load(os.path.join("TraficLight//img","goodjob.jpg")).convert()
cry_img = pygame.image.load(os.path.join("TraficLight//img","cry.jpg")).convert()
home_img = pygame.image.load(os.path.join("TraficLight//img","home.bmp")).convert()
traficlight_img = pygame.image.load(os.path.join("TraficLight//img","traficlight.bmp")).convert()

# 12/7/2021  斑马线坐标
cross_list = [(WIDTH/2 - 50,HEIGHT/2 - 2)]

# 弹出图片暂停
def draw_pause(img):
    screen.blit(img,(0,0))
    pygame.display.update()
    # 游戏回圈，按下 空白键 返回
    running = True
    while running:
        clock.tick(FPS)
        # 接受事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

# 生产汽车并添加到sprite中
def new_car(loadline):
    car = Car(loadline)
    all_cars.add(car)
    all_sprites.add(car)

# 玩家
"""
    玩家应该用一个图片来表示，还没有找到图片，所以用个长方形表示
"""
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 20
        self.speed = 2

    def update(self):
        # self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.rect.y = HEIGHT
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a]:
            self.rect.centerx -= self.speed
        if key_pressed[pygame.K_d]:
            self.rect.centerx += self.speed
        if key_pressed[pygame.K_w]:
            self.rect.bottom -= self.speed
        if key_pressed[pygame.K_s]:
            self.rect.bottom += self.speed


# 车
"""
    马路上的车，在马路上左右不断行驶，当绿灯时会停在斑马线上等待
"""
road_list = [HEIGHT/2 + 5,HEIGHT/2+50,HEIGHT/2+105,HEIGHT/2 + 150]
class Car(pygame.sprite.Sprite):
    def __init__(self,roadline):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(car_imgs)
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = road_list[roadline]

        self.speed = random.randrange(4,10)
        self.loadline = roadline

    def update(self):
        self.rect.x += self.speed
        if self.rect.x >= WIDTH:
            self.rect.x = 0
        if light.color == RED and self.rect.x < cross_list[0][0]-50 and self.rect.x > cross_list[0][0] - 70:
            self.speed = 0
        if light.color == GREEN and self.speed == 0:
            self.speed = random.randrange(4,10)

# 红绿灯
light_time = 3000
class Light(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(traficlight_img,(40,80))
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.bottom = pos_y
        self.color = RED
        self.time = 0

    def update(self):
        if self.color == RED and pygame.time.get_ticks()-self.time>light_time:
            # for car in all_cars:
            #     car.speed = random.randrange(4,10)
            self.color = GREEN
            self.time = pygame.time.get_ticks()
            self.image.set_colorkey((237,28,36))
        elif self.color == GREEN and pygame.time.get_ticks()-self.time>light_time:
            # for car in all_cars:
            #     car.speed = 0
            self.color = RED
            self.time = pygame.time.get_ticks()
            self.image.set_colorkey((34,177,76))



# sprite 群组
all_sprites = pygame.sprite.Group()
all_cars = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(4):
    new_car(i)
light = Light(cross_list[0][0]+80,cross_list[0][1])
all_sprites.add(light)

running = True
# 游戏回圈
while running:

    clock.tick(FPS)

    # 取得输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos_x,pos_y = event.pos
            if pos_y < gs_img_height:
                if pos_x < gs_img_width/2:
                    player.speed = 0
                else:
                    player.speed = 2

    # 更新游戏
    all_sprites.update()

    # 汽车与人发生碰撞
    hits = pygame.sprite.spritecollide(player,all_cars,True)
    for hit in hits:
        draw_pause(cry_img)
        new_car(hit.loadline)
        player.rect.bottom = HEIGHT - 10


    # 页面显示
    screen.fill(WHITE)
    screen.blit(go_stop_img,(0,0))
    screen.blit(road_img,(0,HEIGHT/2))
    screen.blit(crossing_img,cross_list[0])
    screen.blit(home_img,(WIDTH-50,HEIGHT-50))
    all_sprites.draw(screen)
    pygame.display.update()


