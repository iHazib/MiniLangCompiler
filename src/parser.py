import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    'program : statements'
    p[0] = ('program', p[1])

def p_statements(p):
    '''statements : statement statements
                  | statement'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]

def p_statement_assign(p):
    'statement : LET ID EQUALS expression SEMICOLON'
    p[0] = ('assign', p[2], p[4])

def p_statement_print(p):
    'statement : PRINT expression SEMICOLON'
    p[0] = ('print', p[2])

def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'
    p[0] = ('while', p[3], p[6])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression GT expression
                  | expression LT expression
                  | expression EQEQ expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number', p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = ('id', p[1])

def p_error(p):
    if p:
        print(f"Syntax Error: Unexpected token '{p.value}' at line {p.lineno}")
    else:
        print("Syntax Error: Unexpected end of input")

parser = yacc.yacc()