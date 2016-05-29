from lr0state import *
import stack
import streamreader
import io
import sys

class Parser:
    def __init__(self,states,tnts):
        self.states = states
        self.tnts = tnts
        for stateId in states:
            theState = states[stateId]
            theState.tnts = tnts
            for item in theState.items:
                item.tnts = tnts
            #print(theState)
            
    def reduce(self, item, prodStack):
        lhsId = item.production.lhsId
        # We found an item to reduce by.
        prodNames = {} # this is a map from return value names to locations with rhs
        tntCount = {}
        rhsVals = {} # this is a map from index location of rhs to value from the stack.
        
        # this loop builds a map from names of rhs terminals or nonterminals to
        # their index value for the rhs
        for i in range(len(item.production.rhs)):
            tntId = item.production.rhs[i]
            tnt = self.tnts[tntId]
            if not tnt in tntCount:
                tntCount[tnt] = 1
                prodNames[tnt] = i
                prodNames[tnt+"1"] = i
            else:
                numVal = tntCount[tnt]+1
                tntCount[tnt] = numVal
                prodNames[tnt+str(numVal)]=i
        
        # this loop builds a map from index value of rhs location to 
        # the actual value popped from the pda stack.
        for i in range(len(item.production.rhs)-1,-1,-1):
            stateId, val = prodStack.pop()
            rhsVals[i] = val
            
        returnValue = ""
        rvStrm  = streamreader.StreamReader(io.StringIO(item.production.returnValue))
        
        token = rvStrm.getToken()
        
        while not rvStrm.eof():
            if token in prodNames:
                returnValue += rhsVals[prodNames[token]]
            else:
                returnValue += token
                
            token = rvStrm.getToken()

        return returnValue

    # This algorithm comes from page 218, Algorithm 4.7 from Aho,
    # Sethi, and Ullman. The modification from this algorithm has 
    # the stack a stack of tuple of (stateId, val) where val is 
    # the return value for a terminal or nonterminal.
    
    def parse(self, theScanner):

        # The parse method starts by creating the PDA stack. The stack is a stack of 
        # tuples of state identifier and return value. The stack is initialized with the 
        # start state identifier (i.e. 0) and the return value of None. Then the PDA is 
        # run as described in class either shifting or reducing as it continues until
        # the accepting state is encountered when it returns the return value it got 
        # by the last reduction it performed. 

        # The PDA operates by looking for a shift operation first by getting the next token
        # and examining the tokenId to see if there is a transition on that tokenId from the
        # current (top of the stack) state using the hasTransition and onClassGoTo methods.
        # If no shift operation is possible, the parser looks for an item we could do a reduction 
        # by and then checks to see if the tokenId is in the lookahead set of the item. If
        # it finds a match then it calls reduce above. The return value from reduce is a string
        # that must be evaluated by calling self.eval(return value from reduce).

        # val = self.eval(returnValueFromReduce)

        # this method ends when the accepting state is found and at that time it returns 
        # the val that was returned by evaluating the return value of the last reduction.

        # if the state is not accepting, then we do a transition on the top of stack state on
        # the lhs identifier and we push on to the PDA stack the tuple of the 
        # (nextStateId,repr(val)) where nextStateId is the next state that we transition to and 
        # repr(val) builds a string of the result of calling self.eval(returnValueFromReduce). 
        #pass
        pdaStack=stack.Stack()
        pdaStack.push((0,None))
        (lex,tokenId)=theScanner.getToken()
        (currentStateId,val)=pdaStack.peek()
        while not self.states[currentStateId].isAccepting():
            (currentStateId,val)=pdaStack.peek()
            if self.states[currentStateId].hasTransition(tokenId):
                currentStateId=self.states[currentStateId].onClassGoTo(tokenId)
                pdaStack.push((currentStateId,lex))
            else:
                while not self.states[currentStateId].hasTransition(tokenId):                   
                    for item in self.states[currentStateId].items:
                        if tokenId in item.la:
                            matchingItem=item.production.lhsId
                            returnValue=self.reduce(item,pdaStack)
                            val=self.eval(returnValue)
                            (currentStateId,token)=pdaStack.peek()
                            currentStateId=self.states[currentStateId].onClassGoTo(matchingItem)
                            pdaStack.push((currentStateId,repr(val)))
                  
                currentStateId=self.states[currentStateId].onClassGoTo(tokenId)
                pdaStack.push((currentStateId,lex))                
            (lex,tokenId)=theScanner.getToken()
        
        if self.states[currentStateId].isAccepting():
            print("complete")
        else:
            print("invalid")
       
 
                
            
                                      
              
                        
        
            
                    
                    
                        
                            
                            
                        
                             
                                
                                
                            
                        
                
                
            
            
            
