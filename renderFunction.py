from outputScreen import outputScreen
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
    def __init__(self, func) -> None:
        self.y = 0
        self.exprStack = self.__compile().parseString(func, parseAll=True)
        self.variables = {}
        self.epsilon = 1e-12
        self.opn = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "^": operator.pow,
        }

        self.fn = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "exp": math.exp,
            "abs": abs,
            "trunc": int,
            "round": round,
            "sgn": lambda a: -1 if a < -self.epsilon else 1 if a > self.epsilon else 0,
            # functionsl with multiple arguments
            "multiply": lambda a, b: a * b,
            "hypot": math.hypot,
            # functions with a variable number of arguments
            "all": lambda *a: all(a),
        }

    # Complies the function sent into the __init__ into the stack-based format using pyparsing. Code adapted from pyparsing's example code
    def __compile(self) -> None:
        bnf = 0
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
                    (fn_call | pi | e | fnumber | ident).setParseAction(self.__pushFirst)
                    | Group(lpar + expr + rpar)
                )
            ).setParseAction(self.__pushUnaryMinus)

            # by defining exponentiation as "atom [ ^ factor ]..." instead of "atom [ ^ atom ]...", we get right-to-left
            # exponents, instead of left-to-right that is, 2^3^2 = 2^(3^2), not (2^3)^2.
            factor = Forward()
            factor <<= atom + (expop + factor).setParseAction(self.__pushFirst)[...]
            term = factor + (multop + factor).setParseAction(self.__pushFirst)[...]
            expr <<= term + (addop + term).setParseAction(self.__pushFirst)[...]
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

    def __evaluate_stack(self, s):
        op, num_args = s.pop(), 0
        if isinstance(op, tuple):
            op, num_args = op
        if op == "unary -":
            return -self.evaluate_stack(s)
        if op in "+-*/^":
            # note: operands are pushed onto the stack in reverse order
            op2 = self.evaluate_stack(s)
            op1 = self.evaluate_stack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            # note: args are pushed onto the stack in reverse order
            args = reversed([self.evaluate_stack(s) for _ in range(num_args)])
            return self.fn[op](*args)
        elif op[0].isalpha():
            self.variables.append(op)
        else:
            # try to evaluate as int first, then as float if int fails
            try:
                return int(op)
            except ValueError:
                return float(op)

    # Outputs a 2d list for input into matplotlib. The xMin and xMax parameters define the smallest and largest inputs, and xRes defines the amount of points that will be generated, default 20
    def render(self, xMin, xMax, xRes=20) -> list:
        step = (xMax - xMin) / xRes
        returnVal = []
        returnX = []
        returnY = []
        for x in range(xMin, xMax, step):
            returnX.append(x)
            # Calculate y values for each input value
            returnY.append(self.__interp(x, self.variables[0]))
        returnVal.append(returnX)
        returnVal.append(returnY)
        return returnVal

    def __interp(self, x, var):
        stk = self.exprStack.copy()
        for i in range(len(stk)):
            if (stk[i] == var):
                stk[i] = x
        val = 0
        while (len(stk) != 0):
            val += self.__evaluate_stack(stk)
        return val
    pass


