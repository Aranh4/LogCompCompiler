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
            elif self.source[self.position] == "(":
                self.position += 1
                self.next = Token("LPAREN", "(")
            elif self.source[self.position] == ")":
                self.position += 1
                self.next = Token("RPAREN", ")")
            elif self.source[self.position] == " ":
                self.position += 1
                self.selectNext()
        
            
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    @staticmethod
    def parseFactor(TOKENIZER):
        res = 0
        if TOKENIZER.next.type == "INT":
            res = int(TOKENIZER.next.value)
            next = TOKENIZER.selectNext()
        elif TOKENIZER.next.type == "LPAREN":
            
            res = Parser.parseExpression(TOKENIZER=TOKENIZER)
            if TOKENIZER.next.type != "RPAREN":

                sys.stderr.write("token invalido, esperado: RParen, recebido: " + TOKENIZER.next.type + "\n")
            else:
                next = TOKENIZER.selectNext()
  
        elif TOKENIZER.next.type == "PLUS":
            next = TOKENIZER.selectNext()
            res = Parser.parseFactor(TOKENIZER=TOKENIZER)
        elif TOKENIZER.next.type == "MINUS":
            next = TOKENIZER.selectNext()
            res = -Parser.parseFactor(TOKENIZER=TOKENIZER)
        else:
            sys.stderr.write("token invalido8")
        return res

    @staticmethod
    def parseTerm (TOKENIZER):
        

        res = Parser.parseFactor(TOKENIZER=TOKENIZER)
       
        
        while TOKENIZER.next.type == "MULT" or TOKENIZER.next.type == "DIV":
            if TOKENIZER.next.type == "MULT":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS":
                    res *= Parser.parseFactor(TOKENIZER=TOKENIZER)
                
                else:
                    sys.stderr.write("token invalido1")
            elif TOKENIZER.next.type == "DIV":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS":
                    res /= Parser.parseFactor(TOKENIZER=TOKENIZER)
                   
                else:
                    sys.stderr.write("token invalido2")
        
  
        return int(res)

    @staticmethod
    def parseExpression(TOKENIZER):
        next = TOKENIZER.selectNext()
        res = Parser.parseTerm(TOKENIZER=TOKENIZER)
        while TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS":
        
            if TOKENIZER.next.type == "PLUS":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS":
                    res += Parser.parseTerm(TOKENIZER=TOKENIZER)
                    
                else:
                    sys.stderr.write("token invalido4")
            elif TOKENIZER.next.type == "MINUS":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS":
                    res -= Parser.parseTerm(TOKENIZER=TOKENIZER)
                 
                else:
                    sys.stderr.write("token invalido5")
       
           


        return res

    def run(code):
        tokenizer = Tokenizer(code, 0, None)
        parser = Parser(tokenizer)
        result = parser.parseExpression(TOKENIZER=tokenizer)
        if parser.tokenizer.next.type != "EOF":
            
            sys.stderr.write("token invalido, esperado: EOF, recebido: " + parser.tokenizer.next.type + "\n")
        else:
            return result

            
def main():
    code = sys.argv[1]
    parser = Parser.run(code)
    sys.stdout.write(str(parser))

    

if __name__ == "__main__":
    main()


    