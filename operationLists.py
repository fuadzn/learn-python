# Without list comprehension
squares = []
for i in range(5):
    squares.append(i ** 2)
print(squares)

# With list comprehension
squares_with_comp = []
squares_with_comp = [i ** 2 for i in range(5)]
print(squares_with_comp)
