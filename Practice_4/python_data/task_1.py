import datetime

x = datetime.datetime.now()
y = x.day-5
y = x.replace(day=y)
print(x)