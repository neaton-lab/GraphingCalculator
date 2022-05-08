import input
import renderFunction
import outputScreen

def main():
    xMin = 0
    xMax = 10
    xRes = 5
    read = input.Input('Enter the function: ')
    function = renderFunction.RenderFunction(read)
    output = function.render(xMin, xMax, xRes)
    outputScreen.xyplot(output[0], output[1])
    outputScreen.output(0, 0)

# execution
if __name__ == "__main__":
    main()