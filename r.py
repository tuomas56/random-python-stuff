s=dict(zip([1,5,10,50,100,500,1000],"IVXLCDM"))
n=int(input())
o=""
while(n):x=max(filter(lambda x:x<=n,s.keys()));o+=s[x];n-=x if n>0 else
print("VXX" if n==0 else "IIIIIIV" if n == -1 else o)