from sympy import *

x, y = symbols('x, y')

z = x ** 2 + y ** 2 + x * y + 2
print(z)
result = z.subs({x: 1, y: 2})  # 用数值分别对 x、y 进行替换
print(result)

dx = diff(z, x)  # 对 x 求偏导
print(dx)
result = dx.subs({x: 1, y: 2})
print(result)

dy = diff(z, y)  # 对 y 求偏导
print(dy)
result = dy.subs({x: 1, y: 2})
print(result)

# subs 函数可以将算式中的符号进行替换，它有 3 种调用方式：
# expression.subs(x, y) : 将算式中的 x 替换成 y
# expression.subs({x:y,u:v}) : 使用字典进行多次替换
# expression.subs([(x,y),(u,v)]) : 使用列表进行多次替换
