# Yacc example
import copy
import ply.yacc as yacc
import AST

# Get the token map from the lexer.  This is required.
from lex import tokens
from lex import main_table

import sys

import TAC as TAC

threeAC = TAC.threeAC()

from symbolTable import SymbolTable

def get_node(symtab,val):
	while(True):
		indicies = [index for index, value in enumerate(symtab.variables) if value == val]
		if len(indicies)>0:
			for x in indicies:
				if symtab.symtab[indicies[0]][0][1]!=None:
					return symtab.symtab[indicies[0]][1]
		if symtab.outScope > 0:
			symtab = main_table.get_table(symtab.outScope-1)
		else:
			return -1

dec=0

import warnings
warnings.filterwarnings("ignore")

#def p_preProc(p):
#	'''preProc : HASH INCLUDE LT identifier GT stdNamespace '''
	
#def p_stdNamespace(p):
#	'''stdNamespace : USING NAMESPACE STD TERMINAL mainFunc '''

#main function
def p_mainFunc(p):
	'''mainFunc : INT MAIN LPAREN RPAREN statement '''	
	p[0] = p[5]

def p_expression(p):
	'''expression : assignmentExpression
               		| expression COMMA assignmentExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_assignmentExpression(p):
	'''assignmentExpression : conditionalExpression
				| unaryExpression assignOper assignmentExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if(p[1] is not None and p[3] is not None):
			if (p[1].type!=p[3].type):
				print("Datatype mismatch, performing coercion!")
				#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
				#mismatch has to mean int and float, hence coercion to float
				p[0].type=p[1].type
			if(p[3] is not None):
				if(p[3].expr_type == "constant" or p[3].expr_type == "id"):
					if(len(p[2])==2):
						threeAC.AddToTable(p[1],p[3],p[2][0])
						threeAC.AddToTable(p[1],'',p[2][1])
					else:
						threeAC.AddToTable(p[1],p[3],p[2])
				else:
					threeAC.AddToTable(p[1],'',p[2])

	
def p_unaryExpression(p):
	'''unaryExpression : postfixExpression 
			| PLUSPLUS unaryExpression
			| MINUSMINUS unaryExpression
			| unaryOper unaryExpression
			| SIZEOF unaryExpression
			| SIZEOF LPAREN simpleTypeName RPAREN '''
	if(len(p)==2):
		p[0]=p[1]
	elif len(p) == 3:
		p[0] = AST.Expr("unPreOp",operator=p[1],operand1=p[2])
		p[0].type = p[2].type
		threeAC.AddToTable('',p[2],p[1])
	else:
		p[0] = AST.Expr("unaryop",operator=p[1],operand1=p[3])
		p[0].type = p[2].type
		threeAC.AddToTable(p[3],'',p[1])

def p_primaryExpression(p):
	'''primaryExpression : markid 
                       | constant
                       | markstr STRING
                       | LPAREN expression RPAREN '''
	if(len(p)==2):
		p[0] = p[1]
	elif len(p) == 3: #string
		p[0]  = AST.Expr("constant",operand1=p[1],constType='string')
	else:
		p[0]=p[2]

def p_markid(p):
	'''markid : identifier'''
	p[0] = AST.Expr("id",operand1=p[1],constType=p[1].type)


def p_markstr(p):
	'''markstr : '''

def p_postfixExpression(p):
	'''postfixExpression : primaryExpression
			| postfixExpression LEFTSQRBRACKET expression RIGHTSQRBRACKET
			| postfixExpression PLUSPLUS
			| postfixExpression MINUSMINUS'''
			#| DYNAMIC_CAST LT simpleTypeName GT LPAREN expression RPAREN 
			#| STATIC_CAST LT simpleTypeName GT LPAREN expression RPAREN
			#| CONST_CAST LT simpleTypeName GT LPAREN expression RPAREN 
			#| postfixExpression DEREF_ONE identifier
			#| postfixExpression DEREF_TWO identifier
	if(len(p)==2):
		p[0]=p[1]
	elif len(p)==5:
		if(p[3].type!='int'):
			print("Array index has to be int!")
		p[0] = AST.Expr("arrayop",operator='[]',operand1=p[1],operand2=p[3])
		p[0].type = p[1].type.split('[')[0]
		threeAC.AddToTable(p[1],p[3],'[]')
	else:
		p[0] = AST.Expr("unPostOp",operator=p[2],operand1=p[1])
		p[0].type = p[1].type
		threeAC.AddToTable(p[1],'',p[2])

def p_constant(p):
	'''constant : markint INTNUM
		| markfloat FLOATNUM
		| markchar CHAR_CONST'''
	p[0] = AST.Expr("constant",operand1=p[2],constType=p[1])

def p_markint(p):
	'''markint : empty'''
	p[0] = 'int'

def p_markfloat(p):
	'''markfloat : empty'''
	p[0] = 'float'

def p_markchar(p):
	'''markchar : empty'''
	p[0] = 'char'

def p_assignOper(p):
	'''assignOper : ASSIGNMENT
			| MULT_EQ
			 |  DIVIDE_EQ
			 | MOD_EQ
			 | PLUS_EQ 
			 | MINUS_EQ
			 | GTEQ
			 | LTEQ
			 | AND_EQ
			 | XOR_EQ
			 | OR_EQ '''
	p[0]=p[1]

def p_conditionalExpression(p):
	'''conditionalExpression : logicalOrExpression 
                          | logicalOrExpression QUES_MARK expression COLON conditionalExpression''' #need to implement
	if(len(p)==2):
		p[0]=p[1]
		
def p_logicalOrExpression(p):
	'''logicalOrExpression : logicalAndExpression 
				| logicalOrExpression  OR   logicalAndExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in logical OR expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		threeAC.AddToTable(p[1],p[3],p[2])

def p_logicalAndExpression(p):
	'''logicalAndExpression : inclusiveOrExpression 
				| logicalAndExpression  AND   inclusiveOrExpression'''	
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in logical AND expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		threeAC.AddToTable(p[1],p[3],p[2])

def p_inclusiveOrExpression(p):
	'''inclusiveOrExpression : exclusiveOrExpression 
			| inclusiveOrExpression BIT_OR exclusiveOrExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in inclusive OR expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		threeAC.AddToTable(p[1],p[3],p[2])

def p_exclusiveOrExpression(p):
	'''exclusiveOrExpression : andExpression 
			| exclusiveOrExpression BIT_XOR andExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in XOR expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		threeAC.AddToTable(p[1],p[3],p[2])

def p_andExpression(p):
	'''andExpression : equalityExpression 
			| andExpression BIT_AND equalityExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in bitwise AND expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		threeAC.AddToTable(p[1],p[3],p[2])

def p_equalityExpression(p):
	'''equalityExpression : relationalExpression 
			| equalityExpression EQUAL relationalExpression
			| equalityExpression NEQUAL relationalExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in equality expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		threeAC.AddToTable(p[1],p[3],p[2])
		
			
def p_relationalExpression(p):
	'''relationalExpression : shiftExpression
			| relationalExpression LT shiftExpression
			| relationalExpression GT shiftExpression
			| relationalExpression LTEQ shiftExpression
			| relationalExpression GTEQ shiftExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in relational expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		threeAC.AddToTable(p[1].value,p[3].value,p[2])
			
def p_shiftExpression(p):
	'''shiftExpression : additiveExpression
			| shiftExpression LSHIFT additiveExpression
			| shiftExpression RSHIFT additiveExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in shift expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		threeAC.AddToTable(p[1],p[3],p[2])
			
def p_additiveExpression(p):
	'''additiveExpression : multiplicativeExpression
			| additiveExpression U_PLUS multiplicativeExpression
			| additiveExpression U_MINUS multiplicativeExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type="int"
				print(p[0].type)
			else:
				p[0].type="float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in additive expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		if(len(p)==4):
			if p[2] == '+':
				threeAC.AddToTable(p[1],p[3],'+')
			elif p[2] == '-':
				threeAC.AddToTable(p[1],p[3],'-')			

def p_multiplicativeExpression(p):
	'''multiplicativeExpression : castExpression
			| multiplicativeExpression TIMES castExpression
			| multiplicativeExpression DIVIDE castExpression
			| multiplicativeExpression MOD castExpression'''
	if(len(p)==2):
		p[0]=p[1]
	else:
		p[0] = AST.Expr("binop",operator=p[2],operand1=p[1],operand2=p[3])
		if (p[1].type==p[3].type):
			if(p[1].type=="char" or p[3].type=="char"):
				print("Error! Cannot perform operation on character datatype!")
				sys.exit()
			elif (p[1].type=="int"):
				p[0].type = "int"
			else:
				p[0].type = "float"
		elif (p[1].type!=p[3].type):
			#print("Datatype mismatch in ",str(p[1].operand1)," and ",str(p[3].operand1)," performing coercion!")
			print("Datatype mismatch in multiplicative expression, performing coercion!")
			#mismatch has to mean int and float, hence coercion to float
			p[0].type = "float"
		if(len(p)==4):
			if p[2] == '*':
				threeAC.AddToTable(p[1],p[3],'*')	
			elif p[2] == '/':
				threeAC.AddToTable(p[1],p[3],'/')
			elif (p[1] == '(' and p[3] == ')'):
				p[0]=p[2]

def p_castExpression(p):
	'''castExpression : unaryExpression
			| LPAREN simpleTypeName RPAREN castExpression'''
	if(len(p)==2):
		p[0]=p[1]

def p_unaryOper(p):
	'''unaryOper : TIMES
			| BIT_AND
			| U_PLUS
			| U_MINUS
			| NOT
			| BIT_NOT'''
	p[0]=p[1]
		
def p_simpleTypeName(p):
	'''simpleTypeName : CHAR
			| SHORT
			| INT
			| LONG
			| SIGNED
			| UNSIGNED
			| FLOAT
			| DOUBLE
			| VOID'''
	#p[0] = {'type':p[1]}
	p[0] = AST.Type(p[1])
			
#empty production used in optional cases		

def p_empty(p):
    'empty :'
    pass
    
			
def p_statement(p):
	'''statement : labeledStatement
			| expressionStatement
			| compoundStatement
			| selectionStatement
			| jumpStatement'''	#| iterationStatement
	p[0] = p[1]
	
			
def p_labeledStatement(p):
	'''labeledStatement : identifier COLON statement
			| caseList default '''
	if len(p) == 3:
		p[0] = AST.CaseList(p[1], p[2])

def p_caseList(p):
	'''caseList : caseList CASE constantExpression COLON statement
		| empty'''
	if len(p) == 6:
		p[1].add_case(p[3], p[5])
		p[0] = p[1]
		threeAC.AddToTable('','','break')
	else:
		p[0] = AST.Case()

def p_default(p):
	'''default : DEFAULT defaultmark COLON statement enddefault	
		| empty '''
	if(len(p)==4):
		p[0] = AST.CaseDefault(p[3])
	else:
		p[0]=None
			
def p_defaultmark(p):
	'''defaultmark : empty '''
	threeAC.AddToTable('','','Default')

def p_enddefault(p):
	'''enddefault : empty '''
	threeAC.AddToTable('','','EndDefault')

def p_constantExpression(p):
	'''constantExpression : conditionalExpression '''
	p[0]=p[1]
	threeAC.AddToTable(p[1],'',"case")

def p_expressionStatement(p):
	'''expressionStatement : expression TERMINAL
			| empty'''
	if len(p)==3:
		p[0] = p[1]
	else:
		p[0] = None
			
def p_compoundStatement(p):
	'''compoundStatement : oscope declarationList statementList cscope
			| empty'''
	if len(p) == 5:
		if len(p[2].declarations) != 0:
			p[0] = AST.CompoundStmt(p[3], p[2])
		else:	
			p[0] = AST.CompoundStmt(p[3])
	else:
		p[0] = None

def p_oscope(p):
	'''oscope : LEFTCURLYBRACKET'''
	main_table.inScope=main_table.prev_inScope+1
	main_table.prev_inScope+=1
	main_table.outScope+=1
	tab = SymbolTable(main_table.outScope)
	main_table.add_table(tab)
		
def p_cscope(p):
	'''cscope : RIGHTCURLYBRACKET'''
	main_table.inScope-=1
	main_table.outScope-=1											
	
def p_statementList(p):
	'''statementList : statementList statement
			| empty '''
	if len(p) == 3:
		p[1].add_stmt(p[2])
		p[0] = p[1]
	else:
		p[0] = AST.StmtList()

def p_declarationList(p):
	'''declarationList : declarationList declaration
			| empty '''
	if len(p) == 2:
		p[0] = AST.DecList()
	else:
        	p[1].add_decl(p[2])
        	p[0] = p[1]

def p_declaration(p):
	'''declaration :  decSpecList initDecList TERMINAL '''
	global dec	
	dec = 0
	main_table.insert = 0
	p[0] = AST.Declaration(p[1], p[2])

def p_initDecList(p):
	'''initDecList : initDecList COMMA markDec initDec
			| initDec '''
	if len(p)==2:
		p[0] = AST.IdentList([p[1]])
	else:
		p[1].add_identifier(p[4])
		p[0] = p[1]

def p_markDec(p):
	'''markDec : empty '''
	p[0] = p[-3]

def p_decSpecList(p):
	'''decSpecList : decSpecList decSpec
			| decSpec '''
	if(len(p)==2):
		p[0] = p[1]
	else:
		p[0] = p[1].combine(p[2].type)
	global dec
	dec=1
	main_table.insert=1

def p_initDec(p):
	''' initDec : declarator
                    | declarator ASSIGNMENT assignmentExpression'''	
	if len(p)==4:
		p[1].add_value(p[3])
	p[0] = p[1]
	if(p[1].value is not None):
		threeAC.AddToTable(p[1].id,p[1].value.operand1,'=')


def p_declarator(p):
	'''declarator : pointerList directDec'''
	p[0] = p[2]

def p_pointerList(p):
	''' pointerList : pointer
			| empty '''
	if (p[1] != None):
		p[0] = p[1]

def p_pointer(p):
	'''pointer : star typeQualList
		| empty	'''
	if(len(p)==3):
		p[0] = { 'type': p[1]['type'] + p[2]['type'] }	

def p_star(p):
	'''star : star TIMES
		| TIMES	'''
	if(len(p)==2):
		p[0]={'type':'*'}
	else:
		p[0] = p[1]
		p[0]['type']+='*'

def p_typeQualList(p):
	''' typeQualList : typeQualifier
			| empty '''
	if(p[1] != None):
		p[0] = p[1]
	else:
		p[0] = {'type':''}

def p_directDec(p):
	'''directDec : identifier
                      | identifier arrayDec'''
		      #| LEFTCURLYBRACKET declarator RIGHTCURLYBRACKET
                      #| directDec LEFTCURLYBRACKET idList RIGHTCURLYBRACKET
		      #| directDec LPAREN parTypeList RPAREN 
	if(len(p)==3):
		symbol_table = main_table.get_table(main_table.inScope-1)
		p[1].changeToArray(p[2]['val'])
		symbol_table.change_array(p[2]['val'])
	p[0]=p[1]

def p_arrayDec(p): #constExprList
	'''arrayDec : arrayDec LEFTSQRBRACKET INTNUM RIGHTSQRBRACKET	
		| LEFTSQRBRACKET INTNUM RIGHTSQRBRACKET	'''
	if(len(p)==4):
		p[0] = {'val': [int(p[2]),]}
	else:
		p[1]['val'].append(int(p[3]))
		p[0] = p[1]
	

def p_identifier(p):
	'''identifier : ID'''
	symbol_table = main_table.get_table(main_table.inScope-1)
	if(dec==1):
		ret = symbol_table.check_existing(p[1])
		if ret ==-1:
			print("Redeclaration of variable:",p[1])
			sys.exit()	
		elif(p[-1] is None):
			p[0] = AST.Identifier(p[1],idtype = p[-2].type)
			symbol_table.add_type(p[-2].type,p[0])
		else:
			p[0] = AST.Identifier(p[1],idtype = p[-2].type+p[-1]['type'])
			symbol_table.add_type(p[-2].type+p[-1]['type'],p[0])
	else:
		#return sym table entry
		symbol_table.check_existing(p[1])
		node = get_node(symbol_table,p[1])
		if node != -1:
			p[0] = node
		else:
			print("Variable undeclared or outOfScope!")
			sys.exit()
	if(threeAC.switch_cond==1):
		threeAC.AddToTable(p[1],'',"id")
		threeAC.switch_cond=0
	
	#remember while adding to symbol table make changes in directDec for array type

def p_decSpec(p):
	'''decSpec : StorageClassSpec
                          | simpleTypeName
                          | typeQualifier '''
	p[0] = p[1]

def p_typeQualifier(p):
	''' typeQualifier : CONST
			  | VOLATILE '''
	p[0] = AST.Type(p[1])

def p_StorageClassSpec(p):
	'''StorageClassSpec : AUTO
                            | REGISTER
                            | STATIC
                            | EXTERN
                            | TYPEDEF '''
	p[0] = AST.Type(p[1])
			
def p_selectionStatement(p):
	'''selectionStatement : IF LPAREN ifmark expression RPAREN statement endifmark 
			| IF LPAREN ifmark expression RPAREN statement endifmark ELSE elsemark statement
			| SWITCH LPAREN switchmark expression RPAREN statement endswitchmark'''
	if len(p)==11:
		p[0] = AST.IfStmt(p[4], p[6], p[10])
		threeAC.AddToTable('','',"endelse")
	elif len(p) == 8:
		if (p[1] == "if"):
			p[0] = AST.IfStmt(p[4], p[6])
		else:
			p[0] = AST.SwitchStmt(p[4], p[6])

def p_ifmark(p):
	'''ifmark : empty '''
	threeAC.AddToTable('','',"if")
		
def p_endifmark(p):
	'''endifmark : empty '''
	threeAC.AddToTable('','',"endif")

def p_elsemark(p):
	'''elsemark : empty '''
	threeAC.AddToTable('','',"else")

def p_switchmark(p):
	'''switchmark : empty '''
	threeAC.switch_cond=1
	threeAC.AddToTable('','',"switch")

def p_endswitchmark(p):
	'''endswitchmark : empty '''
	threeAC.AddToTable('','',"endswitch")

def p_jumpStatement(p):
	'''jumpStatement : BREAK TERMINAL
			| CONTINUE TERMINAL
			| RETURN expression TERMINAL
			| RETURN TERMINAL
			| GOTO identifier TERMINAL'''
	if(p[1]=="break"):
		p[0]=AST.JumpStmt()
	elif(p[1]=="continue"):
		p[0]=AST.JumpStmt("continue")
	elif p[1] == "return":
		if len(p)==4:
			p[0] = AST.RetStmt(p[2])
		else:
			p[0] = AST.RetStmt()

# Error rule for syntax errorscl
def p_error(p):
	if p is not None:
		print("Syntax error in input\n error: near",p.value,"at line:",p.lineno)
		sys.exit()	

# 	Build the parser
#parser = yacc.yacc()

#Test
yacc.yacc()

s=open('cpp_code2.cpp','r').read()
print (yacc.parse(s))
#s=open('cpp_code.cpp','r').read()
#result = parser.parse(s)
#if result is not None:
#	with open("AST.txt",'w') as f:
#		f.write(str(result))





'''
threeAC.ThreeAddressCode()

print("_______________________")
print()
threeAC.printTriples()

print()			
print("_______________________")
print()	
print("OPTIMIZED CODE")
print("_______________________")
print()

print()
print("AFTER CONSTANT AND COPY PROPAGATION")
print()

threeAC.const_prop()


print()
print("AFTER CONSTANT FOLDING")
print()

threeAC.const_fold()

print()
print("AFTER DEAD CODE ELIMINATION")
print()

threeAC.dead_code()

#main_table.print_table()

'''


