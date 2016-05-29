import streamreader
'''Name: Linh Nguyen
Class: Cs260
Professor: Kent Lee '''
import io

class PrefixToPostfix:
    def __init__(self,token, item1, item2):
        self.token=token
        self.item1=item1
        self.item2=item2
    def eval(self):
        return str(self.item1.eval())+" "+str(self.item2.eval())+" "+self.token.eval()
    
class Item:
    def __init__(self,val):
        self.val=val
    def eval(self):
        return self.val
    
def E(reader):
    token=reader.getToken()
    if token=="*" or token=="-" or token=="+" or token=="/":
        return PrefixToPostfix(Item(token), E(reader), E(reader))
    if type(token)==int:
        return Item(token)
    raise Exception("Invalid expression")

def main():
    try:
        line=input("Please enter a prefix expression: ").strip()
        while (line!=""):
            reader=streamreader.StreamReader(io.StringIO(line))
            astr=E(reader)
            s= astr.eval()
            reader.getToken()
            if reader.eof():
                print("The postfix expression of your expression is: ",s)
                line=input("Please enter a prefix expression: ")
            else:
                print("Invalid expression")
                break
    except Exception as ex:
        print(ex)
main()