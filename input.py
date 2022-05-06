# Carly Middleton
# basic user input file for x value 

class Input:

     def __init__(self, x):
         self.x = x

     @classmethod
     def get_user_input(self):

         while 1:
             try:
                 self.x = input('Enter x value: ')
                 self.x = float(self.x)
                 #print('x val entered:', self.x)
                 return self(self.x)

             except:
                 print('Invalid input. Please enter a number.')
                 continue       

#     def pass_to_render(self):
     
#             self.x = Input.get_user_input()
#xVal = Input.get_user_input()