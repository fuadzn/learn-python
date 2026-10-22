# False = 123
import array
import math
from soupsieve import css_match
from collections.abc import Iterable
x = 7
y = 7
print(x == y)
print(x is y)

print("hello" 'world')

greeting = "Fuad"
space = " "
name = "Blessing"
print(greeting + space + name)

print("Hello" r', ' f"{name}")

print(["one", "two", "three"])

if 2 * 3 == 6:
    print(True)

print({"one", "two", "three"})
print({"one": 1, "two": 2, "three": 3})

print([x**2 for x in range(10)])

def make_list_of_squares(iterable):
    result=[]
    for x in iterable:
        result.append(x**2)
    return result

print(make_list_of_squares(range(10)))

print({x.lower() for x in ['A', 'a', 'C', 'D']})

def make_lowercase_set(iterable):
    result = set()
    for x in iterable:
        result.add(x.lower())
    return result

print(make_lowercase_set(['a', 'A', 'b', 'C']))

def make_dic_mapping_names_to_functions(iterable):
    result = {}
    for func in iterable:
        result[func.__name__] = func
    return result

print(make_dic_mapping_names_to_functions([print, hex, any]))

print(tuple(x**2 for x in range(10)))

print([name for name in vars(math) if name.startswith("f")])

def get_math_f_names(iterable):
    result = []
    for name in iterable:
        if name.startswith("f"):
            result.append(name)
    return result

print(get_math_f_names(vars(math)))

print(10 + 5)

price = 100000
quantity = 5
total = price * quantity
print(f"Total Price: Rp. {total}")


name = "Fuad"
age = 25
print("My name is " + name + " and I am " + str(age) + " years old")
print(f"My name is {name} and I am {age} years old")

revenue = 150000.4567
print(f"Revenue : {revenue}")
print(f"Revenue : {revenue: .2f}")
print(f"Revenue : {revenue:,.2f}")

revenues = 150000000
print(f"Revenue: {revenues:,}")
print(f"Revenue: Rp. {revenues:,}".replace(",", "."))

discount = 0.8576
print(f"Discount: {discount:.1%}")

# Raw order data
product_name = "Laptop Macbook Air"
price_product = 25000000
quantity_product = 3
discount_rate = 0.10
is_paid = True

# Expressions
subtotal = price * quantity_product
discount_amount = subtotal * discount_rate
final_total = subtotal - discount_amount

# Data validation
is_valid = price > 0 and quantity_product > 0

# String formatting
print("======= SALES REPORT =======")
print(f"Product     : {product_name}")
print(f"Price       : Rp{price_product:,}")
print(f"Quantity    : {quantity_product}")
print(f"Subtotal    : Rp{subtotal:,}")
print(f"Discount    : {discount_rate:.0%}")
print(f"Final Total : Rp{final_total:,.2f}")
print(f"Valid       : {is_valid}")
print(f"Paid        : {is_paid}")
print(f"Order status: {'Paid' if is_paid else 'Unpaid'}")
print("============================")

[
    name
    for module in [array, math]
    for name in vars(module)
    if name.startswith('a')
]

def make_list_of_all_a_attributes(iterable):
    result = []
    for module in iterable:
        for name in vars(module):
            if name.startswith('a'):
                result.append(name)
    return result

print(make_list_of_all_a_attributes([array, math]))

students = ["Sandi", "Fuad", "Kazan"]
teachers = ["Pak Udin", "Pak Anto", "Bu Ratna"]
lists_of_people = [students, teachers]

def make_list_of_people(iterable):
    result = []
    for people in iterable:
        result.extend(people)
    return result

print(make_list_of_people(lists_of_people))

iterator = (x ** 2 for x in range(10))
print(list(iterator))

def make_list_of_squares_iterator(iterator):
    for x in iterator:
        yield x ** 2

print(list(make_list_of_squares_iterator(iter(range(10)))))

print(sum(x ** 2 for x in range(10)))
print(sum((x ** 2 for x in range(10)), start=1000))