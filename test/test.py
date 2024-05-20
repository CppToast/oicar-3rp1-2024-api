params = (1, 2, 'a', False)

for i in range(len(params)):
    print('?', end='')
    if i < len(params) - 1:
        print(', ', end='')
