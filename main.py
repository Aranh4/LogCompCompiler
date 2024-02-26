import sys

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next

    def selectNext(self):
        if self.position >= len(self.source):
            self.next = Token("EOF", "")
        else:
            if self.source[self.position] == "+":
                self.position += 1
                self.next = Token("PLUS", "+")
            elif self.source[self.position] == "-":
                self.position += 1
                self.next = Token("MINUS", "-")
            elif self.source[self.position].isdigit():
                start = self.position
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    self.position += 1
                self.next = Token("INT", self.source[start:self.position])
            elif self.source[self.position] == "*":
                self.position += 1
                self.next = Token("MULT", "*")
            elif self.source[self.position] == "/":
                self.position += 1
                self.next = Token("DIV", "/")
            elif self.source[self.position] == " ":
                self.position += 1
                self.selectNext()
        
            
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer


    def parseTerm (self):

        res = 0
       
        if self.tokenizer.next.type == "INT" or self.tokenizer.next.type == "EOF":
            res = int(self.tokenizer.next.value)
            next = self.tokenizer.selectNext()
            while self.tokenizer.next.type == "MULT" or self.tokenizer.next.type == "DIV":
                if self.tokenizer.next.type == "MULT":
                    next = self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "INT":
                        res *= int(self.tokenizer.next.value)
                        next = self.tokenizer.selectNext()
                    else:
                        sys.stderr.write("token invalido1")
                elif self.tokenizer.next.type == "DIV":
                    next = self.tokenizer.selectNext()
                    if self.tokenizer.next.type == "INT":
                        res /= int(self.tokenizer.next.value)
                        next = self.tokenizer.selectNext()
                    else:
                        sys.stderr.write("token invalido2")
          
        else:
            sys.stderr.write("token invalido3") 
       
        return int(res)

    def parseExpression(self):
        next = self.tokenizer.selectNext()
        res = self.parseTerm()
        while self.tokenizer.next.type == "PLUS" or self.tokenizer.next.type == "MINUS":
        
            if self.tokenizer.next.type == "PLUS":
                next = self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    res += self.parseTerm()
                    
                else:
                    sys.stderr.write("token invalido4")
            elif self.tokenizer.next.type == "MINUS":
                next = self.tokenizer.selectNext()
                if self.tokenizer.next.type == "INT":
                    res -= self.parseTerm()
                 
                else:
                    sys.stderr.write("token invalido5")
        if self.tokenizer.next.type != "EOF":
            sys.stderr.write("token invalido6")
           


        return res

    def run(code):
        tokenizer = Tokenizer(code, 0, None)
        parser = Parser(tokenizer)
        return parser.parseExpression()

            
def main():
    code = sys.argv[1]
    parser = Parser.run(code)
    sys.stdout.write(str(parser))

    

if __name__ == "__main__":
    main()


    