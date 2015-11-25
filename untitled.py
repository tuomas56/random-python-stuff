from operator import*
o={"+":(add,2),"-":(sub,2),"*":(mul,2),"/":(truediv,2),"^":(lambda a,b:a**b,2)}
s=[]
for x in input().split(" "): 
 try:s=[float(x)]+s
 except:s.append(o[x][0](*[s.pop()for _ in range(o[x][1])]))
print(s[0])