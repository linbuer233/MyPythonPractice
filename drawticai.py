import random as rd
import turtle as tl


# 移动
def move(x, y):
    tl.penup()
    tl.goto(x, y)
    tl.pendown()


# 画号码，把号码填进去
def circle(x, y, r, num, colornum):
    color = ['red', 'green']
    move(x, y)
    tl.color(color[colornum])
    tl.begin_fill()
    tl.circle(r)
    tl.end_fill()
    tl.color('black')
    move(x, y + r / 2)
    tl.write(str(num), align='center', font=('楷体', 40, 'bold'))


# 随机生成抽奖号码
def coulist(num, st, end):
    coulist = []
    count = 0
    while True:
        temp = rd.randint(st, end)
        if temp in coulist:
            continue
        coulist.append(temp)
        count += 1
        if count == num:
            break
    return coulist


if __name__ == '__main__':
    move(-360, 300)
    tl.write('Linux和Python气象应用大乐透', font=('楷体', 40, 'bold'))
    move(-360, 230)
    tl.write('本期中奖号码', font=('楷体', 40, 'bold'))
    xall = [-300, -150, 0, 150, 300, 150, 300]
    yall = [50, 50, 50, 50, 50, -100, -100]
    numall = coulist(5, 1, 35) + coulist(2, 1, 12)
    colorall = [0, 0, 0, 0, 0, 1, 1]
    for x, y, num, colornum in zip(xall, yall, numall, colorall):
        if input() == '':
            circle(x, y, 60, num, colornum)
    tl.exitonclick()
