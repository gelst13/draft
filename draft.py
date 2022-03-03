# $Smart Calculator
"""
stage 6/7
I decided to replace subtraction by adding negative value
"""


class InvalidIdentifierError(Exception):
    def __str__(self):
        return "Invalid identifier!"


class InvalidAssignmentError(Exception):
    def __str__(self):
        return "Invalid assignment"


class Calculator:
    
    def __init__(self):
        """The initializer of the class.

        Arguments:
        expression: string
        """
        # self.first = first
        # self.second = second
        # self.numbers = numbers
        self.variables = dict()
        self.expression = None
    
    
    @staticmethod
    def store_variable_value(expr: str) -> dict:
        """Process expressions like 'a = 2' or 'a = b'"""
        var, value = expr.split('=')
        var = var.strip()  # var is str here
        value = value.strip()  # value is str here
        try:
            if not var.isalpha():  # wrong variable' name: must contain only Latin letters
                raise InvalidIdentifierError
            else:
                return {var: int(value)}
        except ValueError:
            if not value.isalpha():  # bad reference: variable' name must be of Latin letters
                raise InvalidAssignmentError
            else:
                return {var: value}
    
    def assign(self, expr: str):
        new_entry = Calculator.store_variable_value(expr)
        self.variables.update(new_entry)

    def return_value(self, expr_: str):
        """Expression like 'a' - variable name only.
        return value of this variable from dict or return value of other variable
        in case this variable's value is a reference to other variable."""
        if not isinstance(self.variables[expr_], int):
            other_key = self.variables[expr_]
            print({expr_: self.variables[expr_]}, {other_key: self.variables[other_key]})
            return self.variables[other_key]
        else:
            return self.variables[expr_]

    def process_digits(self):
        """Change self.expression: digit str -> int"""
        for i, char in enumerate(self.expression):
            try:
                if char.isdigit():
                    self.expression[i] = int(char)
            except AttributeError:
                continue

    def process_variables(self):
        """Change self.expression: digit str -> int"""
        for i, char in enumerate(self.expression):
            if char.isalpha():
                self.expression[i] = Calculator.return_value(self, char)

    def process_operators(self):
        """Change self.expression: remove '+', stick '-' to next value."""
        for i, char in enumerate(self.expression):
            if char == '-':
                negative = -self.expression[i + 1]
                self.expression[i + 1] = negative
                del self.expression[i]
            elif char == '+':
                del self.expression[i]

    def add(self, expr: str) -> int:
        """Save taken expr to self.expression and process(change) self.expression."""
        self.expression = expr.split()
        Calculator.process_variables(self)
        # print(self.expression)
        Calculator.process_digits(self)
        # print(self.expression)
        Calculator.process_operators(self)
        # print(self.expression)
        return sum(self.expression)
    
    
    
    
    @staticmethod
    def help():
        print('The program knows two commands: /help, /exit.'
              'It supports variables(storing them in a dict), addition, and subtraction.')


def terminate():
    print('Bye!')
    exit()


def main():
    # collection = ('a', 'n = 33', 'm=4', 'a  =   5', 'b = n', 'b', 'v=   7', 'n =9', 'count = 10',
    #               'a2 = 1', 'a = 2', 'a = 3', 'a', 'a2a', 'n22', 'n = a2a',
    #               '2  + 3  -  a',)
    # collection1 = ('a  =  3', 'b= 4', 'c =5', 'a + b - c', 'b - c + 4 - a', 'a = 800',
    #                'a + b + c', 'BIG = 9000', 'BIG', 'big', '/exit',)
    # new = Calculator()
    while True:
        new = Calculator()
        user_input = input()
    # for expr_ in collection1:
        # user_input = expr_
        if user_input in (' ', ''):  # empty line is ignored
            main()
        elif user_input == '/exit':
            terminate()
        elif user_input == '/help':
            Calculator.help()
            continue
        try:
            # user_input = expr_
            print(f'expression: {user_input}')
            if '=' in user_input:
                Calculator.assign(new, user_input)
                # print(f'new.variables = {new.variables}')
            elif '+' in user_input or '-' in user_input:
                print(Calculator.add(new, user_input))
            # if it's variable name
            else:
                if not user_input.isalpha():  # bad variable name
                    raise InvalidIdentifierError
                else:
                    print(Calculator.return_value(new, user_input))
        except InvalidIdentifierError as err:
            print(err)
            continue
        except InvalidAssignmentError as err:
            print(err)
            continue
        except KeyError:
            print('Unknown variable')
            continue
        except NameError:
            print('Invalid expression')
            main()
        except SyntaxError:
            if user_input[0] == '/':
                print('Unknown command')
                main()
            else:
                print('Invalid expression')
                main()
    print(new.variables)


if __name__ == '__main__':
    main()
