import datetime as dt

x = dt.datetime.now()
print(x.strftime("%c"))

f = open('1_status.log', 'a')
f.write(x.strftime("%c")+'\n')
f.close()