print('hello world')
print('hhh hello world')
for i in range(10):
    if i == 5:
        continue
    print(i)
f = open("new_file.txt", 'w')
f.write('hello world')
f.close()
f = open("new_file.txt", 'r')
print(f.read())
a = 1 + 1
print(a)

var = [1, 2, 3, 4, 5]
b = [2, 3, 4, 5]
print(b[2], var[2])
