'''Name: Linh Nguyen
Class: CS260
Professor: Kent Lee
Turing Machine'''
class Tape:
    def __init__(self,word):
        a=[' ']
        self.tape=a*100
        while 2*len(word)+2>len(self.tape):
            self.tape=a*2*self.tape
        self.tape+=[" "]*len(word)
        self.middle=len(self.tape)//2-1
        self.tape[self.middle]="$"        
        self.readLocation=self.middle
        middle=self.middle-1
        self.tape[middle]="$"        
        for i in word:
            self.tape[middle+1]=i
            middle+=1
        self.tape[middle+1]="$"
    
    def moveLeft(self):
        self.readLocation=self.readLocation-1
    
    def moveRight(self):
        self.readLocation=self.readLocation+1
    
    def read(self,item):
        if item in self.tape:
            return item
        else:
            return None
    
    def write(self,sym):
        self.tape[self.readLocation]=sym
            
    def __str__(self):
        string=""
        for i in self.tape:
            if i!=" " and i!="$" and i!="x":
                string+=i
        return string

def turingMachine(tapeStr,delta,accepting):
    toState=0
    char=tapeStr.tape[tapeStr.readLocation]
    if (toState,char) in delta:
        (toState,sym,move)=delta[(toState,char)]
    else:
        print("Not applicable")
        return 0
    while toState not in accepting and move!="halt":
        tapeStr.write(sym)
        if move=="L":
            tapeStr.moveLeft()
        elif move=="R":
            tapeStr.moveRight()
        char=tapeStr.tape[tapeStr.readLocation]
        if (toState,char) in delta:
            (toState,sym,move)=delta[(toState,char)]
        else:
            print("Not applicable")
            return 0           
    return tapeStr
    
def main():
    word=input("Please enter a word: ")
    while word!="":
        if not "$" in word:
            string=Tape(word)
        else:
            word=word.replace("$",'')
            string=Tape(word)
        #print(string)
        delta={(0,'$'):(0,'$',"R"),(0,'x'):(0,'x',"R"),(0,'r'):(2,'x',"L"),(0,'e'):(3,'x',"L"),
               (0,'s'):(4,'x',"L"),(0,'v'):(5,'x',"L"),(1,'$'):(0,'$',"R"),(1,'r'):(1,'r',"R"),
               (1,'e'):(1,'e',"R"),(1,'v'):(1,'v',"R"),(1,'s'):(1,'s',"R"),(2,'$'):(6,'$',"L"),
               (2,'x'):(2,'x',"L"),(3,'$'):(7,'$',"L"),(3,'x'):(3,'x',"L"),(4,'$'):(9,'$',"L"),
               (4,'x'):(4,'x',"L"),(5,'$'):(8,'$',"L"),(5,'x'):(5,'x',"L"),(6," "):(1,'r',"R"),
               (6,'r'):(6,'r',"L"),(6,'s'):(6,'s',"L"),(6,'v'):(6,'v',"L"),(6,'e'):(6,'e',"L"),
               (7," "):(1,'e',"R"),(7,'r'):(7,'r',"L"),(7,'s'):(7,'s',"L"),(7,'v'):(7,'v',"L"),
               (7,'e'):(7,'e',"L"),(8," "):(1,'v',"R"),(8,'r'):(8,'r',"L"),(8,'s'):(8,'s',"L"),
               (8,'v'):(8,'v',"L"),(8,'e'):(8,'e',"L"),(9," "):(1,'s',"R"),(9,'r'):(9,'r',"L"),
               (9,'s'):(9,'s',"L"),(9,'v'):(9,'v',"L"),(9,'e'):(9,'e',"L"),(0," "):(10," ","halt")}
        accepting=[10]
        result=turingMachine(string,delta,accepting)
        if result!=0:
            print("The reverse string is:",result)
        word=input("Please enter a word: ")
    print('Program completed')
if __name__=="__main__":
    main()
    
    
    
            
            
        