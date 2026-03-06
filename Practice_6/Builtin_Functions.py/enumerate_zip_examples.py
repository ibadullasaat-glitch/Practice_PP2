names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for i, name in enumerate(names):
    print(i, name)
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")


#------------------------------------------------------------------
x = "123"
print(type(x))  

x_int = int(x)
print(type(x_int))  

y = 3.14
y_str = str(y)
print(y_str) 

