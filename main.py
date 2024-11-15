from abc import abstractmethod
import sys

class Writer:

    def __init__(self, path):
        self.path = path

   
    def w(self,line):
        
        with open(self.path, "a") as file:
            file.write(line + "\n")

            file.close()

    
    def clear(self):
        
        with open(self.path, "w") as file:
            file.write("")
            file.close()
    


        
        
        

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.shift = 0
    
    def set(self, symbol, value, type):
        if symbol in self.symbols.keys():
            self.symbols[symbol] = [value, type, self.symbols[symbol][2]]
        else:
            sys.stderr.write("Variavel nao declarada\n")

    def create(self, symbol):   
        self.shift += 4
        if symbol not in self.symbols.keys():     
            self.symbols[symbol] = [0, "int", self.shift]
        else:
            sys.stderr.write("Variavel ja declarada\n")
    
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
    instances = []

    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []
        Node.instances.append(self)
        self.id = len(Node.instances)





    @abstractmethod
    def evaluate(self, ST, writer):
        pass


class BinOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)


    def evaluate(self,ST,writer):

        filho0 = self.children[0].evaluate(ST,writer)
        writer.w("PUSH EAX")

        filho1 = self.children[1].evaluate(ST,writer)
        writer.w("MOV EBX, EAX")
        writer.w("POP EAX")

        
        valor0 = filho0[0]
        tipo0 = filho0[1]

        valor1 = filho1[0]
        tipo1 = filho1[1]

        

        if self.value == '+':
            writer.w("ADD EAX, EBX")
            if tipo0 == "string" or tipo1 == "string":
                sys.stderr.write("Operacao (+) invalida - Erro de Semântica\n Esperado: int\n Recebido: string\n")
                return 0
            return [int(valor0) + int(valor1), "int"]
        elif self.value == '-':
            writer.w("SUB EAX, EBX")
            if tipo0 == "string" or tipo1 == "string":
                sys.stderr.write("Operacao (-) invalida - Erro de Semântica\n Esperado: int\n Recebido: string\n")
                return 0
            return [int(valor0) - int(valor1), "int"]
        elif self.value == '*':
            writer.w("IMUL EAX, EBX")
            if tipo0 == "string" or tipo1 == "string":
                sys.stderr.write("Operacao (*) invalida - Erro de Semântica\n Esperado: int\n Recebido: string\n")
                return 0
            return [int(valor0) * int(valor1), "int"]
        elif self.value == '/':
            writer.w("IDIV EAX, EBX")
            if tipo0 == "string" or tipo1 == "string":
                sys.stderr.write("Operacao (/) invalida - Erro de Semântica\n Esperado: int\n Recebido: string\n")
                return 0            
            return [int(valor0) / int(valor1), "int"]
        elif self.value == '>':
            writer.w("CMP EAX, EBX")
            writer.w("CALL binop_jg")

            if (tipo0 == "string" and tipo1 == "int") or (tipo0 == "int" and tipo1 == "string"):
                sys.stderr.write("Operacao (>) invalida - Erro de Semântica\n tipos diferentes utilizados\n")
                return 0
            return  [int(valor0 > valor1), "int"]
        elif self.value == '<':
            writer.w("CMP EAX, EBX")
            writer.w("CALL binop_jl")
            if (tipo0 == "string" and tipo1 == "int") or (tipo0 == "int" and tipo1 == "string"):
                sys.stderr.write("Operacao (<) invalida - Erro de Semântica\n tipos diferentes utilizados\n")
                return 0
            return [int(valor0 < valor1), "int"]
        elif self.value == '==':
            writer.w("CMP EAX, EBX")
            writer.w("CALL binop_je")
            if (tipo0 == "string" and tipo1 == "int") or (tipo0 == "int" and tipo1 == "string"):
                sys.stderr.write("Operacao (==) invalida - Erro de Semântica\n tipos diferentes utilizados\n")
                return 0
            return [int(valor0 == valor1), "int"]
        elif self.value == 'or':
            writer.w("OR EAX, EBX")
            if tipo0 == "string" or tipo1 == "string":
                sys.stderr.write("Operacao (or) invalida - Erro de Semântica\n Esperado: int\n Recebido:" + tipo0 + " " + tipo1 + "\n")
                return 0
            return [valor0 or valor1, "int"]
        elif self.value == 'and':
            writer.w("AND EAX, EBX")
            if tipo0 == "string" or tipo1 == "string":
                sys.stderr.write("Operacao (and) invalida - Erro de Semântica\n Esperado: int\n Recebido: string\n")
                return 0
            return [int(valor0) and int(valor1), "int"]
        elif self.value == '..':
            return [str(valor0) + str(valor1), "string"]
        else:
            sys.stderr.write("Operacao invalida\n Erro de Semântica\n")
            return 0
        

        
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,ST,writer):
        filho = self.children[0].evaluate(ST,writer)
        valor = filho[0]
        tipo = filho[1]
        if tipo == "string":
            sys.stderr.write("Operacao invalida - Erro de Semântica\n Esperado: int\n Recebido: string\n")
            return 0
        else:
            if self.value == '+':
                   
                return [valor, "int"]
            elif self.value == '-':
                writer.w("NEG EAX")
                return [-valor, "int"]
            elif self.value == 'not':
                writer.w("NOT EAX")
                return [not valor, int]
        
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)
    def evaluate(self,ST,writer):
        writer.w("MOV EAX, " + str(self.value))
        return [int(self.value), "int"]
    
class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)

    def evaluate(self,ST, writer):
        pass


class Print(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,ST,writer):
        filho = self.children[0].evaluate(ST,writer)
        writer.w("PUSH EAX")
        writer.w("PUSH formatout")
        writer.w("CALL printf")
        writer.w("ADD ESP, 8")
        if filho[1] == "int":
            print(int(filho[0]))
        else:
            print(filho[0])
        

class Assign(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,ST,writer):
        filho = self.children[1].evaluate(ST,writer)
        shift = ST.get(self.children[0].value)[2]
        writer.w("MOV [EBP - " + str(shift) + "], EAX")
        valor = filho[0]
        tipo = filho[1]
        ST.set(self.children[0].value, valor, tipo)

class StringVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self,ST,writer):
        return [self.value, "string"]     

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self,ST,writer):
        shift = ST.get(self.value)[2]
        writer.w("MOV EAX, [EBP - " + str(shift) + "]")
        return ST.get(self.value)

class Block(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST,writer):

        for child in self.children:
            child.evaluate(ST,writer)

class whileNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST,writer):
        writer.w("LOOP_" + str(self.id) + ":")
        filho0 = self.children[0].evaluate(ST,writer)
        writer.w("CMP EAX, False")
        writer.w("JE EXIT_" + str(self.id))
        filho1 = self.children[1].evaluate(ST,writer)
        writer.w("JMP LOOP_" + str(self.id))
        writer.w("EXIT_" + str(self.id) + ":")


    
class ifNode(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self, ST,writer):
        filho0 = self.children[0].evaluate(ST,writer)
        writer.w("CMP EAX, False")
        if len(self.children) == 2:
            writer.w("JE EXIT_" + str(self.id))
            self.children[1].evaluate(ST,writer)
            writer.w("EXIT_" + str(self.id) + ":")
        elif len(self.children) == 3:
            writer.w("JE ELSE_" + str(self.id))
            self.children[1].evaluate(ST,writer)
            writer.w("JMP EXIT_" + str(self.id))
            writer.w("ELSE_" + str(self.id) + ":")
            self.children[2].evaluate(ST,writer)
            writer.w("EXIT_" + str(self.id) + ":")
            
        

        if self.children[0].evaluate(ST,writer)[0]:
            self.children[1].evaluate(ST,writer)
        elif len(self.children) == 3:
            self.children[2].evaluate(ST,writer)

class read(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self,ST,writer):
        writer.w("PUSH scanint")
        writer.w("PUSH formatin")
        writer.w("CALL scanf")
        writer.w("ADD ESP, 8")
        writer.w("MOV EAX, DWORD [scanint]")
        return [int(input()), "int"]
    
class Vardec(Node):
    def __init__(self, value, children):
        super().__init__(value, children)

    def evaluate(self,ST,writer):
        ST.create(self.children[0].value)
        writer.w("PUSH DWORD 0")
        if len(self.children) == 2:
            filho1 = self.children[1].evaluate(ST,writer)
            ST.set(self.children[0].value, filho1[0], filho1[1])
        
    



class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source, position, next):
        self.source = source
        self.position = position
        self.next = next
        self.prohibited =["local", "print", "while", "do", "end", "if", "then", "else", "and", "or", "not", "read"]

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
            elif self.source[self.position] == " " or self.source[self.position] == "\t":
                self.position += 1
                self.selectNext()  
            elif self.source[self.position] == "\"":
                self.position += 1
                start = self.position
                while self.source[self.position] != "\"":
                    self.position += 1
                    if self.position >= len(self.source):
                        sys.stderr.write("Aspas Nao fechadas" + "\n")
                        break
                self.next = Token("STRING", self.source[start:self.position])
                self.position += 1
            
            elif self.source[self.position] == "." and self.source[self.position + 1] == ".":
                self.position += 2               
                self.next = Token("CONCAT", "..")
            else:
                sys.stderr.write("token invalido, posicao: " + str(self.position) + "\n" + str(self.source[self.position]) + "\n")
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
                sys.stderr.write("token invalido, esperado: NEWLINE11, recebido: " + TOKENIZER.next.type + "\n")
        
        elif TOKENIZER.next.type == "LOCAL":
            next = TOKENIZER.selectNext()
            if TOKENIZER.next.type == "IDENT":
                res = Vardec("local", [Identifier(TOKENIZER.next.value)])
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "EQUAL":
                    next = TOKENIZER.selectNext()
                    res.children.append(Parser.parseBoolExpression(TOKENIZER))
                
                if TOKENIZER.next.type != "NEWLINE" and TOKENIZER.next.type != "EOF":
                    sys.stderr.write("token invalido, esperado: NEWLINE12, recebido: " + TOKENIZER.next.type + "\n")
                    
            else:
                sys.stderr.write("token invalido, esperado: IDENT, recebido: " + TOKENIZER.next.type + "\n")


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
        elif TOKENIZER.next.type == "NEWLINE":
            
            res = NoOp()
            next = TOKENIZER.selectNext()

        # elif TOKENIZER.next.type == "EOF":
        #     res = NoOp()

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
                    while TOKENIZER.next.type != "END" and TOKENIZER.next.type != "EOF":
                        
                        bloco.children.append(Parser.parseStatement(TOKENIZER))
                        next = TOKENIZER.selectNext()
                    if TOKENIZER.next.type != "END":
                        sys.stderr.write("token invalido, esperado: END, recebido: " + TOKENIZER.next.type + "\n")
                    else:
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
        elif TOKENIZER.next.type == "STRING":
            res = StringVal(TOKENIZER.next.value)
            
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
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS" or TOKENIZER.next.type == "IDENT":
                    res = BinOp("*", [res, Parser.parseFactor(TOKENIZER)])
                    #res *= Parser.parseFactor(TOKENIZER)
                
                else:
                    sys.stderr.write("token invalido" + TOKENIZER.next.type + "\n")
            elif TOKENIZER.next.type == "DIV":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN" or TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS" or TOKENIZER.next.type == "IDENT":
                    #res /= Parser.parseFactor(TOKENIZER)
                    res = BinOp("/", [res, Parser.parseFactor(TOKENIZER)])
                   
                else:
                    sys.stderr.write("token invalido2")
        
  
        return res

    @staticmethod
    def parseExpression(TOKENIZER):
       
        res = Parser.parseTerm(TOKENIZER)
        while TOKENIZER.next.type == "PLUS" or TOKENIZER.next.type == "MINUS" or TOKENIZER.next.type == "CONCAT":
        
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

            elif TOKENIZER.next.type == "CONCAT":
                next = TOKENIZER.selectNext()
                if TOKENIZER.next.type == "STRING" or TOKENIZER.next.type == "IDENT" or TOKENIZER.next.type == "INT" or TOKENIZER.next.type == "LPAREN":
                    res = BinOp("..", [res, Parser.parseTerm(TOKENIZER)])
                    
                else:
                    sys.stderr.write("4token invalido esperado: STRING, IDENT, recebido: " + TOKENIZER.next.type + "\n")
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
    fileasm = filename.split(".")[0] + ".asm"
    writer = Writer(fileasm)
    writer.clear()
    with open("cabecalho.txt", "r") as file:
        cabecalho = file.read()
        writer.w(cabecalho)
        file.close()

    resultado = parser.evaluate(ST,writer)
    
    with open("rodape.txt", "r") as file:
        rodape = file.read()
        writer.w(rodape)
        file.close()

    

if __name__ == "__main__":
    main()


    