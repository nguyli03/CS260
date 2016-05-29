#At leasr one number in each entry:
'''s=''
for k in range(1,10):
    for  i in range(1,10):
        s+=str(i)+str(k)
        for i in range(1,10):
            a=s
            a+=str(i)+' '
            print(a,end=' ')
        print(0)
        s=''
'''
#each number appears at most once in each column:
'''start="-"
x='-'
for first in range(1,10):
    for i in range(1,10):
        for k in range(1,10):
            for n in range(first+1,10):
                x='-'+str(first)+str(i)+str(k)
                start+=str(n)+str(i)+str(k)
                print(x,start,0)
                start="-"
'''
#each number appear at most in each row:
'''start="-"
x='-'
for first in range(1,10):
    for i in range(1,10):
        for k in range(1,10):
            for n in range(first+1,10):
                x='-'+str(i)+str(first)+str(k)
                start+=str(i)+str(n)+str(k)
                print(x,start,0)
                start="-"
'''
#each number appear at most one in each 3x3 grid:
#x='-'
#start='-'
#for  i in range(1,4):
    