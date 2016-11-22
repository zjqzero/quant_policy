a = '>100'

b = 200

c = a[0]
v = a[1:]

print c, v

if eval(str(b) + c + v):
    print 'Yes'
