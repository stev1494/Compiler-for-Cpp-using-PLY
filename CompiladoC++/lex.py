import ply.lex as lex
import sys
from symbolTable import MainSymbolTable
from symbolTable import SymbolTable
import os

import difflib


reserved = dict.fromkeys(
	['asm', 'else', 'new', 'this', 'auto', 'enum', 'operator', 'throw', 'bool', 'explicit', 'private', 'true', 'break', 'export', 'protected', 'try', 'case', 'extern', 'public', 'typedef', 'catch', 'false', 'register', 'typeid', 'char', 'float', 'reinterpret_cast', 'typename', 'class', 'for', 'return', 'union', 'const', 'friend', 'short', 'unsigned', 'const_cast', 'goto', 'signed', 'using', 'continue', 'if', 'sizeof', 'virtual', 'default', 'inline', 'static', 'void', 'delete', 'int', 'static_cast', 'volatile', 'do', 'long', 'struct', 'wchar_t', 'double', 'mutable', 'switch', 'while', 'dynamic_cast', 'namespace', 'template'] , 'KEYWORD'
)

data_types=('enum', 'bool', 'char', 'float', 'short', 'unsigned', 'signed', 'void', 'int', 'long', 'double')

predef_func = dict.fromkeys(
	['cin', 'cout','cerr','exit','gets','puts','malloc','calloc','realloc','atoi'] , 'PREDEFINED_FUNCTION'
)

extra_words = ['include','main','std']

# List of token names.   This is always required
tokens = [
   'INTNUM','FLOATNUM','PLUSPLUS','MINUSMINUS',
    'LEFTSQRBRACKET' , 'RIGHTSQRBRACKET',
    'MULT_EQ','DIVIDE_EQ','MOD_EQ','PLUS_EQ',
   'TIMES', 'MINUS_EQ', 'GTEQ', 'LTEQ', 'AND_EQ',
   'DIVIDE', 'OR_EQ','XOR_EQ', 'LSHIFT_EQ','RSHIFT_EQ',
   'LPAREN','BIT_OR','BIT_XOR','BIT_AND', 'CHAR_CONST',
   'RPAREN', 'OR','AND','EQUAL','NEQUAL',
   'GT',
   'LT',
   'ID',
   'STRING',
   'KEYWORD',
   'PREDEFINED_FUNCTION', 
   'ASSIGNMENT',
   'TERMINAL',
   'LSHIFT',
   'RSHIFT',
   'MOD',
   'U_PLUS',
   'U_MINUS',
   'BIT_NOT',
   'NOT',
   'DEREF',
   'COLON',
   'LEFTCURLYBRACKET',
   'RIGHTCURLYBRACKET',
   'DEREF_ONE',
   'DEREF_TWO',
   'QUES_MARK',
   'COMMA',
   'HASH'
] 

tokens += [kwd.upper() for kwd in reserved]
tokens += [kwd.upper() for kwd in predef_func]
tokens += [kwd.upper() for kwd in extra_words]

# Regular expression rules for simple tokens

t_HASH = r'\#'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_GT  = r'\>'
t_LT  = r'\<'
t_ASSIGNMENT = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_STRING = r'[a-zA-Z_]?\"(\\.|[^\\"])*\"'
t_TERMINAL = r';'
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'\-\-'
t_LEFTSQRBRACKET = r'\['
t_RIGHTSQRBRACKET = r'\]'
t_MULT_EQ = r'\*='
t_DIVIDE_EQ = '/='
t_MOD_EQ = '%='
t_PLUS_EQ = r'\+='
t_MINUS_EQ = '-='
t_LSHIFT_EQ = '<<='
t_RSHIFT_EQ = '>>='
t_GTEQ = '>='
t_LTEQ = '<='
t_AND_EQ = '&='
t_OR_EQ = r'\|='
t_XOR_EQ = '\^='
t_BIT_OR = r'\|'
t_BIT_XOR = r'\^'
t_BIT_AND = r'&'
t_OR = r'\|\|'
t_AND = '&&'
t_EQUAL = '=='
t_NEQUAL = '!='
t_LSHIFT = '<<'
t_RSHIFT = '>>'
t_MOD = '%'
t_U_PLUS    = r'\+'
t_U_MINUS    = r'\-'
t_BIT_NOT = '~'
t_NOT = '!'
t_COLON =':'
t_LEFTCURLYBRACKET ='{'
t_RIGHTCURLYBRACKET ='}'
t_DEREF_ONE =r'\.'
t_DEREF_TWO =r'–>'
t_QUES_MARK = r'\?' 
t_COMMA = r','  
t_CHAR_CONST = r"\'.\'"

def t_COMMENT(t):
    r"(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)"
    pass
    # No return value. Token discarded

# A regular expression rule with some action code

main_table = MainSymbolTable()
main_table.add_table(SymbolTable(main_table.outScope))

def t_FLOATNUM(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved or t.value in predef_func or t.value in extra_words:
        t.type = t.value.upper()    # Check for reserved words
    if t.type == 'ID':
        symbol_table = main_table.get_table(main_table.inScope-1)
        symbol_table.add_entry(t)
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t' + r'$'

# Error handling rule
def t_error(t):
    print("Illegal character ",t.value[0])
    t.lexer.skip(1)


lex.lex()


def seleccionaArchivo ():
    my_inp = open('c.cpp', 'r').read()
    return my_inp


def analisisLexico():
    my_inp=seleccionaArchivo()

    lex.input(my_inp)
    # list=[]
    variable = ''
    while 1:
        tok = lex.token()
        #list.append(tok)

        # print(list)
        variable = variable + '\n' + str(tok)

        if not tok:
            break
        # print(tok)
    print(variable)
    return variable

def probabilidad(var1,var2):
    proba=difflib.SequenceMatcher(None, var1, var2).ratio()
    return probabilidad












