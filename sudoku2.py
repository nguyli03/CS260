def calVal(x,y,z):
    s=81*(x-1)+9*(y-1)+z
    return s

def main():
    #num=0
    sudokuFile=open('sudoku.txt','r')
    row=1
    col=0
    count=0
    saveVal=[]
    for i in range(1,10):
        line=sudokuFile.readline()
        noList=line.split()
        col=0
        for aVal in noList:
            col+=1
            if aVal!="x":
                saveVal.append(calVal(row,col,int(aVal)))
                count+=1
        row+=1
    print("p cnf",729,8829+count)
#print the value in the table    
    for val in saveVal:
        print(val,0)
    for x in range(1,10):
        for y in range(1,10):
            for z in range(1,10):
                s=calVal(x,y,z)
                print(s,end=" ")
            print(0)
            #num+=1
#There is at least one number in each entry:    
    for y in range(1,10):
        for z in range(1,10):
            for x in range(1,9):
                for i in range(x+1,10):
                    s1=calVal(x,y,z)
                    s2=calVal(i,y,z)
                    print(s1*(-1), s2*(-1),0)
                    #num+=1
#Each number appears at most once in each row:
    for x in range(1,10):
        for z in range(1,10):
            for y in range(1,9):
                for i in range(y+1,10):
                    s1=calVal(x,y,z)
                    s2=calVal(x,i,z)
                    print(s1*(-1),end=" ")
                    print(s2*(-1),0)
                    #num+=1  
#Each number appears at most once in each column:    
    for z in range(1,10):
        for i in range(0,3):
            for j in range(0,3):
                for x in range(1,4):
                    for y in range(1,4):
                        for k in range(y+1,4):
                            s1=calVal(3*i+x,3*j+y,z)
                            s2=calVal(3*i+x,3*j+k,z)
                            print(s1*(-1),end=" ")
                            print(s2*(-1),0)
                            #num+=1                              
#Each number appears at most once in each 3x3 sub-grid:    
    for z in range(1,10):
        for i in range(0,3):
            for j in range(0,3):
                for x in range(1,4):
                    for y in range(1,4):
                        for k in range(x+1,4):
                            for l in range(1,4):
                                s1=calVal(3*i+x,3*j+y,z)
                                s2=calVal(3*i+k,3*j+l,z)
                                print(s1*(-1),end=" ")
                                print(s2*(-1),0)
                                #num+=1                                 
    
    #print(num)
main()