lista = ['a', 'b', 'c', 'd', 'e']
count = 0
for l in lista:
    print('Index:', count, ' Value:', l)
    count += 1

# OR
print("\nUsing enumerate: ")
for index, value in enumerate(lista):
    print('Index:', index, ' Value:', value)