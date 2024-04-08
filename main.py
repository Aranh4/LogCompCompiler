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
            return self.children[0].evaluate(ST) / self.children[1].evaluate(ST)
        elif self.value == '>':
            return self.children[0].evaluate(ST) > self.children[1].evaluate(ST)
        elif self.value == '<':
            return self.children[0].evaluate(ST) < self.children[1].evaluate(ST)
        elif self.value == '==':
            return self.children[0].evaluate(ST) == self.children[1].evaluate(ST)
        elif self.value == 'or':
            return self.children[0].evaluate(ST) or self.children[1].evaluate(ST)
        elif self.value == 'and':
            return self.children[0].evaluate(ST) and self.children[1].evaluate(ST)
        

        
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,ST):
        if self.value == '+':
            return self.children[0].evaluate(ST)
        elif self.value == '-':
            return -self.children[0].evaluate(ST)
        elif self.value == 'not':
            return not self.children[0].evaluate(ST) 
        
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
        print(int(self.children[0].evaluate(ST)))
        

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

class whileNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        while self.children[0].evaluate(ST):
            self.children[1].evaluate(ST)
    
class ifNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST):
        if self.children[0].evaluate(ST):
            self.children[1].evaluate(ST)
        elif len(self.children) == 3:
            self.children[2].evaluate(ST)

class read(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self,ST):
        return int(input())
       
    



class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next
        self.prohibited =["print", "while", "do", "end", "if", "then", "else", "and", "or", "not", "read"]

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
                while self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position].isdigit() or self.source[self.position] == "_"):
                    self.position += 1
                if self.source[start:self.position] in self.prohibited:
                    self.next = Token(self.source[start:self.position].upper(), self.source[start:self.position])
                else:
                   self.next = Token("IDENT", self.source[start:self.position])
            elif self.source[self.position] == "\n":
                self.position += 1
                self.next = Token("NEWLINE", "\n")
            elif self.source[self.position] == "=":
                self.position += 1
                if self.source[self.position] == "=":
                    self.position += 1
                    self.next = Token("COMPAREEQUAL", "==")
                else:
                    self.next = Token("EQUAL", "=")
            elif self.source[self.position] == "<":
                self.position += 1
                self.next = Token("LESS", "<")
            elif self.source[self.position] == ">":
                self.position += 1
                self.next = Token("GREATER", ">")  
            elif self.source[self.position] == " ":
                self.position += 1
                self.selectNext()   
            else:
                #sys.stderr.write("token invalido, posicao: " + str(self.position) + "\n" + str(self.source[self.position]) + "\n")
                self.position += 1
                self.selectNext()
            
        
            
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    @staticmethod
    def parseBoolExpression(TOKENIZER):
        res = Parser.parseBoolTerm(TOKENIZER)
        while TOKENIZER.next.type == "OR":
            next = TOKENIZER.selectNext()
            res = BinOp("or", [res, Parser.parseBoolTerm(TOKENIZER)])
        return res
    
    @staticmethod
    def parseBoolTerm(TOKENIZER):
        res = Parser.ParseRelExpression(TOKENIZER)
        while TOKENIZER.next.type == "AND":
            next = TOKENIZER.selectNext()
            res = BinOp("and", [res, Parser.ParseRelExpression(TOKENIZER)])
        return res
    
    @staticmethod
    def ParseRelExpression(TOKENIZER):
        res = Parser.parseExpression(TOKENIZER)
        if TOKENIZER.next.type == "COMPAREEQUAL":
            next = TOKENIZER.selectNext()
            res = BinOp("==", [res, Parser.parseExpression(TOKENIZER)])
        elif TOKENIZER.next.type == "LESS":
            next = TOKENIZER.selectNext()
            res = BinOp("<", [res, Parser.parseExpression(TOKENIZER)])
        elif TOKENIZER.next.type == "GREATER":
            next = TOKENIZER.selectNext()
            res = BinOp(">", [res, Parser.parseExpression(TOKENIZER)])
        return res

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
                res.children.append(Parser.parseBoolExpression(TOKENIZER))
            
            
            if TOKENIZER.next.type != "NEWLINE" and TOKENIZER.next.type != "EOF":
                sys.stderr.write("token invalido, esperado: NEWLINE1, recebido: " + TOKENIZER.next.type + "\n")
          

        elif TOKENIZER.next.type == "PRINT":
            next = TOKENIZER.selectNext()
            if TOKENIZER.next.type == "LPAREN":
                next = TOKENIZER.selectNext()
                res = Print("print", [Parser.parseBoolExpression(TOKENIZER)])
                if TOKENIZER.next.type != "RPAREN":
                    sys.stderr.write("token invalido, esperado: RParen, recebido: " + TOKENIZER.next.type + "\n")
                else:
                    next = TOKENIZER.selectNext()
            else:
                sys.stderr.write("token invalido, esperado: LParen, recebido: " + TOKENIZER.next.type + "\n")
            #next = TOKENIZER.selectNext()
            if TOKENIZER.next.type != "NEWLINE" and TOKENIZER.next.type != "EOF":
                sys.stderr.write("token invalido, esperado: NEWLINE2, recebido: " + TOKENIZER.next.type + "\n")
        elif TOKENIZER.next.type == "NEWLINE" or TOKENIZER.next.type == "EOF":
            res = NoOp()
            next = TOKENIZER.selectNext()

        elif TOKENIZER.next.type == "IF":
            next = TOKENIZER.selectNext()
            condition = Parser.parseBoolExpression(TOKENIZER)
            bloco = Block("block", [])
            
            if TOKENIZER.next.type != "THEN":
                sys.stderr.write("token invalido, esperado: THEN, recebido: " + TOKENIZER.next.type + "\n")
                sys.stderr.write("posicao:"+ str(TOKENIZER.position) + "\n")
            else:
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type != "NEWLINE":
                    sys.stderr.write("token invalido, esperado: NEWLINE, recebido: " + TOKENIZER.next.type + "\n")
                else:
                    next = TOKENIZER.selectNext()
                    while TOKENIZER.next.type != "END" and TOKENIZER.next.type != "ELSE":
                    
                        bloco.children.append(Parser.parseStatement(TOKENIZER))
                        next = TOKENIZER.selectNext()
                    if TOKENIZER.next.type == "ELSE": 
                        next = TOKENIZER.selectNext()
                        if TOKENIZER.next.type != "NEWLINE":
                            sys.stderr.write("token invalido, esperado: NEWLINE, recebido: " + TOKENIZER.next.type + "\n")
                        else:
                            next = TOKENIZER.selectNext()
                            blocoelse = Block("block", [])
                            while TOKENIZER.next.type != "END":
                                blocoelse.children.append(Parser.parseStatement(TOKENIZER))
                                next = TOKENIZER.selectNext()
                            res = ifNode("if", [condition, bloco, blocoelse])
                            if TOKENIZER.next.type != "END":
                                sys.stderr.write("token invalido, esperado: END, recebido: " + TOKENIZER.next.type + "\n")
                            else: 
                                next = TOKENIZER.selectNext()
                    elif TOKENIZER.next.type == "END":
                        next = TOKENIZER.selectNext()
                        res = ifNode("if", [condition, bloco])
                    else:
                        sys.stderr.write("token invalido, esperado: END, ELSE, recebido: " + TOKENIZER.next.type + "\n")
        
            if TOKENIZER.next.type != "NEWLINE" and TOKENIZER.next.type != "EOF":
                sys.stderr.write("token invalido, esperado: NEWLINE3, recebido: " + TOKENIZER.next.type + "\n")

        elif TOKENIZER.next.type == "WHILE":
            next = TOKENIZER.selectNext()
            condition = Parser.parseBoolExpression(TOKENIZER)
            if TOKENIZER.next.type != "DO":
                sys.stderr.write("token invalido, esperado: DO, recebido: " + TOKENIZER.next.type + "\n")
            else:
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type != "NEWLINE":
                    sys.stderr.write("token invalido, esperado: NEWLINE, recebido: " + TOKENIZER.next.type + "\n")
                else:
                    next = TOKENIZER.selectNext()
                    
                    bloco = Block("block", [])
                    while TOKENIZER.next.type != "END":
                        
                        bloco.children.append(Parser.parseStatement(TOKENIZER))
                        next = TOKENIZER.selectNext()
                    res = whileNode("while", [condition, bloco])
                    next = TOKENIZER.selectNext()
            if TOKENIZER.next.type != "NEWLINE" and TOKENIZER.next.type != "EOF":
                sys.stderr.write("token invalido, esperado: NEWLINE4, recebido: " + TOKENIZER.next.type + "\n")
        

        else:
            sys.stderr.write("token invalido, esperado: IDENT, PRINT, NEWLINE, IF, WHILE, recebido: " + TOKENIZER.next.type + "\n")

        return res

    @staticmethod
    def parseFactor(TOKENIZER):
        if TOKENIZER.next.type == "INT":
            res = IntVal(TOKENIZER.next.value)
            next = TOKENIZER.selectNext()
        elif TOKENIZER.next.type == "LPAREN":
            next = TOKENIZER.selectNext()
            res = Parser.parseBoolExpression(TOKENIZER)
            if TOKENIZER.next.type != "RPAREN":
                sys.stderr.write("Syntax error: Unmatched parentheses\n")
            else:
                next = TOKENIZER.selectNext()
        elif TOKENIZER.next.type == "PLUS":
            next = TOKENIZER.selectNext()
            res = UnOp("+", [Parser.parseFactor(TOKENIZER)])
        elif TOKENIZER.next.type == "MINUS":
            next = TOKENIZER.selectNext()
            res = UnOp("-", [Parser.parseFactor(TOKENIZER)])
        elif TOKENIZER.next.type == "NOT":
            next = TOKENIZER.selectNext()
            res = UnOp("not", [Parser.parseFactor(TOKENIZER)])
        elif TOKENIZER.next.type == "READ":
            next = TOKENIZER.selectNext()
            if TOKENIZER.next.type == "LPAREN":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "RPAREN":
                    res = read("read")
                    next = TOKENIZER.selectNext()
                else:
                    sys.stderr.write("Syntax error: Unmatched parentheses\n")
            else:
                sys.stderr.write("Syntax error: Unplaced parentheses\n")
               
        elif TOKENIZER.next.type == "IDENT":
            res = Identifier(TOKENIZER.next.value)
            next = TOKENIZER.selectNext()
        else:
            sys.stderr.write("Syntax error: Invalid token at factor\n")
            res = NoOp() 
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


    