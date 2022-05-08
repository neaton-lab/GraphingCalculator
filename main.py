import input
import renderFunction
import outputScreen

def main():
    read = input.Input()
    function = renderFunction.RenderFunction(read)
    output = function.render(0, 10, 5)
    outputScreen.xyplot(output[0], output[1])
    outputScreen.output(0, 0)

# execution
if __name__ == "__main__":
    main()