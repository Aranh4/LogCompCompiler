from abc import abstractmethod
import sys

class SymbolTable:
    def __init__(self):
        self.symbols = {}
    
    def add(self, symbol, value):
        self.symbols[symbol] = value
    
    def get(self, symbol):
        return self.symbols[symbol]

class PrePro:
    @staticmethod
    def filter(code):
        res = code
        for i in range(len(code)):
            if i < len(code) and code[i] =='-':     # rest of the code
                if code[i+1] == '-':
                    for j in range(i, len(code)):
                        if code[j] == '\n':
                            code = code[:i] + code[j:]
                            break
        return code

class Node():
    def __init__(self, value, children = None):
        self.value = value
        self.children = children if children is not None else []



    @abstractmethod
    def evaluate(self):
        pass


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)


    def evaluate(self,ST):
        if self.value == '+':
            return self.children[0].evaluate(ST) + self.children[1].evaluate(ST)
        elif self.value == '-':
            return self.children[0].evaluate(ST) - self.children[1].evaluate(ST)
        elif self.value == '*':
            return self.children[0].evaluate(ST) * self.children[1].evaluate(ST)
        elif self.value == '/':
            return self.children[0].evaluate(ST) / self.children[1].evaluate()
        
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,ST):
        if self.value == '+':
            return self.children[0].evaluate(ST)
        elif self.value == '-':
            return -self.children[0].evaluate(ST)
        
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)
    def evaluate(self,ST):
        return int(self.value)
    
class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self,ST):
        pass

class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,ST):
        print(self.children[0].evaluate(ST))
        

class Assign(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,ST):
        ST.add(self.children[0].value, self.children[1].evaluate(ST))

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self,ST):
        return ST.get(self.value)

class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        for child in self.children:
            child.evaluate(ST)
    



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
            elif self.source[self.position].isalpha():
                start = self.position
                while self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_":
                    self.position += 1
                if self.source[start:self.position] == "print":
                    self.next = Token("PRINT", "print")
                else:
                   self.next = Token("IDENT", self.source[start:self.position])
            elif self.source[self.position] == "\n":
                self.position += 1
                self.next = Token("NEWLINE", "\n")
            elif self.source[self.position] == "=":
                self.position += 1
                self.next = Token("EQUAL", "=")	
            else:
                sys.stderr.write("token invalido, posicao: " + str(self.position) + "\n")
                self.position += 1
                self.selectNext()
            
        
            
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    @staticmethod
    def parseBlock(TOKENIZER):
        res = Block("block", [])
        next = TOKENIZER.selectNext()
        while TOKENIZER.next.type != "EOF":
            parsed = Parser.parseStatement(TOKENIZER)
            res.children.append(parsed)
          
        return res


    @staticmethod
    def parseStatement(TOKENIZER):
        if TOKENIZER.next.type == "IDENT":
            res = Assign("=", [Identifier(TOKENIZER.next.value)])
            next = TOKENIZER.selectNext()
            if TOKENIZER.next.type != "EQUAL":
                sys.stderr.write("token invalido, esperado: EQUAL, recebido: " + TOKENIZER.next.type + "\n")
            else:
                next = TOKENIZER.selectNext()
                res.children.append(Parser.parseExpression(TOKENIZER))
            
            
            if TOKENIZER.next.type != "NEWLINE" and TOKENIZER.next.type != "EOF":
                sys.stderr.write("token invalido, esperado: NEWLINE1, recebido: " + TOKENIZER.next.type + "\n")
        elif TOKENIZER.next.type == "PRINT":
            next = TOKENIZER.selectNext()
            if TOKENIZER.next.type == "LPAREN":
                next = TOKENIZER.selectNext()
                res = Print("print", [Parser.parseExpression(TOKENIZER)])
                if TOKENIZER.next.type != "RPAREN":
                    sys.stderr.write("token invalido, esperado: RParen, recebido: " + TOKENIZER.next.type + "\n")
                else:
                    next = TOKENIZER.selectNext()
            else:
                sys.stderr.write("token invalido, esperado: LParen, recebido: " + TOKENIZER.next.type + "\n")
            #next = TOKENIZER.selectNext()
            if TOKENIZER.next.type != "NEWLINE" and TOKENIZER.next.type != "EOF":
                sys.stderr.write("token invalido, esperado: NEWLINE2, recebido: " + TOKENIZER.next.type + "\n")
        elif TOKENIZER.next.type == "NEWLINE":
            res = NoOp()
            next = TOKENIZER.selectNext()

        else:
            sys.stderr.write("token invalido, esperado: IDENT, PRINT, NEWLINE, recebido: " + TOKENIZER.next.type + "\n")

        return res

    @staticmethod
    def parseFactor(TOKENIZER):
        
        if TOKENIZER.next.type == "INT":
            res = IntVal(TOKENIZER.next.value)
            next = TOKENIZER.selectNext()
        elif TOKENIZER.next.type == "LPAREN":
            
            res = Parser.parseExpression(TOKENIZER)
            if TOKENIZER.next.type != "RPAREN":

                sys.stderr.write("token invalido, esperado: RParen, recebido: " + TOKENIZER.next.type + "\n")
            else:
                next = TOKENIZER.selectNext()
        elif TOKENIZER.next.type == "PLUS":
            next = TOKENIZER.selectNext()
            res = UnOp("+", [Parser.parseFactor(TOKENIZER)])
        elif TOKENIZER.next.type == "MINUS":
            next = TOKENIZER.selectNext()
            res = UnOp("-", [Parser.parseFactor(TOKENIZER)])
        elif TOKENIZER.next.type == "IDENT":
            res = Identifier(TOKENIZER.next.value)
            next = TOKENIZER.selectNext()
        else:
            sys.stderr.write("1token invalido, esperado: INT, LParen, PLUS, MINUS, IDENT, recebido: " + TOKENIZER.next.type + "\n")
            res =0
        return res

    @staticmethod
    def parseTerm (TOKENIZER):
        

        res = Parser.parseFactor(TOKENIZER)
       
        
        while TOKENIZER.next.type == "MULT" or TOKENIZER.next.type == "DIV":
            if TOKENIZER.next.type == "MULT":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS":
                    res = BinOp("*", [res, Parser.parseFactor(TOKENIZER)])
                    #res *= Parser.parseFactor(TOKENIZER)
                
                else:
                    sys.stderr.write("token invalido1")
            elif TOKENIZER.next.type == "DIV":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS":
                    #res /= Parser.parseFactor(TOKENIZER)
                    res = BinOp("/", [res, Parser.parseFactor(TOKENIZER)])
                   
                else:
                    sys.stderr.write("token invalido2")
        
  
        return res

    @staticmethod
    def parseExpression(TOKENIZER):
       
        res = Parser.parseTerm(TOKENIZER)
        while TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS":
        
            if TOKENIZER.next.type == "PLUS":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS" or TOKENIZER.next.type == "IDENT":
                    res = BinOp("+", [res, Parser.parseTerm(TOKENIZER)])
                    
                else:
                    sys.stderr.write("2token invalido esperado: INT, LPAREN, PLUS, MINUS, recebido: " + TOKENIZER.next.type + "\n")
            elif TOKENIZER.next.type == "MINUS":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS" or TOKENIZER.next.type == "IDENT":
                    res = BinOp("-", [res, Parser.parseTerm(TOKENIZER)])
                 
                else:
                    sys.stderr.write("3token invalido esperado: INT, LPAREN, PLUS, MINUS, recebido: " + TOKENIZER.next.type + "\n")
        return res

    def run(code):
        code = PrePro.filter(code)
        tokenizer = Tokenizer(code, 0, None)
        parser = Parser(tokenizer)
        result = parser.parseBlock(TOKENIZER=tokenizer)
        if parser.tokenizer.next.type != "EOF":
            
            sys.stderr.write("token invalido, esperado: EOF, recebido: " + parser.tokenizer.next.type + "\n")
        else:
            return result

            
def main():

    filename = sys.argv[1]

    if filename.endswith('.lua'):
        with open(filename, 'r') as file:
            code = file.read()
    
    parser = Parser.run(code)
    ST = SymbolTable()
    resultado = parser.evaluate(ST)
    

    

if __name__ == "__main__":
    main()


    