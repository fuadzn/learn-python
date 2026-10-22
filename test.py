# Last login: Mon Oct 19 22:34:37 on ttys004
# fuadzaidannajib@Fuads-MacBook-Air ~ % fm
# zsh: command not found: fm
# fuadzaidannajib@Fuads-MacBook-Air ~ % python
# zsh: command not found: python
# fuadzaidannajib@Fuads-MacBook-Air ~ % python3
# Python 3.14.7 (main, Aug  5 2026, 10:29:49) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# >>> exit
# fuadzaidannajib@Fuads-MacBook-Air ~ % cd
# fuadzaidannajib@Fuads-MacBook-Air ~ % cd ..
# fuadzaidannajib@Fuads-MacBook-Air /Users % cd..
# zsh: command not found: cd..
# fuadzaidannajib@Fuads-MacBook-Air /Users % cd ..
# fuadzaidannajib@Fuads-MacBook-Air / % ls
# Applications	Users		cores		home		sbin		var
# Library		Volumes		dev		opt		tmp
# System		bin		etc		private		usr
# fuadzaidannajib@Fuads-MacBook-Air / % cd usr 
# fuadzaidannajib@Fuads-MacBook-Air /usr % ls 
# X11		bin		libexec		sbin		standalone
# X11R6		lib		local		share
# fuadzaidannajib@Fuads-MacBook-Air /usr % cd local 
# fuadzaidannajib@Fuads-MacBook-Air local % ls
# bin	go
# fuadzaidannajib@Fuads-MacBook-Air local % cd bin 
# fuadzaidannajib@Fuads-MacBook-Air bin % ls
# docker				kiro				orbctl
# docker-compose			kubectl
# docker-credential-osxkeychain	orb
# fuadzaidannajib@Fuads-MacBook-Air bin % cd
# fuadzaidannajib@Fuads-MacBook-Air ~ % python -m site
# zsh: command not found: python
# fuadzaidannajib@Fuads-MacBook-Air ~ % python33 -m site
# zsh: command not found: python33
# fuadzaidannajib@Fuads-MacBook-Air ~ % python3 -m site 
# sys.path = [
#     '/Users/fuadzaidannajib',
#     '/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python314.zip',
#     '/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14',
#     '/opt/homebrew/Cellar/python@3.14/3.14.7/Frameworks/Python.framework/Versions/3.14/lib/python3.14/lib-dynload',
#     '/opt/homebrew/lib/python3.14/site-packages',
#     '/opt/homebrew/opt/python@3.14/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages',
# ]
# USER_BASE: '/Users/fuadzaidannajib/Library/Python/3.14' (doesn't exist)
# USER_SITE: '/Users/fuadzaidannajib/Library/Python/3.14/lib/python/site-packages' (doesn't exist)
# ENABLE_USER_SITE: True
# fuadzaidannajib@Fuads-MacBook-Air ~ % pyhton3
# zsh: command not found: pyhton3
# fuadzaidannajib@Fuads-MacBook-Air ~ % python3
# Python 3.14.7 (main, Aug  5 2026, 10:29:49) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
# Type "help", "copyright", "credits" or "license" for more information.
# >>> the_world_is_flat = true;
# Traceback (most recent call last):
#   File "<python-input-0>", line 1, in <module>
#     the_world_is_flat = true;
#                         ^^^^
# NameError: name 'true' is not defined. Did you mean: 'True'?
# >>> the_world_is_flat = True
# >>> if the_world_is_flat:
# ...     print("Be careful not to fall off!")
# ...     
# Be careful not to fall off!
# >>> print("Hello World!")
# Hello World!
# >>> 2 + 2
# 4
# >>> 50 - 5*6
# 20
# >>> 8 / 5
# 1.6
# >>> width = 20
# >>> height = 9 * 5
# >>> width * height
# 900
# >>> s = 'First line.\nSecond Line.'
# >>> s
# 'First line.\nSecond Line.'
# >>> s = 'First line.\nSecond Line.'
# >>> print(s)
# First line.
# Second Line.
# >>> print('C:\this\name')
# C:	his
# ame
# >>> 'fuad ' 'zaidan'
# 'fuad zaidan'
# >>> cubs = [1, 2, 27, 65, 125]
# >>> cubs
# [1, 2, 27, 65, 125]
# >>> cubs[3] = 64
# >>> cubs
# [1, 2, 27, 64, 125]
# >>> cubs.append(212)
# >>> cubs
# [1, 2, 27, 64, 125, 212]
# >>> cubs.append(7 * 3)
# >>> cubs
# [1, 2, 27, 64, 125, 212, 21]
# >>> rgb = ["Red", "Green", "Blue"]
# >>> rgba = rgb
# >>> id(rgb) == id(rgba)
# True
# >>> rgba.append("Alph")
# >>> tgb
# Traceback (most recent call last):
#   File "<python-input-28>", line 1, in <module>
#     tgb
# NameError: name 'tgb' is not defined. Did you mean: 'rgb'?
# >>> rgb
# ['Red', 'Green', 'Blue', 'Alph']
# >>> correct_rgba = rgba[:]
# >>> correct_rgba[-1] = "Alpha"
# >>> correct_rgba
# ['Red', 'Green', 'Blue', 'Alpha']
# >>> rgba
# ['Red', 'Green', 'Blue', 'Alph']
# >>> rgba[1] = []
# >>> rgba
# ['Red', [], 'Blue', 'Alph']
# >>> rgba[1] = null
# Traceback (most recent call last):
#   File "<python-input-36>", line 1, in <module>
#     rgba[1] = null
#               ^^^^
# NameError: name 'null' is not defined
# >>> rgba[1] = nil
# Traceback (most recent call last):
#   File "<python-input-37>", line 1, in <module>
#     rgba[1] = nil
#               ^^^
# NameError: name 'nil' is not defined
# >>> rgba[1] = nill
# Traceback (most recent call last):
#   File "<python-input-38>", line 1, in <module>
#     rgba[1] = nill
#               ^^^^
# NameError: name 'nill' is not defined
# >>> a, b = 0, 1
# >>> while a < 10:
# ...     print(a)
# ...     a, b = b, a+b
# ...     
# 0
# 1
# 1
# 2
# 3
# 5
# 8
# >>> x = int(input("Please enter an integer: "))
# Please enter an integer: 23
# >>> if x < 0:
# ...     x = 0
# ...     print("Negative changed to zero")
# ...     
# >>> x = int(input("Please enter an integer: "))
# Please enter an integer: -1
# >>> 
# >>> 
# >>> 2
# 2
# >>> 3
# 3
# >>> 4
# 4
# >>> x = int(input("Please enter an integer: "))
# Please enter an integer: 23
# >>> if x < 0:
# ...     x = 0
# ...     print("Negative changed to zero")
# ... elif x == 0:
# ...     print('Zero')
# ... elif x == 1:
# ...     print('Single')
# ... else:
# ...     print('More')
# ...     
# More
# >>> words = ['cat', 'window', 'defenestrate']
# >>> for w in words:
# ...     print(w, len(w))
# ...     
# cat 3
# window 6
# defenestrate 12
# >>> user = {'Hans': 'active', 'Eleonore': 'inactive', 'cawni': 'active'}
# >>> for user, status in users.copy().items():
# ...     if status == 'inactive':
# ...         del user[users]
# ...         
# KeyboardInterrupt
# >>> users = {'Hans': 'active', 'Eleonore': 'inactive', 'cawni': 'active'}
# >>> for user, status in users.copy().items():
# ...     if status == 'inactive':
# ...         del users[user]
# ...         
# >>> users
# {'Hans': 'active', 'cawni': 'active'}
# >>> active_users = {}
# >>> for user, status in users.items():
# ...     if status == 'active':
# ...         active_users[user] = status
# ...         
# >>> active_users
# {'Hans': 'active', 'cawni': 'active'}
# >>> for i in range(5)
#   File "<python-input-60>", line 1
#     for i in range(5)
#                      ^
# SyntaxError: expected ':'
# >>> for i in range(5):
# ...     print(i)
# ...     
# 0
# 1
# 2
# 3
# 4
# >>> list(range(0,10,3))
# [0, 3, 6, 9]
# >>> a = ['Mary', 'had', 'a', 'little', 'lamb']
# >>> for i in range(len(a)):
# ...     print(i, a[i])
# ...     
# 0 Mary
# 1 had
# 2 a
# 3 little
# 4 lamb
# >>> for n in range(2, 10):
# ...     for x in range(2, n):
# ...         if n % x == 0:
# ...             print(f"{n} equals {x} * {n//x}")
# ...             break
# ...             
# 4 equals 2 * 2
# 6 equals 2 * 3
# 8 equals 2 * 4
# 9 equals 3 * 3
# for  num in range(2, 10):
#     if num % 2 == 0:
#         print(f"Found an even number {num}")
#         continue
#     print(f"Found an odd number {num}")


# Else clauses on Loops
for n in range(2, 10):
    for x in range(2, n):
        if n % x == 0:
            print(n, 'equals', x, '*', n//x)
            break
    else:
        print(n, 'is a prime number')

def http_error(status):
    match status:
        case 400:
            return "Bad request"
        case 401 | 403 | 404:
            return "Not allowed"
        case 418:
            return "I'm a teapot"
        case _:
            return "Something's gone wrong"

print(http_error(400))
print(http_error(401))
print(http_error(403))
print(http_error(404))
print(http_error(418))
print(http_error(500))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def locate(point):
    match point:
        case Point(x=0, y=0):
            print("Origin")
        case Point(x=0, y=y):
            print(f"Y-axis at {y}")
        case Point(x=x, y=0):
            print(f"X-axis at {x}")
        case Point(x=x, y=y):
            print(f"Point at ({x}, {y})")
        case _:
            print("Not a point")

print(locate(Point(0, 0)))
print(locate(Point(0, 1)))
print(locate(Point(1, 0)))
print(locate(Point(1, 1)))

from enum import Enum

class Color(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

color = Color(input("Enter a color: "))

match color:
    case Color.RED:
        print('I see red')
    case Color.GREEN:
        print('I see green')
    case Color.BLUE:
        print('I see blue')
    case _:
        print("Not a color")

print(color)


def fib(n):
    a, b = 0, 1
    while a < n:
        print(a, end=' ')
        a, b = b, a + b
    print()

fib(1000)

class Dog:
    kind = 'cocaine'
    def __init__(self, name):
        self.name = name

d = Dog('Rex')

print(d.kind)
print(d.name)

class Cat:
    tricks = []
    def __init__(self, name):
        self.name = name

    def add_trick(self, trick):
        self.tricks.append(trick)

fido = Cat('Fido')
buddy = Cat('Buddy')
fido.add_trick('roll over')
buddy.add_trick('play dead')
print(fido.tricks)
print(buddy.tricks)
