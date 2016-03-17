#Name: Linh Nguyen
#Class: CS260
#Professor: Kent Lee
#DFA Minimization 
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
        
        def transToMin(fromStateId,onClass):
            fromState=dfa.states[fromStateId]
            toStateId=fromState.onClassGoTo(onClass)
            if toStateId==-1:
                return -1
            return dfa2min[toStateId] 
        
        def finer(partitionId):
            stateSet=partitionsList[partitionId]
            primaryState=sorted(stateSet)[0]
            transitionsToPartitions[primaryState]={}
            for onClass, toStateId in dfa.states[primaryState].getTransitions():
                toPartition=transToMin(primaryState,onClass)
                transitionsToPartitions[primaryState][onClass]=toPartition
                
            for stateId in stateSet:
                transitionsToPartitions[stateId]={}
                for onClass, toStateId in dfa.states[stateId].getTransitions():
                    toPartition=transToMin(stateId,onClass)
                    transitionsToPartitions[stateId][onClass]=toPartition  
                if set(transitionsToPartitions[primaryState])!=set(transitionsToPartitions[stateId]):
                    newPartition.add(stateId)
                    dfa2min[stateId]=len(partitionsList)
            partitionsList[partitionId]=OrderedSet(partitionsList[partitionId]-newPartition)
            return len(newPartition)!=0 
        
        self.states=OrderedMap()                  
        partitionsList=[]
        dfa2min={}  
        partition1=OrderedSet()
        partition2=OrderedSet()
        for stateId in dfa.states:
            if dfa.states[stateId].isAccepting():
                partition2.add(stateId)
                dfa2min[stateId]=1
            else:
                partition1.add(stateId)
                dfa2min[stateId]=0
        partitionsList.append(partition1)
        partitionsList.append(partition2)

        transitionsToPartitions={}
        
        change=True
        while change:
            change=False
            for partitionId in range(len(partitionsList)):
                newPartition=OrderedSet()
                change=finer(partitionId)
                if change:
                    partitionsList.append(newPartition)
                    
        for i in range(len(partitionsList)):
            self.states[i]=State(i)
            for stateId in partitionsList[i]:
                if dfa.states[stateId].isAccepting():
                    self.states[i].setAccepting(1)
        
        for i in range(len(partitionsList)):
            stateId=list(partitionsList[i])[0]
            for onClass in transitionsToPartitions[stateId]:
                toPartition=transitionsToPartitions[stateId][onClass]
                self.states[i].addTransition(onClass,toPartition)       
     
        
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
    