import state
import io
import streamreader
#from nfa import NFA
from stack import Stack
epsilon = "epsilon"
    
class NFA:
    def __init__(self,states,classes):
        self.states = states
        self.startStateId = 0
        self.classes = classes
    
    #fix it, it need to take in a set of states
    '''def eClosure(self,stateIdSet):
        statesStack=Stack()
        eClosure=set()
        for cls in self.states.keys():
            statesStack.push(cls)
        while not statesStack.isEmpty():
            stateId=statesStack.pop()
            for state in stateIdSet:
                if state not in eClosure:
                    if state.onClassGoTo(epsilon)==stateId:
                        statesStack.push(stateId)
                        eClosure.append(self.states[stateId])
                    else:   
                        statesStack.pop()
        return eclosure'''
        
        stateStack=Stack()
        eClosure=set()
        for state in stateIdSet:
            stateStack.push(state)
            eClosure.append(state)
        while not statesStack.isEmpty():
            currentStateId=statesStack.pop()
            for onClass, stateId on self.states[currentStateId].onGoTo(epsilon):
                
class DFA:
    def __init__(self):
        self.states = {}
        self.startStateId = None
        self.classes = {}

    
                
        
    '''def buildFromNFA(self,nfa):
        unexploreState=Stack()
        statesDFA=[]
        stateId=nfa.startStateId
        stateList=[nfa.startStateId]
        i=0
        n=i+1
        F={}
        def constructDFAStates(self,stateList,statesDFA):
            nextStateList=[]
            if stateList not in statesDFA:
                for stateId in stateList:
                    for onClass,stateId in nfa.states[stateId].getTransitions():
                        if onClass==epsilon:
                            while nfa.states[stateId].hasTransition('epsilon'):
                                stateId=nfa.states[stateId].onClassGoTo(onClass)
                                stateList.append[stateId]
                            unexploreState.push(i)
                            i+=1
                            #self.eClosure(nfa,nfa.states[stateId])
                        else:
                            for onClass2,stateId2 in nfa.states[stateId].getTransitions():
                                if onClass2==onClass:
                                    stateId=nfa.states[stateId].onClassGoTo(onClass)
                                    nextStateList.append(stateId)
                            unexploreState.push(n)
                            n+=1
                        for state in stateList:
                            if state.isAccepting():
                                F.append(i)
                statesDFA.append(stateList)
                statesList=nextStateList
                constructDFAStates(stateList,statesDFA)
                unexploreState.pop()
            return statesDFA
                
        return constructDFAStates(self,stateList,statesDFA)'''
    def buildFromNFA(self,nfa):
        dfaStartStateSet=nfa.eClosure(nfa.states[nfa.startStateId])
        dfaStartStateId=0
        dfaStartState=state.State(dfaStartStateId)
        for state in startStateSet:
            if state.isAccepting():
                startStateSet.setAccepting(1)
        
        dfaStates={}
        dfa2nfa={}
        unexploreState=Stack()
        
        dfa2nfa[dfaStateId]=dfaStartStateSet
        nfa2dfa[frozenset(dfaStartStateSet)]=dfaStateId
        dfaStates[dfaStateId]=startState
        unexploreState.push(dfaStateId)
        
        build(nfa,dfa2nfa[dfaStateId],dfa2nfa)
        def build(self,nfa,states,dfa2nfa):
            stateSet={}
            while not unexploreState.isEmpty():
                stateId=unexploreState.pop()
                for state in states:
                    for onClass, stateId in state.getTransitions():
                        if onClass!=epsilon:
                            #stateSet[onClass]=self.eClosure(nfa,stateId)
                            #for cls in nfa.classes:
                                #if state.hasTransitions(cls):
                                    #stateId=state.onClassGoTo(cls)
                            stateSet[onClass].append(nfa.states[stateId])
                            if nfa.states[stateId].hasTransition(epsilon):
                                #epState=nfa.states[stateId].onGoTo(epsilon)
                                epStates=nfa.eClosure(nfa,nfa.states[stateId])
                                for state in epStates:
                                    stateSet[onClass].append(nfa.states[state])
          #need a make transition function - gather classes       
                for cls in stateSet.keys():
                    #for i in nfa2dfa.keys():
                    if stateSet[cls] not in dfa2nfa.values():
                        dfaStateId+=1
                        dfa2nfa[dfaStateId]=stateSet[cls]
                        nfa2nfa[frozenset(stateSet[cls])]=dfaStateId
                            #make a state out of it and put it in the dfaState dictionary
                        dfaStates[dfaStateId]=state.State(dfaStateId)
                            #dfaStatesSet[dfaStateId]=stateSet[cls]
                        for state in dfa2nfa[dfaStateId]:
                            if state.isAccepting():
                                dfaStates[dfaStateId].setAccepting(1)
                            #add transition:
                        dfaStates[stateId].addTransition[cls,dfaStateId]
                        unexploreState.push(dfaStateId)
                        #otherwise, the state already exist:
                    else:
                        dfaStates[dfaStateId].addTransition(cls,nfa2dfa[frozenset(stateSet[cls])])
                       #does it need to be a frozenset to be looked up?             
            build(nfa,dfa2nfa[dfaStateId],dfa2nfa)      
            
    def writeListing(self):
        print("The Start State is: 0")
        print("%20s %20s %20s %20s"%("State","on Class","Go To","Accepting"))
        
              

def main():
    
    q0 = state.State(0)
    q1 = state.State(1,1)
    q2 = state.State(2)
    classes = {"zero":frozenset(["0"]), "one":frozenset(["1"]), "epsilon":frozenset([])}

    q0.addTransition("zero", 1)
    q0.addTransition("one", 1)
    q1.addTransition("zero", 0)
    q1.addTransition("one",1)
    q1.addTransition("zero",2)
    q1.addTransition("epsilon", 2)
    q2.addTransition("one",1)

    nfa = NFA({0:q0, 1:q1, 2:q2} classes)
    
    dfa = DFA()
    print(dfa.buildFromNFA(nfa))
    #dfa.writeListing(sys.stdout)
    
    
main()
                        
                                
                    
                
                