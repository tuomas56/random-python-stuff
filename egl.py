var -> f => var
var = i | i <- var | f i
var = filter(f,var)

var -> f -> var
(f i) -> (var << i) | i <- var
var.extend(filter(f,var))

var => f :: Func :=> var
var = f i | i <- var
var = map(f,var)

var => f :-> var
var << (f i) | i <- var
var.extend(map(f,var))


(x) :> y
	 z
if x:
	y
	z

x << i
x.append(i)

x = i
x = i


f x y = x*y
f = lambda x: lambda y: x * y

f x
f(x)

f x y
f(x)(y)

[0,1,2]_x
[0,1,2][x]

{'a' => 'b','c' => 'd'}
{'a':'b','c':'d'}

var => x :: Dict => var
var = map(lambda y: x[y],var)

\x.x
lambda x: x

var => f >> g
g(map(f,var))

[1..] -> \y.x => |_| => print("Valid") 
--filtering an infinite iterator by a constant boolean function and mapping it to a do block is how while is acheived. This has a syntactic sugar:
@x => print("Valid")
while x:
	print("Valid")

y => |x| => print x
--Map every element of y to the do block (like a function but must be the end of the chain and can contain more that one statement)
--In this case we could use:
y => print
for x in y:
	print(x)


e.g)

(x => f -> not 1 => lt 10 >> any) -> print "Valid"

if any(map(lambda x: x < 10,filter(lambda x: x != 1,map(f,x)))): print("Valid")




