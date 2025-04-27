def fact():
    if n==1 or n==0: print(1)
    elif n>0:
              d=1
              for i in range(2,n+1,1):
                         d*=i
              print(d)
n=int(input())
fact()
