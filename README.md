LispInterpreter
===============

Lisp Interpreter in Python




Design Document

The s-expression is implemented using the 'tuple' interface of python, so none of the internals are exposed. 

Breif description of the functions  for Part1 are as follows:

 dotnotation(expr):   This recursively generates the s-expression in dot notation

 ParseExprWithDot(expr):   This parses an expression with a dot returns a tuple with the parsed car and parsed cdr
 ParseListExpr(expr):  This parses an expression which is space separated list

 mainparser(expr):  This is the master function for parsing, it takes the expression checks for dots and appropriately passes it down to the other expression parser functions

 tokenize: returns token for the expression

for Part2:

primitive functions have been defined in primitives
 
the required functions such as eval, apply, evlis, evcon etc are as given in the Lisp Manual and course slides and implemented in the same way


Invalid expressions have been handled using regular expressions and using Exception handlers with messages


A few points to note

1. for an output expected in list form, the interpreter gives the output in dot notation
   e.g for input: (QUOTE(A))
		  > (A.NIL)   which corresponds to (A) in ist notation
   So for any output which is expected in list format e.g (1 2 3 4) it will be displayed as (1 . (2 . (3 . (4 . NIL))))

2 while using DEFUN to define functions, define it and compile it at the same time. I am not showing the name of the function as the output after defining a function.
  e.g for input: (DEFUN MINUS2 (A B) (MINUS A B)) (MINUS2 3 1)
                 > 2

      for input: (DEFUN MINUS2 (A B) (MINUS A B))
                 the output will raise an expection and will have a message saying the function has to be used in the same line.
		 I am sorry for this, but i was having some issues with null data after DEFUN, so had make it this way in the last minute.

      For two function definitions with the same name in one line of input, it takes ony the first function and ignores the second.
      

3 Regarding number of parameters in a Function. 
    a. If too many parameters are provided for a function, it just picks up as many arguments as it needs (1/2) and ignores the remaining.
    b. If the parameters are fewer than the required, then it throws an error.

 4. If two s-expressions are entered in one line. It will show the output for both if both are valid. If the first one is wrong it show an error and terminate. 
    If suppose three s-expressions are provided as input and the first two expressions are valid, and the third one is wrong, then the output will be shown for the first two, 
    and it will throw an error for the third one and terminate.

The interpreter asks you to enter an expression. The input expression can be entered in multiple lines, once the input has been entered, press [ENTER] key twice to get the output.
