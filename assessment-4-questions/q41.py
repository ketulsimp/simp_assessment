l=[1, [2, [3, 4], [5, [6, 7]]], 8]

l1=[]
for i in range(len(l)):
    if l[i] is list:
        print('jkfghjk')
    l1.append(l[i])

print(l1)