a = 2
b = 3
print(a)
del b
if not 'b' in locals():
    print('coucou')