import sys

n=int(input())
i=0

#-------------------to print dict of matches
match={}
while i!=n:
	matchdict=sys.stdin.readline().strip()[:]
	i+=1
	k,v=matchdict.split(':')
	v= dict((x.strip(),y.strip())
        for x, y in (element.split('-')  
        for element in v.split(',')))
	match[k]=v
print(match) 

#------------to print the dict of total of each player
matchlist={}
for key, value in match.items():
	for k,v in value.items():
		matchlist[k]=matchlist.get(k,0)+int(v)

#-------------to convert above dict in list of tuples and then to sort it
tpl=[(s,t) for s,t in matchlist.items()]
tpl.sort(key=lambda tup:tup[0])
print(tpl)