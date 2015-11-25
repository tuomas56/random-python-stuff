l,f,p=len,lambda n:list(filter(lambda b:n%b==0,range(2,n))),lambda n:l(f(n))==0;r=lambda n: n if p(n) else[x if p(x) else r(x) for x in [f(n)[0],f(n)[l(f(n))-1]]]
print(r(168));