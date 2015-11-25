from random import*
s=randint(3,20)
x=s%2
print('\n'.join("Loves me%s..."%(n%2*" not")for n in range(s-1)),'\nLoves me%s\n<%s3'%(x*(' not.','/')+(not x)*('!',"")))