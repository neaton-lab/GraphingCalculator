import re

"""
RenderFunction holds the list of operations that need to be performed for the function (list of tuples, typically duples of operation and other argument)
Operations should all be either unary (for example trig functions) or communtitive (subtraction should be converted into addition)
"""
class RenderFunction:
    # Takes in a tokenized list or a string
    def __init__(self, function) -> None:
        pass

    # Complies the function sent into the __init__ into the stack-based format needed for render
    def __compile(self, function) -> None:
        for token in function:
            if token is ")":
                pass
            elif token is "(":
                pass
            elif token is "+":
                pass
            elif token is "-":
                pass
            elif token is "/":
                pass
            elif token is "%":
                pass
            elif token is "^" or token is "**":
                pass
            elif token is "sqrt":
                pass
            elif token is "log":
                pass
            elif token is "sin":
                pass
            elif token is "cos":
                pass
            elif token is "tan":
                pass
            elif re.match(r'^-?\d+(?:\.\d+)$', token) is not None:
                pass
            else:
                pass

    # Outputs a 2d list for input into matplotlib. The xMin and xMax parameters define the smallest and largest inputs, and xRes defines the amount of points that will be generated, default 20
    def render(self, xMin, xMax, xRes=20) -> list:
        step = (xMax - xMin) / xRes

    pass