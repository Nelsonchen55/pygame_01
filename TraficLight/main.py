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

    12/8/2021
        创建商店， 关于商店应该是building的一个子类
        -- Building
            -- House
            -- Shop
        感觉没什么必要，但是还是先这样弄
        Shop 重要弄个targe 用来实现购物

    12/9/2021
        创建店员，和店员对话在左侧出现购物单
        店员就是一个类，设置为seller,也是一个sprite.
        和player发生碰撞后 -- player应该不能继续前行
                          -- 应该按下一个固定健来对话
                          上面的需求先不做
                          直接碰撞就弹出  商品菜单

    12/10/2021
        今天来处理商品菜单的问题： 也许弄一个菜单的方法比较好
            这个方法接受一个list， 然后将list 中的内容画在屏幕的右边
"""



import pygame
import os
import random
import sys

# 方便用于测试
pos = 500,200

FPS = 60
WIDTH = 920
HEIGHT = 650
CAR_WIDTH,CAR_HEIGHT = 60,20
ITEM_WIDTH,ITEM_HEIGHT = 100,100

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

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

# 菜单
def draw_menu(ls1,ls2):
    for index in range(len(ls1)):
        screen.blit(ls1[index],(WIDTH - 150,index*110))
        draw_text(screen,"+",20,(WIDTH - 240,index*110+60))
        draw_text(screen,str(ls2[index]),30,(WIDTH - 210,index*110+65))
        draw_text(screen,"-",20,(WIDTH - 180,index*110+60))

Char_list = ['A','B','C','D','E','F','G']
# 列出方程组,参数为: 未知数的个数,未知数可取的最大值
def create_equation_set(nums,largest):
    equations = []
    # 随机生成未知数
    randnums = random.choices(list(range(largest)),k=nums)
    numchars = Char_list[:nums]
    # numchars.append(Char_list[0])
    print(randnums)
    # 这个循环是将从头都尾部的所有相邻的两个数进行操作
    for i in range(nums):
        a = randnums[i]
        if i+1 == nums:
            i = -1
        b = randnums[i+1]
        equations.append(str(numchars[i]) + ' + ' + str(numchars[i+1]) + ' = ' + str(a+b))

    # # 这个循环得到一个所有未知数的相关操作的一个等式
    # total_equation = ''
    # total_answer = 0
    # for i in range(nums):
    #     total_answer = total_answer + randnums[i]
    #     total_equation = total_equation + str(numchars[i])
    #     if i == nums-1:
    #         total_equation = total_equation + ' = ' + str(total_answer)
    #     else:
    #         total_equation = total_equation + ' + '
    # equations.append(total_equation)

    return equations

'''
    画出方程组，并且接受数值的输入
    需要对输入的数字进行判断，应该想生成方程组那些 显示出 数字的操作  。。。。 视乎思路完全打乱了，需要重新在设置一个方法？ 
        而且创建方程组的方法也就是出现了加法操作而已，理论上时不应该这样的， 所以这个检测方法是不是也能先写出加法的操作

    
    key的按钮操作：
        space:  刷新页面，生成新的方程组
        0-9：   写入数字
        return: 换到新的一行进行赋值
        q:      退出该页面，回到原来的那个界面
        应该还要有“检测” 和 “删除输入的所有数字” 这两个操作
            “删除输入的所有数字” 较为简单，就是不调用create_equation_set方法跳出里循环
            如果有“检测”的功能，就应该有一个数组来记录生成的数字
                思路： 这个数组要有一个长度，应该和未知数的个数一样的
                       按回车键时就应该进入下一个变量，所以index 为 line
                       而且每次输入数字的时候，添加之前应该要*10
                       这里line作为index的话，就要考虑outofindex的情况了，所以判断line到了一定的值时就不能继续增加了，所以也就不需要 p案件了
        back:   “删除输入的所有数字”
        p:      “检测”    ---- 改在return里实现

'''
def calculating():
    variable_length, variable_range = (3,10)
    eqs = create_equation_set(variable_length, variable_range)  # 方程组在刚开始或者按刷新时才重新调用的，所以因该放在游戏回圈前和触发刷新时
    input_list = [0 for x in range(variable_length)]
    print(input_list)
    ORI_X,ORI_Y = (200,100)  # 角标的位置，用于方便控制 draw_text 的光标位置
    x = ORI_X
    y = ORI_Y
    testing = True
    while testing:
        screen.fill(WHITE)
        
        for i in range(len(eqs)):
            draw_text(screen,eqs[i], 50, (x,y*i))
            draw_text(screen,Char_list[i]+" = ", 50, (x+500, y*i))


        pygame.display.update()

        line = 0 # 用于记录现在输入数字应该对应与那一行
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # x,y = pygame.mouse.get_pos() # 在鼠标所在的位置写入数字也是不错的，就是不能使数字处于水平，而且间距也不好看
                if event.key <= pygame.K_9 and event.key >= pygame.K_0 :
                    input_list[line] = input_list[line] * 10 + (event.key-pygame.K_0)
                    draw_text(screen,str(event.key-pygame.K_0),50,(x+590,y*line))
                    # 虽然现在的未知数都是单位数的，以后可能要调大到两位数，所以输入一个数值后，x的值应该右移动一点
                    x = x + 25
                    pygame.display.update()
                elif event.key == pygame.K_RETURN:
                    # 并且x的值应该回归原来的值
                    x = ORI_X
                    # 换到输入的下一行, 如果line的值小于变量的值
                    if line < variable_length-1:
                        line = line + 1
                    else:
                        # 写出检测的方程组
                        equations = []
                        # 这个循环是将从头都尾部的所有相邻的两个数进行操作
                        for i in range(variable_length):
                            a = input_list[i]
                            if i+1 == variable_length:
                                i = -1
                            b = input_list[i+1]
                            equations.append(str(input_list[i]) + ' + ' + str(input_list[i+1]) + ' = ' + str(a+b))

                        for i in range(len(equations)):
                            draw_text(screen,equations[i], 50, (x,y*(i+variable_length)))

                        pygame.display.update()
                        input_list = [0 for x in range(variable_length)]              
                elif event.key == pygame.K_SPACE:
                    input_list = [0 for x in range(variable_length)]
                    eqs = create_equation_set(variable_length, variable_range)
                    x = ORI_X
                    break
                elif event.key == pygame.K_BACKSPACE:
                    input_list = [0 for x in range(variable_length)]
                    x = ORI_X
                    break
                elif event.key == pygame.K_q:
                    testing = False
                    break

# 写文字在界面上
font_name = os.path.join("TraficLight","font.ttf")
def draw_text(surf,text,size,pos):
    font = pygame.font.Font(font_name,size)
    # 文本渲染
    text_surface = font.render(text,True,BLACK)
    # 定位
    text_rect = text_surface.get_rect()
    text_rect.left = pos[0]
    text_rect.top = pos[1]
    # 画出来
    surf.blit(text_surface,text_rect)

# 玩家
"""
    玩家应该用一个图片来表示，还没有找到图片，所以用个长方形表示
"""
class Player(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("TraficLight//img","men_01.jpg")).convert()
        self.image.set_colorkey(WHITE)
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.bottom = pos_y
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

class Building(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        # pygame.sprite.Sprite.__init__(self)
        pass

    def update(self):
        pass

class Shop(Building):
    def __init__(self,pos_x,pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((100,100))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.width = 120
        self.height = 120
        self.rect.centerx = pos_x
        self.rect.bottom = pos_y
        self.all_sprites = pygame.sprite.Group()
        self.all_sellers = pygame.sprite.Group()


    def inside(self):
        
        # player.rect.bottom = HEIGHT - 30
        # player.rect.centerx = WIDTH/2
        # 测试用码，需要改回上面的
        player.rect.bottom = 200
        player.rect.centerx = WIDTH/2
        self.all_sprites.add(player)
        seller = Seller(WIDTH/2, 100)
        self.all_sellers.add(seller)
        self.all_sprites.add(seller)

        shopping_images = []
        shopping_images.append(pygame.transform.scale(pygame.image.load(os.path.join("TraficLight//img","chocalate.jpg")).convert(),(ITEM_WIDTH,ITEM_HEIGHT)))
        shopping_images.append(pygame.transform.scale(pygame.image.load(os.path.join("TraficLight//img","Coca.webp")).convert(),(ITEM_WIDTH,ITEM_HEIGHT)))
        shopping_images.append(pygame.transform.scale(pygame.image.load(os.path.join("TraficLight//img","cookie.webp")).convert(),(ITEM_WIDTH,ITEM_HEIGHT)))
        shopping_images.append(pygame.transform.scale(pygame.image.load(os.path.join("TraficLight//img","notebook.jpg")).convert(),(ITEM_WIDTH,ITEM_HEIGHT)))
        shopping_images.append(pygame.transform.scale(pygame.image.load(os.path.join("TraficLight//img","toy.jpg")).convert(),(ITEM_WIDTH,ITEM_HEIGHT)))
        shopping_nums = [0 for x in shopping_images]

        waiting = True
        buying = False
        while waiting:

            clock.tick(FPS)
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.all_sprites.update()
            if player.rect.bottom > HEIGHT:
                waiting = False

            if buying == False:
                # player 与 seller 碰撞
                hits = pygame.sprite.spritecollide(player,self.all_sellers,False)
            if hits and buying == False:
                buying = True
                player.rect.bottom = seller.rect.bottom + 50
                
                

                while buying:
                    clock.tick(FPS)
                    screen.fill(WHITE)
                    draw_menu(shopping_images,shopping_nums)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            pos_x,pos_y = event.pos
                            if pos_x > WIDTH - 100 and pos_y > HEIGHT - 100:
                                buying = False
                            elif pos_y > 0 and pos_y < 100:
                                if pos_x < WIDTH  and pos_x > WIDTH - 230:
                                    shopping_nums[0] += 1

                    self.all_sprites.draw(screen) 
                    pygame.display.update()

            
            self.all_sprites.draw(screen) 
            pygame.display.update()

class Seller(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.bottom = pos_y


# sprite 群组
all_sprites = pygame.sprite.Group()
all_cars = pygame.sprite.Group()
all_shops = pygame.sprite.Group()
player = Player(pos[0],pos[1])
all_sprites.add(player)
for i in range(4):
    new_car(i)
light = Light(cross_list[0][0]+80,cross_list[0][1])
all_sprites.add(light)

target = Shop(WIDTH - 200, 200)
all_sprites.add(target)
all_shops.add(target)

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
        # 按击 Q 键 用于测试新的加入功能
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                calculating()

    # 更新游戏
    all_sprites.update()

    # 汽车与人发生碰撞
    hits = pygame.sprite.spritecollide(player,all_cars,True)
    for hit in hits:
        draw_pause(cry_img)
        new_car(hit.loadline)
        player.rect.bottom = HEIGHT - 10

    # 人与商店相撞 --- 之后应该给商店设置个门口
    hits = pygame.sprite.spritecollide(player,all_shops,False)
    for hit in hits:
        # position = player.rect.centerx,player.rect.bottom
        hit.inside()
        player.rect.centerx,player.rect.bottom = hit.rect.centerx,hit.rect.bottom+50


    # 页面显示
    screen.fill(WHITE)
    screen.blit(go_stop_img,(0,0))
    screen.blit(road_img,(0,HEIGHT/2))
    screen.blit(crossing_img,cross_list[0])
    screen.blit(home_img,(WIDTH-50,HEIGHT-50))
    all_sprites.draw(screen)
    pygame.display.update()






