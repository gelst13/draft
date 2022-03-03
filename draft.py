# $Smart Calculator
"""
stage 6/7
I decided to replace subtraction by adding negative value
"""
import logging

logging.basicConfig(filename='my_calc.log', level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')


logging.disable(10)

# logging.debug('DEBUG message')
# logging.info('INFO message')
# logging.warning('WARNING message')
# logging.error('ERROR message')
# logging.critical('CRITICAL message')


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
        self.expression = list()
    
    def process_assignment(self, expr: str) -> dict:
        """Process expressions like 'a = 2' or 'a = b'"""
        var, value = expr.split('=')
        var = var.strip()  # var is str here
        # logging.debug(f'len {var} = {len(var)}')
        value = value.strip()  # value is str here
        # logging.debug(f'len {value} = {len(value)}')
        try:
            if not var.isalpha():  # check left side if wrong variable' name
                raise InvalidIdentifierError
            elif (not value.isdigit()) and (value not in list(self.variables.keys())):
                raise InvalidAssignmentError
            else:
                return {var: int(value)}
        except ValueError:
            if not value.isalpha():  # # check right side if wrong variable' name
                raise InvalidAssignmentError
            else:
                return {var: value}
    
    def assign(self, expr: str):
        new_entry = Calculator.process_assignment(self, expr)
        logging.debug(f'new_entry = {new_entry}')
        self.variables.update(new_entry)
        logging.debug(f'self.variables = {self.variables}')
    
    def return_value(self, expr_: str):
        """Expression like 'a' - variable name only.
        return value of this variable from dict or return value of other variable
        in case this variable's value is a reference to other variable."""
        logging.debug('start executing return_value(self, expr_: str)')
        if not isinstance(self.variables[expr_], int):
            logging.debug(not isinstance(self.variables[expr_], int))
            other_key = self.variables[expr_]
            logging.debug({expr_: self.variables[expr_]}, {other_key: self.variables[other_key]})
            return self.variables[other_key]
        else:
            logging.debug(f"self.variables[{expr_}] {self.variables[expr_]}")
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
            elif char == '+' or char == '++':
                del self.expression[i]
    
    def add(self, expr: str) -> int:
        """Cast taken expr to list, save it in self.expression
        process(change) self.expression."""
        expr = expr.replace('---', '-')
        expr = expr.replace('--', '+')
        self.expression = expr.split()
        Calculator.process_variables(self)
        logging.debug(self.expression)
        Calculator.process_digits(self)
        logging.debug(self.expression)
        Calculator.process_operators(self)
        logging.debug(self.expression)
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
    # collection3 = ('a = 9', 'b=2', 'c = 1', 'a + b', 'b - a', 'b + c', 'b - c',
    #                'a -- b - c + 3 --- a ++ 1')
    new = Calculator()
    while True:
        user_input = input()
        logging.debug(f'expression: {user_input}')
        # for expr_ in collection3:
        #     user_input = expr_
        #     logging.debug(f'expression: {user_input}')
        if user_input in (' ', ''):  # empty line is ignored
            logging.info("if user_input in (' ', '')")
            main()
        elif user_input == '/exit':
            logging.info("elif user_input == '/exit'")
            terminate()
        elif user_input == '/help':
            logging.info("elif user_input == '/help'")
            Calculator.help()
            continue
        try:
            # user_input = expr_
            # logging.debug(f'expression: {user_input}')
            logging.info('TRY:')
            if user_input.count('=') > 1:
                raise InvalidAssignmentError
            elif '=' in user_input:
                logging.info("if '=' in user_input ")
                Calculator.assign(new, user_input)
            
            elif '+' in user_input or '-' in user_input:
                logging.info("elif '+' in user_input or '-' in user_input")
                print(Calculator.add(new, user_input))
            # if it's variable name
            else:
                logging.info('ELSE')
                if user_input[0] == '/':
                    logging.debug("user_input[0] == '/'\nmessage: Unknown command")
                    print('Unknown command')
                    main()
                elif not user_input.isalpha():  # bad variable name
                    raise InvalidIdentifierError
                else:
                    logging.info('call Calculator.return_value(new, user_input)')
                    print(Calculator.return_value(new, user_input))
        except InvalidIdentifierError as err:
            print(err)
            continue
        except InvalidAssignmentError as err:
            print(err)
            continue
        except KeyError as err:
            logging.warning(err)
            print('Unknown variable')
            continue
        except NameError as err:
            logging.warning(err)
            print('Invalid expression')
            main()
        except SyntaxError as err:
            logging.warning(err)
            # if user_input[0] == '/':
            #     print('Unknown command')
            #     main()
            # else:
            print('Invalid expression')
            main()


if __name__ == '__main__':
    main()
