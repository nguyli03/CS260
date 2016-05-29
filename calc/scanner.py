import streamreader
import state
from orderedcollections import *
             
class Scanner:
    def __init__(self, instream = None, startStateId = None, states={}, classes={}, keywords = {}, identifierTokenId = -1, eatComments = False, commentTokenId = -1):
        # The use of dict below creates a copy of the default parameter because
        # only one copy of default parameters is created and if multiple scanner 
        # objects were created this would be a problem... for Python...
        self.states = dict(states)
        self.classes = dict(classes)
        self.startStateId = startStateId
        self.reader = streamreader.StreamReader(instream)
        self.keywords = dict(keywords)
        self.identiferTokenId = identifierTokenId
        self.eatComments = eatComments
        self.commentTokenId = commentTokenId
        for stateId in states:
            states[stateId].setClasses(classes)
  
    def getToken(self):  

        # Here the getToken method must skip whitespace and then run the finite state machine starting with self.startStateId.
        # The finite state machine is an infinite loop of getting characters from the reader and transitioning between states.
        # The getToken method returns a tuple of (tokenId, lex) where tokenId is the token Identifier from the state or from the 
        # map of keywords if the lexeme is in the keyword map.
        # If a transition is not found, then an exception can be raised like this.
        # raise Exception("Bad Token '"+lex+"' found at line " + str(self.reader.getLineNumber()) + " and column " + str(self.reader.getColNumber()) + ".")    
        #pass 
        currentStateId=self.startStateId
        lex=""
        self.reader.skipWhiteSpace()
        c=self.reader.readChar()
        onClass=ord(c)
        lex+=c
        while self.states[currentStateId].onGoTo(onClass)!=-1:
            currentStateId=self.states[currentStateId].onGoTo(onClass)
            c=self.reader.readChar()
            onClass=ord(c)
            lex+=c
            
        self.reader.unreadChar(c)
        lex=lex[0:len(lex)-1];
        accept=self.states[currentStateId].getAcceptsTokenId()
        if accept==None:
            raise Exception("Bad Token"+lex+" found at line "+ str(self.reader.getLineNumber())+ " and column "+str(self.reader.getColNumber())+".")  
        return (lex, accept)
        




