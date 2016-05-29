#Name: Linh Nguyen
#Class: CS260
#Professor: Kent Lee
#Finite State Machine 2-2d

import state
import io
import streamreader

class FiniteStateMachine:
    def __init__(self, states, startStateId, classes):
        self.states = states
        self.startStateId = startStateId
        self.classes = classes

        for stateId in self.states:
            self.states[stateId].setClasses(classes)

    def accepts(self, strm):
        ch=strm.readChar()
        stateId=self.startStateId
        while not strm.eof():
            stateId=self.states[stateId].onGoTo(ch)
            ch=strm.readChar()
        return self.states[stateId].isAccepting()
def main():

    q0 = state.State(0)
    q1 = state.State(1)
    q2 = state.State(2)
    q3 = state.State(3,2)
    q4 = state.State(4)
    q5 = state.State(5)
    q6 = state.State(6)
    q7 = state.State(7)

    classes = {"a":frozenset("a"), "b":frozenset("b")}
  
    
    q0.addTransition("a", 1)
    q0.addTransition("b", 4)
    q1.addTransition("a", 1)
    q1.addTransition("b",2)
    q2.addTransition("a",2)
    q2.addTransition("b",3)
    q3.addTransition("a",3)
    q3.addTransition("b",6)
    q4.addTransition("a",7)
    q4.addTransition("b",5)
    q5.addTransition("a",3)
    q5.addTransition("b",6)
    q6.addTransition("a",6)
    q6.addTransition("b",6)
    q7.addTransition('a',7)
    q7.addTransition('b',3)

    dfa = FiniteStateMachine({0:q0, 1:q1, 2:q2, 3:q3, 4:q4, 5:q5, 6:q6, 7:q7}, 0, classes)

    # You must complete the main function here but you can
    # create a stream over a string s by writing
    # strm = streamreader.StreamReader(io.StringIO(s))
    s=input("Please enter a string of a's and b's: ")
    while s!='':
        strm=streamreader.StreamReader(io.StringIO(s))
        if dfa.accepts(strm):
            print('That string is accepted by this finite state machine.')
        else:
            print('That string is not accepted.')
        s=input("Please enter a string of a's and b's: ")
    print('Program completed.')
        
if __name__=="__main__":
    main()