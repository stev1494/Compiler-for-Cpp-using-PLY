from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter.ttk import Progressbar
from lex import *
from parser import *
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, font
import difflib
import ply.yacc as yacc


ventana=Tk()
ventana.geometry("270x270")
ventana.title("Compilador C++")


label=Label(ventana,text="LP-ESPOL-2018",font=("Helvetic", 15))
label.grid(row=1, column=1, sticky="nsew", padx=50, pady=10)

style = ttk.Style(ventana)


#txt = scrolledtext.ScrolledText(ventana, width=40, height=10)
#txt.grid(column=1, row=4)


def selecciona():
    #file = filedialog.askopenfilename()
    file = filedialog.askopenfilename(filetypes=(("Text files", "*.cpp"), ("all files", "*.*")))
    #my_inp = open('cpp_code.cpp', 'r').read()
    my_inp = open(file, 'r').read()
    return my_inp



def analisisLexico():
    lex.lex()
    my_inp=selecciona()


    lex.input(my_inp)
    # list=[]
    variable = ''
    while 1:
        tok = lex.token()
        #list.append(tok)

        # print(list)
        variable = variable + '\n' + str(tok)

        if not tok:
            #print(tok.value)
            break
        #print(tok)
    print(variable)
    return variable


def analisisSintactico():
    parser = yacc.yacc()

    while True:
        try:
            s = selecciona()
        except EOFError:
            break
        if not s: continue
        result = parser.parse(s)
        print(result)
    '''
    yacc.yacc()
    s = selecciona()
    result = yacc.parse(s)
    if result is not None:
        with open("AST.txt", 'w') as f:
            f.write(str(result))
    '''


def probabilidad(var1,var2):
    proba=difflib.SequenceMatcher(None, var1, var2).ratio()

    return proba

def plagio(num):
    bar = Progressbar(ventana, length=200, style='black.Horizontal.TProgressbar')
    bar['value'] = num*100
    print(str(round(num * 100, 2)) + "%")
    bar.grid(column=1, row=9)


def mostrarplagio(num):

    porcentaje=num
    label_plagio = Label(ventana, text=porcentaje)
    label_plagio.grid(column=1,row=9)


def lexico():
    variable1=analisisLexico()
    variable2=analisisLexico()
    plagio(probabilidad(variable1,variable2))
    #mostrarplagio(plagio)




#Definicion de Botones
fuente = font.Font(family='Times', size= 11,weight='bold')
#btn_add1=Button(ventana,text="Seleccione primer archivo", command=selecciona,background="CadetBlue", borderwidth= 3, width=20, height=1, font=fuente )
#btn_add2=Button(ventana,text="Seleccione segundo archivo",command=selecciona,background="CadetBlue", borderwidth= 3, width=20, height=1, font=fuente)

btn_lex=Button(ventana,text="Análisis Léxico",command=lexico,background="CadetBlue", borderwidth= 3, width=20, height=1, font=fuente)
btn_sintax=Button(ventana,text="Análisis Sintáctico",command=analisisSintactico,background="CadetBlue", borderwidth= 3, width=20, height=1, font=fuente)
btn_plagio=Button(ventana,text="Plagio",command=plagio,background="CadetBlue", borderwidth= 3, width=20, height=1, font=fuente)

#Posicionamiento de Botones
#btn_add1.grid(column=1,row=2, padx=2, pady=2)
#btn_add2.grid(column=1,row=3,padx=2, pady=2)
btn_plagio.grid(column=1,row=8, padx=2, pady=2)
btn_lex.grid(column=1,row=4, padx=2, pady=2)
btn_sintax.grid(column=1,row=5, padx=2, pady=2)


##Presentacion de la ventana
ventana.mainloop()



