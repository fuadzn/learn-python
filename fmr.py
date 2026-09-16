# Filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Filter even numbers
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

# Map
def power2(val: int) -> int:
    return val*val

powered_numbers = list(map(power2, numbers))
# OR
squared_numbers = list(map(lambda x: x**2, numbers))
print(powered_numbers)
print(squared_numbers)

# Reduce
from functools import reduce
words = ["apple", "banana", "orange", "apple", "grape", "banana"]

# Count the occurences of each word
word_counts = reduce(lambda counts, word: {**counts, word: counts.get(word, 0) + 1}, words, {})
print(word_counts)

numberss = [1,2,3,4,5]
product = reduce((lambda x, y: x* y), numberss)
print(product)