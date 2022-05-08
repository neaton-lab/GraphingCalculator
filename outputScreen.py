# Brandon Sharp
# This file plots and outputs the x and y data onto the screen
# uses data from other files
import networkx as nx
import math
import matplotlib.pyplot as plt

class outputScreen:

    def xyplot(x, y):
        plt.plot(x, y) # plots the points for each x and y value
    def output(x, y):
        plt.show() # outputs the graph


# x = [1, 2, 3, 4, 5] # testing
# y = x # testing
# outputScreen.xyplot(x, y) # testing
# outputScreen.output(x, y) # testing
