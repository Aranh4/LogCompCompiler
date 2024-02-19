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
            return Token("EOF", "")
        else:
            if self.source[self.position] == "+":
                self.position += 1
                return Token("PLUS", "+")
            if self.source[self.position] == "-":
                self.position += 1
                return Token("MINUS", "-")
            if self.source[self.position].isdigit():
                start = self.position
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    self.position += 1
                return Token("INT", self.source[start:self.position])
            elif self.source[self.position] == " ":
                self.position += 1
                return self.selectNext()
        
            
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        

    def parseExpression(self):
        token = self.tokenizer.selectNext()
        res = 0
        if token.type == "INT":
            res = int(token.value)
            token = self.tokenizer.selectNext()
            while token.type == "PLUS" or token.type == "MINUS":
                if token.type == "PLUS":
                    token = self.tokenizer.selectNext()
                    if token.type == "INT":
                        res += int(token.value)
                        token = self.tokenizer.selectNext()
                    else:
                        sys.stderr.write("token invalido")
                elif token.type == "MINUS":
                    token = self.tokenizer.selectNext()
                    if token.type == "INT":
                        res -= int(token.value)
                        token = self.tokenizer.selectNext()
                    else:
                        sys.stderr.write("token invalido")
            if token.type != "EOF":
                sys.stderr.write("token invalido")
           
        else:
            sys.stderr.write("token invalido") 

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


    