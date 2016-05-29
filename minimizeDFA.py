import sys
from state import *
from stack import *
from orderedCollection import *

class DFA():
    def __init__(self,classes,states):
        self.classes=classes
        self.states=states

class MinimumDFA():
    def __init__(self):
        self.classes=None
        self.states=None
    def buildFromDFA(self,dfa):
        def finer(minDFAStateId):
          #only one partition come out of the call of finer; changes has to be
          #set to true whenever finer return a change (receive true if there is 
          #at least a change in return
            stateSet=dfa2min[minDFAStateId]
            stateSet=sorted(stateSet)
            primaryState=stateSet[0]
            listOfTransitions=dfa.states[primaryState].getTransitions()
            if len(listOfTransitions)==0:
                for stateId in stateSet[1:]:
                    listOfTransitionOfStateId=dfa.states[stateId].getTransitions()
                    if len(listOfTransitionOfStateId)!=0:
                        self.newPartition.add(stateId)
                        dfa2min[minDFAStateId].remove(stateId)
            else:
                for onClass, toState in listOfTransitions:
                    for stateId in stateSet[1:]:
                        if not dfa.states[stateId].hasTransition(onClass) or \
                           toState!=dfa.states[stateId].onGoTo(onClass):
                            if not stateId in self.newPartition:
                                self.newPartition.add(stateId)
                                dfa2min[minDFAStateId].remove(stateId)
                                #print(self.newPartition)
                                
                            else:
                                if len(self.newPartition)!=0:
                                    #print(self.newPartition)
                                    return True
            if len(self.newPartition)!=0:
                #print(self.newPartition)
                return True                
            
            #go through the states and get it classes and find the toState, compare those listOfTransitions to each other           
                        
        self.states=OrderedMap()                  
        #min2dfa=OrderedMap()
        #dfa2min=OrderedMap()
        dfa2min=[]
        #self.partitionSetList=[]
        partition1=OrderedSet()
        partition2=OrderedSet()
        for stateId in dfa.states:
            if dfa.states[stateId].isAccepting():
                partition2.add(stateId)
            else:
                partition1.add(stateId)
        print(partition1)
        print(partition2)
        #minDFAStateId=0
        #min2dfa[minDFAStateId]=partition1
        dfa2min.append(partition1)
        dfa2min.append(partition2)
        #self.states[minDFAStateId]=State(minDFAStateId)
        minDFAStateIdSet=partition1
        #minDFAStateId2=1
        #min2dfa[minDFAStateId2]=partition2
        #dfa2min[OrderedFrozenSet(partition2)]=minDFAStateId2
        #self.states[minDFAStateId]=State(minDFAStateId2)        
            
        changes=True
        while changes:
            changes=False
            self.newPartition=OrderedSet()
            currentStateIdSet=minDFAStateIdSet
            change=finer(dfa2min.index(currentStateIdSet))
            dfa2min.append(self.newPartition)
            currentStateIdSet=dfa2min.index(self.newPartition)
        
        minDFAStateIdSet=partition2
        changes=True
        while changes:
            changes=False
            self.newPartition=OrderedSet()
            currentStateIdSet=minDFAStateIdSet
            change=finer(dfa2min.index(currentStateIdSet))
            dfa2min.append(self.newPartition)
            currentStateIdSet=dfa2min.index(self.newPartition)
        

                #minDFAStateId+=1
                #min2dfa[minDFAStateId]=self.newPartition
                #dfa2min.append(self.newPartition)

            
            #for stateId in min2dfa[currentStateIdSet]:
                #listOfTransitions=dfa.states[stateId].getTransitions()
                #for onClass, toStateId in listOfTransitions:
                    #for state in min2dfa[minDFAStateId]:
                        #if toStateId==state:
                            #self.states[currentStateId].\
                                #addTransition(onClass,minDFAStateId)
            print(dfa2min)
                            
            
         #when to create new minDFA States and it's transitions? (can I do like what I did?)
         #how to loop through the loop of 2, can do it entirely after the first loop?
            
        
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
    dfa=DFA({'+': {43}, 's': {83, 115}, 'EPSILON': set(), '/': {47}, 'digit': {48, 49, 50, 51, 52, 53, 54, 55, 56, 57}, '*': {42}, ')': {41}, 'r': {82, 114}, '^': {94}, '-': {45}, 'period': {46}, 'i': {73, 105}, '(': {40}},{0: State(0,None,[('(', 1), (')', 2), ('*', 3), ('+', 4), ('-', 5), ('/', 6), ('^', 7), ('digit', 8), ('i', 9), ('r', 10), ('s', 11)]), 1: State(1,1,[]), 2: State(2,1,[]), 3: State(3,1,[]), 4: State(4,1,[]), 5: State(5,1,[]), 6: State(6,1,[]), 7: State(7,1,[]), 8: State(8,1,[('digit', 12), ('period', 13)]), 9: State(9,1,[]), 10: State(10,1,[]), 11: State(11,1,[]), 12: State(12,1,[('digit', 12), ('period', 13)]), 13: State(13,None,[('digit', 14)]), 14: State(14,1,[('digit', 15)]), 15: State(15,1,[('digit', 15)])})
    
    mindfa=MinimumDFA()
    mindfa.buildFromDFA(dfa)
    mindfa.writeListing(sys.stdout)
main()
    