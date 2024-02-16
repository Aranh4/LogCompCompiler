import sys

import sys

def aplicaoperacao(listanumeros, listaoperadores):
    dictoperadores = {"+": lambda x, y: x + y, "-": lambda x, y: x - y}
    result = listanumeros[0]
    for i in range(0, len(listaoperadores)):
        result = dictoperadores[listaoperadores[i]](result, listanumeros[i+1])
    return result

def main(args):
    operandos = ['+', '-']
    listanumeros = []
    listaoperadores = []
    last= ""
    number = ""
    temespaco = False
    if len(args) == 0:
        return "No arguments given"
    for c in args[0]:
        if (c != "+" and c != "-" and not temespaco) or c == " ":
            if c == " ":
                if number != "":
                    temespaco = True
                continue
            number += c

        
        
        elif c in operandos:
            temespaco = False
            listanumeros.append(int(number))
            
            number = ""
            listaoperadores.append(c)

        else:
            sys.stderr.write("Error: invalid input")
            return
        
    listanumeros.append(int(number))
         
    resultado = aplicaoperacao(listanumeros, listaoperadores)
   
            

       
        

    return resultado

if __name__ == "__main__":
    args = sys.argv[1:]
    print(main(args))

    
        