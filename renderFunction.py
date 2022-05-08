from pyparsing import (Literal, CaselessLiteral, CaselessKeyword, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf, Suppress, delimitedList, Regex)
import math
import operator

"""
RenderFunction holds the list of operations that need to be performed for the function (list of tuples, typically duples of operation and other argument)
Operations should all be either unary (for example trig functions) or communtitive (subtraction should be converted into addition)
"""
class RenderFunction:
    # Takes in a tokenized list or a string
    def __init__(self, function) -> None:
        self.y = 0
        self.exprStack = []
        self.variables = {}

    # Complies the function sent into the __init__ into the stack-based format using pyparsing. Code adapted from pyparsing's example code
    def __compile(self, function) -> None:
        global bnf
        if not bnf:
            # Defining common constants
            e = CaselessKeyword("E")
            pi = CaselessKeyword("PI")
            # Regex for testing for numerals
            fnumber = Regex(r"[+-]?\d+(?:\.\d*)?(?:[eE][+-]?\d+)?")
            ident = Word(alphas, alphas + nums + "_$")
            

            # Defining names for various operators
            plus, minus, mult, div = map(Literal, "+-*/")
            lpar, rpar = map(Suppress, "()")
            addop = plus | minus
            multop = mult | div
            expop = Literal("^")

            expr = Forward()
            expr_list = delimitedList(Group(expr))
            # add parse action that replaces the function identifier with a (name, number of args) tuple
            def insert_fn_argcount_tuple(t):
                fn = t.pop(0)
                num_args = len(t[0])
                t.insert(0, (fn, num_args))

            fn_call = (ident + lpar - Group(expr_list) + rpar).setParseAction(
                insert_fn_argcount_tuple
            )
            atom = (
                addop[...]
                + (
                    (fn_call | pi | e | fnumber | ident).setParseAction(self.pushFirst)
                    | Group(lpar + expr + rpar)
                )
            ).setParseAction(self.pushUnaryMinus)

            # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left
            # exponents, instead of left-to-right that is, 2^3^2 = 2^(3^2), not (2^3)^2.
            factor = Forward()
            factor <<= atom + (expop + factor).setParseAction(self.pushFirst)[...]
            term = factor + (multop + factor).setParseAction(self.pushFirst)[...]
            expr <<= term + (addop + term).setParseAction(self.pushFirst)[...]
            bnf = expr
        return bnf

    def __pushFirst(self, toks):
        self.exprStack.append(toks[0])
        
    def __pushUnaryMinus(self, toks):
        for t in toks:
            if t == "-":
                self.exprStack.append("unary -")
            else:
                break

    # Outputs a 2d list for input into matplotlib. The xMin and xMax parameters define the smallest and largest inputs, and xRes defines the amount of points that will be generated, default 20
    def render(self, xMin, xMax, xRes=20) -> list:
        step = (xMax - xMin) / xRes

    pass


