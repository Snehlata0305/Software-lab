import functools as ft
import sys
import re

fname = str(sys.argv[1])
f = open(fname,'r')
line = f.readline()
names = re.sub(' +',' ',line).split(" ")
mapping ={key:0 for key in names}
uniques=[]
for name in names:
    if name not in uniques:
        uniques.append(name)

most=0
lucky=""
for name in names:
    mapping[name]+=1
    if mapping[name]>most:
        most=mapping[name]
        lucky=name
    elif mapping[name]==most:
        if(uniques.index(name) < uniques.index(lucky)):
            lucky = name
            most=mapping[name]

print(lucky)
