import random

Char_list = ['A','B','C','D','E','F','G']
# 列出方程组,参数为: 未知数的个数,未知数可取的最大值
def draw_equation_set(nums,largest):
    # 随机生成未知数
    randnums = random.choices(list(range(largest)),k=nums)
    numchars = Char_list[:nums]
    # numchars.append(Char_list[0])
    print(randnums)
    print(str(numchars))
    for i in range(nums):
        a = randnums[i]
        if i+1 == nums:
            i = -1
        b = randnums[i+1]
        c = a+b
        print('a='+str(a) + ', b='+str(b) + ', a+b='+str(c))
        print(str(numchars[i]) + ' + ' + str(numchars[i+1]) + ' = ' + str(c))

draw_equation_set(3,10)