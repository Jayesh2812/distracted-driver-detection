a = open('result.txt','r').read()
head =[
    'Epoch' ,
    'loss' ,
    'accuracy' ,
    'precision' ,
    'recall' ,
    'val_loss' ,
    'val_accuracy' ,
    'val_precision' ,
    'val_recall' ,
]
data = [head]
a = a.split('\n')
epochs = len(a)//2
a = [ f'{a[i]} - {a[i+1]}' for i in range(0, 2 * epochs, 2) ]
for i in range(epochs):
    t = a[i].split(' - ')
    t.pop(1)
    t.pop(1)
    temp = []
    for val in t:
        if 'Epoch' in val:
            print('Epoch', val.split()[-1].split('/')[0])
            temp.append(val.split()[-1].split('/')[0])
        else:
            key, value = val.split(': ')
            print(key, value)
            temp.append(value)
    data.append(temp)


for row in data:
    print(*row)
