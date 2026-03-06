import math
x = math.pi
y = int(input("Enter a number: "))
z = (y*x)/180
print(z)


#---------------------------------------------------------------
h = int(input("Enter the height of the trapezoid: "))
a = int(input("Enter the length of the first base: "))
b = int(input("Enter the length of the second base: "))
area = (a + b) * h / 2
print(area)


#---------------------------------------------------------------
import math

def regular_polygon_area(n, s):
    area = (n * s * s) / (4 * math.tan(math.pi / n))
    return area
n = int(input("Enter the number of sides: "))
s = float(input("Enter the length of a side: "))
area = regular_polygon_area(n, s)
print("The area of the regular polygon is:", area)



#---------------------------------------------------------------
h = int(input("Enter the height of the parallelogram: "))
b = int(input("Enter the base of the parallelogram: "))
area = b * h
print(area)