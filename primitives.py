#!/usr/bin/env python

#-------------------------------------------------------------
# Name:       primitives.py
# Purpose:    Course Project
# Author:     Aveek Mukhopadhyay
# Created:    03/22/2013
#-------------------------------------------------------------
# primitives functions are defined here
   
def car(exp):
    return exp[0]

def cdr(exp):
    return exp[1]

def cons(exp1, exp2):
    return (exp1, exp2)

def atom(exp):
    return not isinstance(exp, tuple)
    
def eq(exp1, exp2):
    if not atom(exp1):
        raise ValueError("This function needs its first parameter as an atom. \n%s was supplied" % str(exp1))
    if not atom(exp1):
        raise ValueError("This function needs its second parameter as an atom. \n%s was supplied" % str(exp1))
    if exp1 == exp2:
        return True
    else:
        return False

def null(exp):
    return isinstance(exp, bool) and exp == False
    
def lisp_int(exp):
    return not isinstance(exp, bool) and (isinstance(exp, int))

def plus(val1, val2):
    return val1 + val2
    
def minus(val1, val2):
    return val1 - val2

def times(val1, val2):
    return val1 * val2
    
def quotient(val1, val2):
    return int(val1 / val2)

def remainder(val1, val2):
    return val1 - times(val2, quotient(val1, val2))


def less(val1, val2):
    if(val1<val2):
        return True

    
def greater(val1, val2):
    if(val1<val2):
        return True
    
def quote(exp):
    return  exp

def defun(name, parameters, body):
    return cons( name, cons(parameters, body) )
