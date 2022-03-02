# $Smart Calculator
"""
multiplication, division, addition, and subtraction
+ the ability to calculate expressions containing parenthesis
+ the ability to remember the previous result
stage 1/7
Write a program that reads two integer numbers from the same line
and prints their sum in the standard output. Numbers can be positive, negative, or zero.
stage 2/7
program that reads two numbers in a loop and prints the sum in the standard output.
If a user enters only a single number, the program should print the same number.
If a user enters an empty line, the program should ignore it.
When the command /exit is entered, the program must print "Bye!" and then stop.
stage 3/7
Add to the calculator the ability to read an unlimited sequence of numbers.
Add a /help command to print some information about the program.
stage 4/7
the program must receive the addition + and subtraction - operators as an input
It must support both unary and binary minus operators
If the user has entered several same operators following each other,
the program still should work (like Java or Python REPL).
9 +++ 10 -- 8
3 --- 5
14        -  12
two adjacent minus signs turn into a plus.
/help command: maintain its relevance depending on the changes (in the next stages too).
stage 5/7
The program only knows numbers, a plus sign, a minus sign, and two commands.
It cannot accept all other characters
"""


class Calculator:
    
    def __init__(self, numbers):
        """The initializer of the class.

        Arguments:
        numbers: tuple of integers
        """
        # self.first = first
        # self.second = second
        self.numbers = numbers
    
    def add(self):
        """ Addition """
        return sum(self.numbers)
    

def terminate():
    print('Bye!')
    exit()


def main():
    while True:
        user_input = input()
        if user_input in (' ', ''):
            main()
        try:
            print(eval(user_input))
        except NameError:
            print('Invalid expression')
            main()
        except SyntaxError:
            if user_input == '/exit':
                terminate()
            elif user_input == '/help':
                print('The program only knows numbers, a plus sign, a minus sign, and two commands:'
                      '/help, /exit. It cannot accept any other characters.')
                main()
            elif user_input[0] == '/':
                print('Unknown command')
                main()
            elif user_input in (' ', ''):
                main()
            else:
                print('Invalid expression')
                main()


if __name__ == '__main__':
    main()
