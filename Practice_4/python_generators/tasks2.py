def square_generator(N):
    for i in range(N + 1):
        yield i * i
N = int(input("Enter a number: ")) 
for square in square_generator(N):
    print(square)


#---------------------------------------------------------------
def even_generator(N):
    for i in range(N + 1):
        if i % 2 == 0:
            yield i
N = int(input("Enter a number: "))
for even in even_generator(N):
    print(even)


#---------------------------------------------------------------
def divisble_three_four_generator(N):
    for i in range(N + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i
N = int(input("Enter a number: "))
for num in divisble_three_four_generator(N):
    print(num)


#---------------------------------------------------------------
def squre_generator(a, b):
    for i in range(a, b + 1):
        yield i * i
a = int(input("Enter the start number: "))
b = int(input("Enter the end number: "))
for square in squre_generator(a, b):
    print(square)


#---------------------------------------------------------------
def all_generator(N):
    for i in range(N, -1, -1):
        yield i
N = int(input("Enter a number: "))
for num in all_generator(N):
    print(num)  