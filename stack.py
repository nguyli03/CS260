class Stack:
    def __init__(self,lst=[]):
        self.lst=lst[:]
        #do not let the original to be modify
    def pop(self):
        return self.lst.pop()
    def push(self,item):
        self.lst.append(item)
    def isEmpty(self):
        return len(self.lst)==0
    def peek(self):
        return self.lst[len(self.lst)-1]
    def __len__(self):
        return len(self.lst)
    def __add__(self,item):
        s=Stack(self.lst)
        s.push(item)
        return s
    #implement a function so you can do s=s+5
    
    def __repr__(self):
        return "Stack("+repr(self.lst)+")"
    
    def __str__(self):
        s="bottom::"
        for k in self.lst:
            s+=" "+str(k)
        return s+"::top"
    
def main():
    s=Stack([1,2,3,4,5])
    print(repr(s))
    print(s)
    
if __name__=="__main__":
    main()