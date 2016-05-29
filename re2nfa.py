import sys
from state import *
from stack import *
from orderedCollection import *
import streamreader
digits = set(list("0123456789"))
lettersdigitsunderscore = set(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"))
letters = set(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"))

class NFA():
    def __init__(self):
        self.states={}
        self.classes={}
        self.keywords={}
    def buildFromLanguage(self,instream):
        reader = streamreader.StreamReader(instream)
        startStates = []
        
        reader.skipComments()
        
        if reader.peek("#CLASSES"):
            #print("Found #CLASSES")
            reader.readUpTo("\n")
            while (not reader.peek("#")):
                # The "#" marks the beginning of the next section. Either KEYWORDS or TOKENS. KEYWORDS are optional.
                reader.skipComments()
        
                # We could have keywords right after a comment. So if keyword section is found, don't read
                # any more character classes.
                if not reader.peek("#KEYWORDS"):
                    className = reader.readIdentifier()
                    reader.readUpTo("=")
                    if reader.peek("^"):
                        anticlass = True
                        reader.readUpTo("^")
                        #classSet = orderedCollection.OrderedSet(range(256))
                        classSet = OrderedSet(range(256))
                    else:
                        anticlass = False
                        #classSet = orderedCollection.OrderedSet()
                        classSet =OrderedSet()
                    done = False
        
                    while not done:
        
                        if reader.peek("'"):
                            # Found a character constant
                            reader.readUpTo("'")
                            character = reader.readUpTo("'")[0]
                            #print(character)
                            ordVal = ord(character)
        
                        else:
                            ordVal = reader.readInt()
        
                        # Add the end of the range if there is a range of characters
                        if reader.peek(".."):
                            reader.readUpTo("..")
        
                            if reader.peek("'"):
                                reader.readUpTo("'")
                                character = reader.readUpTo("'")[0]
                                #print(character)
                                lastOrdVal = ord(character)
                            else:
                                lastOrdVal = reader.readInt()
                        else:
                            lastOrdVal = ordVal
        
                        # Now build the set
                        for i in range(ordVal, lastOrdVal+1):
                            if anticlass:
                                classSet.remove(i)
                            else:
                                classSet.add(i)
        
                        if reader.peek(","):
                            reader.readUpTo(",")
                        else:
                            done = True
        
                    #print(className)
        
                    #Add the class to the class dictionary
                    self.classes[className] = classSet
        
                    reader.readUpTo(";")
        
        
        #print("These are the classes")
        #print(self.classes)
        # keyword and token id numbers
        idnum = 0
        keywordsPresent = False
        
        if reader.peek("#KEYWORDS"):
            reader.readUpTo("#KEYWORDS")
            keywordsPresent = True
            reader.skipComments()
        
            while (not reader.peek("#TOKENS")):
                #idnum = reader.readInt()
                #reader.readUpTo(":")
                reader.readUpTo("'")
                keyword = reader.readUpTo("'")[:-1].strip()
                #print(idnum,keyword)
                self.keywords[keyword] = idnum
                idnum += 1
                reader.readUpTo(";")
                reader.skipComments()
        
        #print(self.keywords)
        reader.readUpTo("#TOKENS")
        reader.skipComments()        
        
        listOfEx={}
        listOfEx['(']=0
        listOfEx['|']=1
        listOfEx['.']=2
        listOfEx['*']=3
        finalStateOfEachToken=[]
        startStateOfEachToken=[]
        i=1
        while not reader.peek("#DEFINITIONS"):
            operands=Stack()
            operators=Stack()
            operators.push('(')                       
            if not reader.peek("'"):
                accepting = reader.readIdentifier()
                reader.readUpTo("=")
                machine={}
                m=1
                startState={}
                finalState={}                

                c=reader.readChar()
                while not reader.peek(";"):
                    if c in letters:
                        reader.unreadChar(c)
                        token=reader.getToken()
                        if token in self.classes:
                            self.states[i]=state.State(i)
                            self.states[i+1]=state.State(i+1)
                            self.states[i].addTransition(token,i+1)
                            startState[m]=i
                            finalState[m]=i+1
                            i+=2
                            machine[m]=m
                            operands.push(m)
                            m+=1
                    else:
                        operator=reader.readChar()
                        if operator=='(':
                            operators.push(operator)
                        elif operator==')':
                            self.state[i]=state.State(i)
                            m2=operands.pop()
                            m1=operands.pop()
                            m2fs=startState[m2]
                            m1fs=startState[m1]
                            self.states[m1fs].addTransition['EPSILON',i]
                            self.states[m2fs].addTransition['EPSILON',i]
                            self.state[i+1]=state.State(i+1)
                            m2ls=finalState[m2]
                            m1ls=finalState[m1]
                            self.states[m1ls].addTransition['EPSILON',i+1]
                            self.states[m2ls].addTransition['EPSILON',i+1]
                            i+=2
                            machine[m]=m
                            operands.push(m)
                            m+=1
                        else:
                            while len(operators)>0 and listOfEx[operator]<=listOfEx[operators.peek()]:
                                self.state[i]=state.State(i)
                                m2=operands.pop()
                                m1=operands.pop()
                                m2fs=startState[m2]
                                m1fs=startState[m1]
                                self.states[m1fs].addTransition['EPSILON',i]
                                self.states[m2fs].addTransition['EPSILON',i]
                                self.state[i+1]=state.State(i+1)
                                m2ls=finalState[m2]
                                m1ls=finalState[m1]
                                self.states[m1ls].addTransition['EPSILON',i+1]
                                self.states[m2ls].addTransition['EPSILON',i+1]
                                i+=2
                                machine[m]=m
                                operands.push(m)
                                m+=1
                            operators.push(operator)
                while len(operators)>0 and len(operands)>=2:
                    self.state[i]=state.State(i)
                    m2=operands.pop()
                    m1=operands.pop()
                    m2fs=startState[m2]
                    m1fs=startState[m1]
                    self.states[m1fs].addTransition['EPSILON',i]
                    self.states[m2fs].addTransition['EPSILON',i]
                    self.state[i+1]=state.State(i+1)
                    m2ls=finalState[m2]
                    m1ls=finalState[m1]
                    self.states[m1ls].addTransition['EPSILON',i+1]
                    self.states[m2ls].addTransition['EPSILON',i+1]
                    i+=2
                    machine[m]=m
                    operands.push(m)
                    m+=1
                finalStateOfEachToken.append(i-1)
                startStateOfEachToken.append(i-2)
                self.states[i-1].setAccepting(accepting)
            else:
                reader.readUpTo("'")
                accepting=reader.readUpTo("'")
                accepting.strip("")
                startStateOfEachToken.append(i)
                for char in range(0,len(accepting)):                    
                    self.states[i]=state.State(i)
                    self.states[i+1]=state.States(i+1)
                    self.states[i].addTransition(accepting[char],i+1)
                    i+=2
                finalStateOfEachToken.append(i-1)
        self.states[0]=state.State(0)
        self.states[i]=state.State(i)
        for state in startStateOfEachToken:
            self.states[state].addTransition('EPSILON',0)
        for state in finalStateOfEachToken:
            self.state[state].addTransition('EPSILON',i)
    def writeListing(self,strm):
        print("The Start State is: 0")
        print("%0s %20s %20s %20s"%("State","on Class","Go To","Accepting"))
        print("%0s %20s %20s %20s"%("-----","--------","------","--------"))
        for stateId in self.states.keys():
            if self.states[stateId].isAccepting():
                print("%0s %20s %20s %20s"%(stateId,'','',"yes"))
                print()
            else:
                print("%0s %20s %20s %20s"%(stateId,'','',''))
                print()
            for onClass, toStateId in self.states[stateId].getTransitions():
                print("%0s %20s %20s %20s"%("",onClass,toStateId,''))
                print()
def main():
    nfa=NFA()
    file=open('language.txt','r')
    nfa.buildFromLanguage(file)
    nfa.writeListing(sys.stdout)
    
main()


                
                        
                                
                                
                            