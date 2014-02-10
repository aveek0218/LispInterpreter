#!/usr/bin/env python
#-------------------------------------------------------------
# Name:       InterpreterP2.py
# Purpose:    Course Project
# Author:     Aveek Mukhopadhyay
# Created:    03/22/2013
#-------------------------------------------------------------
from primitives import *
import sys
import re
functions = False
def dotnotation(exp):
    if isinstance(exp, tuple):
        return "(%s . %s)" % (dotnotation(exp[0]),dotnotation(exp[1]))
    else:
        if isinstance(exp, bool):
            if exp:
                return "T"
            else:
                return "NIL"
        return str(exp)
    
def tokenize(atom):
    numeral = re.match(r"^\s*([\-\+]?[0-9]+)\s*$", atom)
    if numeral:
        return int(numeral.group(1))
    alpha = re.match(r"^\s*([A-Za-z]\w*)\s*$", atom)
    if alpha:
        token = alpha.group(1)
        if token == "NIL":
            return False
        elif token == "T":
            return True
        else:
            return token
    raise Exception("Not Invalid atom %s" % atom)
def parseExprWithDot(expr):
    matches = re.match(r"^\(.*\)$", expr)
    if matches:
        expr = expr[1:-1]
        parcount = 0
        for location, character in enumerate(expr):
            if character == '(':
                parcount += 1
            elif character == ')':
                parcount -= 1
            elif parcount == 0 and character == '.':
                return ( mainparser(expr[:location]) , mainparser(expr[location+1:]) )
        raise Exception("Invalid:\n%s" % (expr))

def parseListExpr(expr):
    if re.match(r"^\(\s*\)$", expr):
        return tokenize("NIL")
    matches = re.match(r"^\(.*\)$", expr)
    if matches:
        expr = expr[1:-1]
        parcount = 0
        start = -1
        
        for location, character in enumerate(expr):
            if character == ')':
                parcount -= 1
                if parcount == 0:
                    element = expr[start:location+1]
                    return cons( mainparser(element), mainparser("(%s)" % expr[location+1:]) )
            elif parcount == 0 and start > -1 and re.match(r"\s|\(", character):
                element = expr[start:location]
                return cons( mainparser(element), mainparser("(%s)" % expr[location:]) )
            elif parcount == 0 and start == -1 and re.match(r"[\-\+\w]", character):
                start = location
            elif character == '(':
                if parcount == 0:
                    start = location
                parcount += 1
                
        if parcount == 0 and start > -1:
            element = expr[start:location+1]
            
            return cons( mainparser(element), mainparser("(%s)" % expr[location+1:]) )           
    raise Exception("Bad List")
def argcount(l):
    d = 1
    for i in l:
        if(type(i) == tuple):
            d = d + argcount(i)
        else:
            continue
    return d
def nestcount(l):
    d = 0
    for i in l:
        if(type(i) == tuple):
            d = d + nestcount(i)
        else:
            d = d + 1
    return d
def chkdot(expr):
    matches = re.match(r"^\(.*\)$", expr)
    if matches:
        expr = expr[1:-1]
        parcount = 0
        for location, character in enumerate(expr):
            if character == '(':
                parcount += 1
            elif character == ')':
                parcount -= 1
            elif parcount == 0 and character == '.':
                return (True, location)
    return (False, 0)
def chkParenthesisBalance(expression):
   parfreq = defaultdict(int)
   for s in expression:
        if(s == '('):
            parfreq['(']+=1
        elif(s == ')'):
            parfreq[')']+=1
   parcount = math.fabs(parfreq['(']-parfreq[')'])
   if(parcount == 0):
    return True
   else:
    return False
def eval(exp, aList):
    if atom(exp):
        if lisp_int(exp):
            return exp
        elif eq(exp, True):
            return True
        elif eq(exp, False):
            return False
        elif lisp_in(exp, aList):
            return getvalue(exp, aList)
        else:
            raise Exception("unbound variable!, ''%s''" % exp)
    elif atom(car(exp)):
       
        if eq(car(exp), "QUOTE"):                      
                return quote( car(cdr(exp)) )
        elif eq(car(exp), "COND"):
            return evcon(cdr(exp), aList)
        elif eq(car(exp), "DEFUN"):
            func = defun( 
                car(cdr(exp)), 
                car(cdr(cdr(exp))), 
                car( cdr(cdr(cdr(exp))) )
            )
            global functions
            functions = cons(func, functions)
            return func
        else:
            return apply(
                car(exp), 
                evlis(cdr(exp), aList), 
                aList
            )
    else:
        raise Exception("not able to evaluate:\n%s" % exp)
    
def apply(func, args, aList):
    if atom(func):
        if eq(func, "CAR"):
            return car(car(args))
        elif eq(func, "CDR"):
            return cdr(car(args))
        elif eq(func, "ATOM"):
            return atom(car(args))
        elif eq(func, "INT"):
            return lisp_int(car(args))
        elif eq(func, "NULL"):
            return null(car(args))
        elif eq(func, "CONS"):
            if cdr(args)[1] == False:
                return cons(car(args), cdr(args)[0])
            else:
                return cons(car(args), cdr(args))
        elif eq(func, "EQ"):
            return eq(car(args), car(cdr(args)))
        elif eq(func, "PLUS"):  
            return plus(car(args), car(cdr(args)))
        elif eq(func, "MINUS"):
            return minus(car(args), car(cdr(args)))
        elif eq(func, "TIMES"):
            return times(car(args), car(cdr(args)))
        elif eq(func, "QUOTIENT"):
            return quotient(car(args), car(cdr(args)))
        elif eq(func, "REMAINDER"): 
            return remainder(car(args), car(cdr(args)))
        elif eq(func, "LESS"):
            return less(car(args), car(cdr(args)))
        elif eq(func, "GREATER"):
            return greater(car(args), car(cdr(args)))
        else:
            body = cdr(getvalue(func, functions))
            params = car(getvalue(func, functions))
            alistnew = add_pairs( params, args, aList )
            return eval(body, alistnew)
    else:
        raise Exception("Non-atomic function name:\n%s" % func)
def evcon(be, aList):
    if null(be):
        raise Exception("Invalid conditional expression")
    elif eval(car(car(be)), aList):
        return eval(car(cdr(car(be))), aList)
    else:
        return evcon(cdr(be), aList)
def evlis(expList, aList):
    if null(expList):
        return False
    else:
        head = eval(car(expList), aList)       
        tail = evlis(cdr(expList), aList)
        return cons( head, tail )
def lisp_in(atom, aList):
    if null(aList):
        return False
    elif eq(atom, car(car(aList))):
        return True
    else:
        return lisp_in(atom, cdr(aList))
        
def getvalue(atom, aList):
    if null(aList):
        raise Exception("variable %s not in attribute list:\n%s" % (atom, aList))
    elif eq(atom, car(car(aList))):
        return cdr(car(aList))
    else:
        return getvalue(atom, cdr(aList))
def add_pairs(parameters, args, aList):
    if null(parameters):
        return aList
    else:
        return cons(
            cons( car(parameters), car(args) ),
            add_pairs( cdr(parameters), cdr(args), aList )
        )
def mainparser(expr):
    expr = expr.strip()    
    matches = re.match(r"^\(.*\)$", expr)
    if matches:
        dot, location = chkdot(expr)
        if dot:
            return parseExprWithDot(expr)
        else:
            return parseListExpr(expr)
    else:
        return tokenize(expr)
    
def chkdefun(exps):
    for loc, exp in enumerate(exps):
        if not atom(exp) and len(exp) > 0 and exp[0] == "DEFUN":
            eval(exp, False)
        else:
            return exps[loc:]
    
def getlispexpressions(inputexp):
    formExp = re.sub(r"[\s\n]+", " ", inputexp)
    lis = []
    lindx = formExp.index("(")
    while lindx != -1:
        depth = 0
        for loc, character in enumerate(formExp[lindx:]):
            if character == '(':
                depth += 1
            elif character == ')':
                depth -= 1
            if depth == 0:
                lis.append(formExp[lindx:lindx+loc+1])
                formExp = formExp[lindx+loc+1:]
                lindx = formExp.find("(")
                break
    lispex = [mainparser(exp) for exp in lis]
    return chkdefun(lispex)
       
def evaluateExpressions(inputexp): 
    if(type(getlispexpressions(inputexp)) == list or type(getlispexpressions(inputexp)) == tuple):
    	for exp in getlispexpressions(inputexp):
            yield eval(exp, False)
    else:
        raise Exception ("After defining a function use the function in the same line of input")
    
def goeval(inputexp):
    for result in evaluateExpressions(inputexp):
        print ">" + (dotnotation(result))

def output():
    strbuffer = ''
    print"Enter an expression: "
    while True:
        line = raw_input()
        if not line: break
        strbuffer += line
    goeval(strbuffer)
if __name__ == "__main__":
    
    while True:
        try:
            output()
            print "More?"
        except KeyboardInterrupt:
            break;
