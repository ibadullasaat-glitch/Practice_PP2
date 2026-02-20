import datetime

x = datetime.datetime.now()
y = x.day-5
y = x.replace(day=y)
print(x)


#--------------------------------------------------------------
import datetime

x = datetime.datetime.now()
y = datetime.datetime.now()
z = datetime.datetime.now()

a = x.day
b = y.day-1
c = z.day+1
print(b, a, c)


#---------------------------------------------------------------
import datetime
x = datetime.datetime.now()
y = x.replace(microsecond=0)
print(y)


#---------------------------------------------------------------
import datetime
x = datetime.datetime.now()
y = x - datetime.timedelta(days=1)
a = x.second
b = y.second
print(a-b)