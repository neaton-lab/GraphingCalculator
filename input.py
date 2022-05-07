# Carly Middleton
# receives user input including functions

class Input:
     def __init__(self, fx):
        self.fx = fx

     @classmethod
     def get_user_input(self):
         while 1:
             try:
                 self.fx = input('Please enter function: ')
                 self.fx = lambda x: eval(self.fx)
                 #print('Function entered:', self.fx)
                 return self(self.fx)

             except:
                 print('Invalid input. Please enter a function.')
                 continue       
#func = Input.get_user_input()
