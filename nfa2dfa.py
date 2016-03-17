#Name: Linh Nguyen
#Class: CS260
#Professor: Kent Lee
#Project: Build DFA from NFA

import sys
from state import *
from stack import *
from orderedCollection import *

class NFA:
    def __init__(self,classes,states):
            self.states = states
            self.startStateId = 0
            self.classes = classes    

class DFA():
    def __init__(self):
        self.classes=None
        self.states=None
    
    def buildFromNFA(self,nfa):
        
        def eClosure(stateIdSet):
            closedSet=OrderedSet(stateIdSet)
            unexploredStates= Stack()
            #push the states in the Stack
            for stateId in closedSet:
                unexploredStates.push(stateId)
                
            while not unexploredStates.isEmpty():
                currentStateId=unexploredStates.pop()
                for onClass, toStateId in nfa.states[currentStateId].getTransitions():
                    if onClass.upper()=="EPSILON" and not toStateId in closedSet:
                        closedSet.add(toStateId)
                        unexploredStates.push(toStateId)
            
            return OrderedFrozenSet(closedSet)
        
        def gatherClasses(stateIdSet):
                listOfClasses=[]
                for cls in nfa.classes:
                    for state in stateIdSet:
                        if nfa.states[state].hasTransition(cls) and cls not in listOfClasses\
                        and cls.upper()!="EPSILON":
                            listOfClasses.append(cls)
                return listOfClasses
        
        self.states=OrderedMap()
        self.classes=nfa.classes
        
        startStateSet=OrderedSet([0])
        startStateSet=eClosure(startStateSet)
        
        self.nfa2dfa={}
        self.dfa2nfa={}
        
        dfaCurrentStateId=0
        
        unexploredStatesStack=Stack()
        
        unexploredStatesStack.push(dfaCurrentStateId)
        self.dfa2nfa[dfaCurrentStateId]=startStateSet
        
        self.states[dfaCurrentStateId]=State(dfaCurrentStateId)
        while not unexploredStatesStack.isEmpty():
            #add the set of States into nfaSet 
            
            stateIdSet=unexploredStatesStack.pop()
            listOfClasses=gatherClasses(self.dfa2nfa[stateIdSet])

            for cls in listOfClasses:
                nfaSetId=OrderedSet()
                for stateId in self.dfa2nfa[stateIdSet]:
                    listOfTransitions=nfa.states[stateId].getTransitions()
                    for onClass,toStateId in listOfTransitions:
                        if onClass==cls and onClass!="EPSILON":
                            nfaSetId.add(toStateId)
                nfaSet=eClosure(nfaSetId)
                
                if nfaSet not in self.nfa2dfa:
                    dfaCurrentStateId+=1
                    self.nfa2dfa[nfaSet]=dfaCurrentStateId
                    self.dfa2nfa[dfaCurrentStateId]=nfaSet
                
                    unexploredStatesStack.push(dfaCurrentStateId)
                    #create new dfa States and create transition
                    self.states[dfaCurrentStateId]=State(dfaCurrentStateId)
                    self.states[stateIdSet].addTransition(cls,dfaCurrentStateId)
                else:
                    self.states[stateIdSet].addTransition(cls,self.nfa2dfa[nfaSet])
                 
        for stateId in self.states.keys():
            for nfaState in self.dfa2nfa[stateId]:
                if nfa.states[nfaState].isAccepting():
                    self.states[stateId].setAccepting(1)
    
    def writeListing(self,strm):
        strm.write("The Start State is: 0\n")
        strm.write("%0s %20s %20s %20s"%("State","on Class","Go To","Accepting\n"))
        strm.write("%0s %20s %20s %20s"%("-----","--------","------","--------\n"))
        for stateId in self.states.keys():
            if self.states[stateId].isAccepting():
                strm.write("%0s %20s %20s %20s"%(stateId,'','',"yes\n"))
                strm.write('\n')
            else:
                strm.write("%0s %20s %20s %20s"%(stateId,'','','\n'))
                strm.write("\n")
            for onClass, toStateId in self.states[stateId].getTransitions():
                strm.write("%0s %20s %20s %20s"%("",onClass,toStateId,'\n'))
                strm.write("\n")
        

def main():
    q0 =State(0)
    q1 =State(1)
    q2 =State(2)
    q3 =State(3)
    q4 =State(4)
    q5 =State(5)
    q6 =State(6)
    q7 =State(7)
    q8 =State(8)
    q9 =State(9)
    q10 =State(10)
    q11=State(11,1)
    
    classes = {"a":frozenset(["a"]), "epsilon":frozenset([])}

    q0.addTransition('epsilon',1)
    q0.addTransition('epsilon',7)  
    q1.addTransition('epsilon',6)
    q6.addTransition('epsilon',11)
    q6.addTransition('epsilon',1)
    q7.addTransition('epsilon',10)
    q10.addTransition('epsilon',11)
    q10.addTransition('epsilon',7)
    
    
    q1.addTransition('a',2)
    q2.addTransition('a',3)
    q3.addTransition('a',4)
    q4.addTransition('a',5)
    q5.addTransition('a',6)
    q7.addTransition('a',8)
    q8.addTransition('a',9)
    q9.addTransition('a',10)
    
    states={0:q0,1:q1,2:q2,3:q3,4:q4,5:q5,6:q6,7:q7,8:q8,9:q9,10:q10,11:q11}
    nfa=NFA(classes,states)
    
    dfa=DFA()
    dfa.buildFromNFA(nfa)
    dfa.writeListing(sys.stdout)
    print('complete')
main()