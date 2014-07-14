#!/usr/bin/env python

# exprToString/prefix/postfix expression conversion

import tpg

if tpg.__python__ == 3:
    raw_input = input

class WrongParamsError(tpg.Error):
    """ WrongParamsError(msg)

    WrongParamsError is raised by user actions when an error is detected.

    Attributes:
        msg  : message associated to the error
    """
    pass
class Op:
    """ Binary operator """
    def __init__(self, op, a, b, prec):
        self.op = op            # operator ("+", "-", "*", "/", "^")
        self.prec = prec        # precedence of the operator
        self.a, self.b = a, b   # operands
    def exprToString(self):
        a = self.a.exprToString()
        if self.a.prec < self.prec: a = "(%s)"%a
        b = self.b.exprToString()
        if self.b.prec <= self.prec: b = "(%s)"%b
        return "%s %s %s"%(a, self.op, b)
    def printString(self):
        a = self.a.printString()
        b = self.b.printString()
        return "Op(%s %s %s)"%(self.op,a,b)

class Atom:
    """ Atomic expression """
    def __init__(self, s):
        self.a = s
        self.prec = 99
    def exprToString(self): return self.a
    def printString(self): return 'Atom(%s)' % self.a

class Func:
    """ Function expression """
    def __init__(self, parser,name, parmList):
        self.name = name
        self.args = parmList
        self.prec = 98
        self.checkParams()
    def exprToString(self):
        args = [a.exprToString() for a in self.args]
        #modifierStr = ",".join(self.modifiers)
        return "%s(%s)"%(self.name,",".join(args))
    def checkParams(self):
        if len(self.args) > 3:
            if parser.lexer.last_token is None:
                last_token = ""
                line, column = 1, 1
            else:
                last_token = parser.lexer.last_token.text
                line, column = parser.lexer.last_token.line, parser.lexer.last_token.column
            raise WrongParamsError((line, column),"Function arguments error at %s." % (self.exprToString()))
    def printString(self):
        args = [a.printString() for a in self.args]
        #modifierStr = ",".join(self.modifiers)
        return "function_%s(%s)"%(self.name,",".join(args))


# Grammar for arithmetic expressions

class ExpressionParser(tpg.Parser):
    r"""

    set lexer_ignorecase = True
    separator space "\s+";
    token func "\b(peek|match|sum|min|max|count|avg)\b" ;


    token distinct "DISTINCT" ;
    token total "TOTAL" ;
    token real      '(\d+\.\d*|\d*\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+' ;
    token integer   '\d+' ;
    token str1 '".*?"' ;
    token str2 "'.*?'" ;
    token ident "\w+" ;




    START/e ->
        EXPR/e          "\n";

    # exprToString expressions

    EXPR/e -> TERM/e ( "[+-]"/op TERM/t     $ e=Op(op,e,t,1)
                     )*
    ;
    TERM/t -> FACT/t ( "[*/]"/op FACT/f     $ t=Op(op,t,f,2)
                     )*
    ;
    FACT/f -> ATOM/f ( "\^"/op FACT/e       $ f=Op(op,f,e,3)
                     )?
    ;

    FUNC/a ->                          $ params = []
        func/f "\(" 
            ( total  )? 
            (distinct )? 
            ( EXPR/x $params.append(x)$ )? 
            ( "," EXPR/xn $params.append(xn)$ )*  
                "\)" $ a = Func(self,f,params)
    ;    
    ATOM/a ->
           ident/s                            $ a=Atom(s)
       |   integer/s                          $ a=Atom(s)
       |   str1/s                             $ a=Atom(s)                              
       |   str2/s                             $ a=Atom(s)                              
       |   real/s                             $ a=Atom(s)
       |    "\(" EXPR/a "\)"
       |    FUNC/a
    ;

    OP/<op,prec> ->
        "[+-]"/op $ prec=1
    |   "[*/]"/op $ prec=2
    |   "\^"/op   $ prec=3
    ;

    """

parser = ExpressionParser()
e = "a + min(disTINCT 'asd', 3 , 5)"
try:
    expr = parser(e+"\n")
    #print('asdf')
except tpg.Error:
    print(tpg.exc())
else:
    print("\texprToString   : %s "%expr.exprToString())
    print("\touput   : %s "%expr.printString())
