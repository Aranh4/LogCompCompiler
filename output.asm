; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

formatin: db "%d", 0
formatout: db "%d", 10, 0 ; newline, nul terminator
scanint: times 4 db 0 ; 32-bits integer = 4 bytes

segment .bss  ; variaveis
res RESB 1

section .text
global main ; linux
;global _main ; windows
extern scanf ; linux
extern printf ; linux
;extern _scanf ; windows
;extern _printf; windows
extern fflush ; linux
;extern _fflush ; windows
extern stdout ; linux
;extern _stdout ; windows

; subrotinas if/while
binop_je:
JE binop_true
JMP binop_false

binop_jg:
JG binop_true
JMP binop_false

binop_jl:
JL binop_true
JMP binop_false

binop_false:
MOV EAX, False  
JMP binop_exit
binop_true:
MOV EAX, True
binop_exit:
RET

main:

PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; estabelece um novo base pointer

; codigo gerado pelo compilador abaixo

PUSH DWORD 0
PUSH DWORD 0
PUSH DWORD 0
PUSH scanint
PUSH formatin
CALL scanf
ADD ESP, 8
MOV EAX, DWORD [scanint]
MOV [EBP - 8], EAX
MOV EAX, 1
MOV [EBP - 12], EAX
MOV EAX, 2
MOV [EBP - 4], EAX
LOOP_39:
MOV EAX, [EBP - 4]
PUSH EAX
MOV EAX, [EBP - 8]
PUSH EAX
MOV EAX, 1
MOV EBX, EAX
POP EAX
ADD EAX, EBX
MOV EBX, EAX
POP EAX
CMP EAX, EBX
CALL binop_jl
CMP EAX, False
JE EXIT_39
MOV EAX, [EBP - 12]
PUSH EAX
MOV EAX, [EBP - 4]
MOV EBX, EAX
POP EAX
IMUL EAX, EBX
MOV [EBP - 12], EAX
MOV EAX, [EBP - 4]
PUSH EAX
MOV EAX, 1
MOV EBX, EAX
POP EAX
ADD EAX, EBX
MOV [EBP - 4], EAX
JMP LOOP_39
EXIT_39:
MOV EAX, [EBP - 12]
PUSH EAX
PUSH formatout
CALL printf
ADD ESP, 8

; interrupcao de saida (default)

PUSH DWORD [stdout]
CALL fflush
ADD ESP, 4

MOV ESP, EBP
POP EBP

MOV EAX, 1
XOR EBX, EBX
INT 0x80
