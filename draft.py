# $Smart Calculator
"""
stage 6/7
I decided to replace subtraction by adding negative value
implemented regex for parsing:
1) expression of type 'assignment ='
2) expressions with operators + -
"""
import logging
import re
from collections import deque


logging.basicConfig(filename='my_calc.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')
# logging.disable(10)

# logging.debug('DEBUG message')
# logging.info('INFO message')
# logging.warning('WARNING message')
# logging.error('ERROR message')
# logging.critical('CRITICAL message')


class InvalidIdentifierError(Exception):
    def __str__(self):
        return "Invalid identifier"


class InvalidAssignmentError(Exception):
    def __str__(self):
        return "Invalid assignment"


class Calculator:
    
    def __init__(self):
        """The initializer of the class.

        Arguments:
        variables: dict
        expression: string
        """
        # self.first = first
        # self.second = second
        # self.numbers = numbers
        self.variables = dict()
        self.expression = None
        self.postfix = ''
    
    
    def process_assignment(self, expr: str) -> dict:
        """Process expressions like 'a = 2' or 'a = b'"""
        logging.info('executing process_assignment(self, expr: str)...')
        logging.info("parse expression of type 'assignment ='")
        parse = re.match(r'^\s*(\w+)\s*=\s*(\w+)\s*$', expr)
        var, value = parse[1], parse[2]
        # var, value = expr.split('=')
        var = var.strip()  # var is str here
        logging.debug(f'var = {var}')
        value = value.strip()  # value is str here
        logging.debug(f'value= {value} ')
        try:
            if not var.isalpha():  # check left side if wrong variable' name
                logging.info('during assignment - check_identifier (left part)')
                logging.debug(f'not var.isalpha()? {not var.isalpha()}')
                raise InvalidIdentifierError
            elif (not value.isdigit()) and (value not in list(self.variables.keys())):
                logging.info('during assignment - check_right_part')
                logging.debug('right_part is not digit and is not stored variable')
                raise InvalidAssignmentError
            else:
                logging.info('during assignment - check_right_part')
                return {var: int(value)}
        except ValueError:
            if not value.isalpha():  # # check right side if wrong variable' name
                logging.info('raise InvalidAssignmentError')
                raise InvalidAssignmentError
            else:
                logging.info('success! return {var: other_var}')
                return {var: value}
    
    def assign(self, expr: str):
        logging.info('executing assign(self, expr: str)...')
        new_entry = self.process_assignment(expr)
        logging.debug(f'new_entry = {new_entry}')
        self.variables.update(new_entry)
        logging.debug(f'success! self.variables = {self.variables}')
    
    def return_value(self, expr_: str):
        """Expression like 'a' - variable name only.
        return value of this variable from dict or return value of other variable
        in case this variable's value is a reference to other variable."""
        logging.info('executing return_value(self, expr_: str)...')
        if not isinstance(self.variables[expr_], int):
            logging.info('return_value when {var: other_var}')
            other_key = self.variables[expr_]
            logging.debug({expr_: self.variables[expr_]}, {other_key: self.variables[other_key]})
            logging.debug(f'=> {expr_} = {self.variables[other_key]}')
            return self.variables[other_key]
        else:
            logging.info('return_value when {var: int}')
            logging.debug(f"self.variables[{expr_}]= {self.variables[expr_]}")
            return self.variables[expr_]
    
    def process_digits(self):
        """Change self.expression: digit str -> int"""
        logging.info('executing process_digits(self)...')
        logging.debug(self.expression)
        for i, char in enumerate(self.expression):
            try:
                if char.isdigit():
                    self.expression[i] = int(char)
            except AttributeError:
                continue
    
    def process_variables(self):
        """Change self.expression: digit str -> int"""
        logging.info('executing process_variables(self)...')
        logging.debug(self.expression)
        for i, char in enumerate(self.expression):
            if char.isalpha():
                self.expression[i] = self.return_value(char)
    
    def process_operators(self):
        """Change self.expression: remove '+', stick '-' to next value."""
        logging.info('executing process_operators(self)...')
        logging.debug(self.expression)
        for i, char in enumerate(self.expression):
            if char == '-':
                negative = -self.expression[i + 1]
                self.expression[i + 1] = negative
                del self.expression[i]
            elif char == '+' or char == '++':
                del self.expression[i]
    
    @staticmethod
    def process_plus(expr: str):
        expr_new = ''
        i = 0
        while i < len(expr):
            if expr[i] == '+':
                expr_new += '+'
                parse = re.match('["+"]+', expr[i:])
                if parse:
                    end_i = i + parse.end()
                    i = end_i
            else:
                expr_new += expr[i]
                i += 1
        return expr_new
    
    @staticmethod
    def process_minus(expr: str):
        expr_new = ''
        i = 0
        while i < len(expr):
            if expr[i] == '-':
                parse = re.match('[-]+', expr[i:])
                if parse:
                    if len(parse[0]) % 2 == 0:
                        expr_new += '+'
                    else:
                        expr_new += '-'
                    end_i = i + parse.end()
                    i = end_i
            else:
                expr_new += expr[i]
                i += 1
        return expr_new
    
    def add(self, expr: str) -> int:
        """Cast taken expr to list, save it in self.expression
        process(change) self.expression."""
        logging.info('executing add(self, expr: str)...')
        logging.debug(f'expr: {expr}')
        logging.info('process adjacent operators like -- or ---')
        expr = expr.replace(' ', '')
        expr = expr.replace('---', '-')
        expr = expr.replace('+++', '+')
        expr = expr.replace('--', '+')
        expr = expr.replace('++', '+')
        logging.debug(f'{expr}')
        # parse expressions with operators
        self.expression = re.findall(r'([\-+]|\w+|[^\s\w\-+]+)', expr)
        # self.expression = expr.split()
        logging.debug(f'self.expression = {self.expression}')
        self.process_variables()
        logging.debug(self.expression)
        self.process_digits()
        logging.debug(self.expression)
        self.process_operators()
        logging.debug(self.expression)
        return sum(self.expression)
   
    @staticmethod
    def help():
        print('The program knows two commands: /help, /exit.'
              'It supports variables(storing them in a dict), addition, and subtraction.')
    
    @staticmethod
    def polish_postfix_notation(expression_: str) -> list:
        priority = {'+': 0, '-': 0, '*': 1, '/': 1, }
        my_stack = deque()
        postfix_notation = []
        parse = re.findall(r'([\-+*/()]|\w+|[^\s\w\-+]+)', expression_)
        logging.debug(f'parse={parse}')
        try:
            for char in parse:
                # Add operands (numbers and variables) to the result (postfix notation)
                logging.debug(f"char: {char}")
                if char not in '/+-*()':  # char is operand
                    postfix_notation.append(char)
                    logging.debug(postfix_notation)
                else:  # char is operator or ()
                    if char == '(':  # 4
                        logging.info("# 4")
                        my_stack.append(char)
                        logging.debug(f" 49 {my_stack}")
                    elif char == ')':  # 5
                        logging.info("# 5")
                        while my_stack:
                            r = my_stack.pop()
                            logging.debug(f"r= {r}")
                            logging.debug(f"56 {my_stack}")
                            if r != '(':
                                postfix_notation.append(r)
                                logging.debug(f"{postfix_notation}")
                            else:
                                logging.info("break")
                                break
                    elif not my_stack or my_stack[-1] == '(':  # 1
                        logging.info("# 1")
                        my_stack.append(char)
                        logging.debug(f"66  {my_stack}")
                    elif priority[char] > priority[my_stack[-1]]:  # 2
                        logging.info("# 2")
                        my_stack.append(char)
                        logging.debug(f"70 {my_stack}")
                    elif priority[char] <= priority[my_stack[-1]]:
                        logging.info("# 3")
                        while my_stack:
                            r = my_stack[-1]
                            logging.debug(f"r= {r}")
                            if my_stack[-1] == '(' or priority[char] >= priority[r]:  # 3.1
                                logging.info("# 3.1")
                                logging.debug('break')
                                my_stack.pop()
                                break
                            else:  # 3.2
                                logging.info("# 3.2")
                                postfix_notation.append(r)
                                logging.debug(f'83 {postfix_notation}')
                                my_stack.pop()
                        my_stack.append(char)
                        logging.debug(f"87 {my_stack}")
            logging.debug(f'final stack in postfix: {my_stack}')
            while my_stack:  # 6
                logging.info("# 6")
                postfix_notation.append(my_stack.pop())
                logging.debug(postfix_notation)
            if my_stack:
                raise SyntaxError
            return postfix_notation
        except IndexError as err:
            logging.warning(err)
            print(err)
    
    
    def calculating_result(self, user_expr: str) -> int:
        logging.info('executing def calculating_result()...')
        my_stack = deque()
        self.expression = self.process_plus(user_expr)
        logging.debug(self.expression)
        self.expression = self.process_minus(self.expression)
        logging.debug(self.expression)
        expression_ = self.polish_postfix_notation(self.expression)  # list
        logging.debug(f"postfix notation: {expression_}")
        for element in expression_:
            if element.isdigit():
                my_stack.append(int(element))
                logging.debug(my_stack)
            elif element.isalpha():
                my_stack.append(self.return_value(element))
                logging.debug(my_stack)
            else:
                logging.debug(f'operator = {element}')
                first = my_stack.pop()
                second = my_stack.pop()
                logging.debug(f'{second} {element} {first}')
                my_stack.append(eval(f'{second} {element} {first}'))
                logging.debug(my_stack)
        logging.debug(f'calculating_result: {my_stack[-1]}')
        return my_stack[-1]


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
    collection4 = ('n = 2', 'n = 3', 'n', 'a  =   5', 'b = a', 'b', 'a = 8', 'b = c', 'a1 = 8',
                   'n1 = a2a', 'n = a2a', 'a = 7 = 8', 'a2a', 'e', 'a=1', 'a', '1 + 2 - 3',
                   'b - c + 4 - a', '1 ++ 2 -- 3 --- 4')
    new = Calculator()
    logging.info('new = Calculator()')
    while True:
        user_input = input()
        logging.debug(f'user_input: {user_input}')
    # for expr_ in collection4:
    #     user_input = expr_
    #     logging.debug(f'user_input: {user_input}')
        if user_input in (' ', ''):  # empty line is ignored
            logging.info('empty line is ignored')
            main()
        elif user_input == '/exit':
            logging.info("user_input == '/exit'")
            terminate()
        elif user_input == '/help':
            logging.info("user_input == '/help'")
            Calculator.help()
            continue
        try:
            logging.info('try:')
            if user_input.count('=') > 1:
                logging.info("assignment: check for multiple '='")
                raise InvalidAssignmentError
            elif '=' in user_input:
                logging.info("detected assignment =")
                Calculator.assign(new, user_input)
            # elif '+' in user_input or '-' in user_input:
            #     logging.info("calculations of different expressions")
            #     print(Calculator.add(new, user_input))
            # if it's variable name
            elif any([operator in user_input for operator in '+-/*']):
                logging.info("calculations of different expressions")
                print(Calculator.calculating_result(new, user_input))
            else:
                logging.info('ELSE')
                if user_input[0] == '/':
                    logging.debug("user_input[0] == '/..'\nmessage: Unknown command")
                    print('Unknown command')
                    main()
                elif not user_input.isalpha():  # bad variable name -> True
                    logging.info('call variable: check_identifier')
                    raise InvalidIdentifierError
                else:
                    logging.info('call variable: check_if_variable_stored')
                    print(Calculator.return_value(new, user_input))
        except InvalidIdentifierError as err:
            print(err)
            continue
        except InvalidAssignmentError as err:
            print(err)
            continue
        except KeyError as err:
            logging.debug('check_if_variable_stored: False')
            logging.warning(err)
            print('Unknown variable')
            continue
        except NameError as err:
            logging.warning(err)
            print('Invalid expression')
            main()
        except SyntaxError as err:
            logging.warning(err)
            print('Invalid expression')
            main()


if __name__ == '__main__':
    main()
