import state
import io
import streamreader

# This is exercise 12 from page 55 of Linz Text, 5th Ed.

class NFA:
    def __init__(self, states, startStateId, classes):
        self.states = states
        self.startStateId = startStateId
        self.classes = classes

        for stateId in self.states:
            self.states[stateId].setClasses(classes)

    def accepts(self, strm):
        # The accepts method uses a recursive acceptsSuffix
        # which starts in the given state (not necessarily the
        # start state) and recursively uses search with backtracking
        # to try to find a final state with all of the input consumed.
        # If it is successful on this path then it returns True and if
        # not it returns False to continue to backtrack and look for
        # another path to a final state.

        def acceptsSuffix(stateId):
            theState = self.states[stateId]

            # Check that we are not at end of file and in an accepting state.
            c = strm.readChar()
            if strm.eof() and theState.isAccepting():
                return True

            strm.unreadChar(c)

            for onClass, toStateId in theState.getTransitions():

                if onClass == "epsilon":
                    if acceptsSuffix(toStateId):
                        return True

                else: # onClass is not an epsilon transition
                    c = strm.readChar()

                    if c in self.classes[onClass] and acceptsSuffix(toStateId):
                        return True

                    strm.unreadChar(c)

            return False

        # Beginning of accepts function body - We call acceptsSuffix
        # initially starting from the start state.
        return acceptsSuffix(self.startStateId)
