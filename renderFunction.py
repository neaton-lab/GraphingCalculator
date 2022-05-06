
"""
RenderFunction holds the list of operations that need to be performed for the function (list of tuples, typically duples of operation and other argument)
Operations should all be either unary (for example trig functions) or communtitive (subtraction should be converted into addition)
"""
class RenderFunction:
    # Takes in a tokenized list or a string
    def __init__(self, function) -> None:
        pass

    # Complies the function sent into the __init__ into the stack-based format needed for render
    def __compile(self) -> None:
        pass

    # Outputs a 2d list for input into matplotlib
    def render(self) -> list:
        pass
    pass