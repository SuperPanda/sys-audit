import re

v1 = '500.232G'
v2 = '2T'

a = {
    'K': 1024,
    'M': 1024*1024,
    'G': 1024*1024*1024,
    'T': 1024*1024*1024*1024
}

def getBytes(value):
    return float(re.search("[0-9]+\.?[0-9]{0,3}",value)[0]) * float(a[re.search("[A-Z]$",value)[0]])

print(getBytes(v2))
print(getBytes(v1))
print((getBytes(v1) / getBytes(v2))*100)
