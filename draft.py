# !/usr/bin/python
# -*- coding: utf-8
# $Static Code Analyzer
import ast
import logging
import os
import re
import string
import sys
from pprint import pprint

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')

# logging.disable(20)

# os.chdir(r'C:\Users\Тоша\PycharmProjects\Static Code Analyzer\Static Code Analyzer\task')
# os.chdir(r'C:\Users\Тоша\PycharmProjects\FirstProject')

target = sys.argv[1]
logging.debug(target)


class StaticCodeAnalyzer:
    
    def __init__(self, _target: str):
        self.target = _target
        self.mistakes = dict()  # {'line' : [errors]}
        self.messages = {'S001': 'T00 long',
                         'S002': 'Indentation is not a multiple of four',
                         'S003': 'Unnecessary semicolon after a statement',
                         'S004': 'Less than two spaces before inline comments',
                         'S005': 'TODO found',
                         'S006': 'More than two blank lines preceding a code line',
                         'S007': "Too many spaces after \"$name\"",
                         'S008': 'Class name class_name should be written in CamelCase',
                         'S009': 'Function name function_name should be written in snake_case',
                         'S010': 'Argument name \"$name\" should be written in snake_case',
                         'S011': 'Variable \"$name\" should be written in snake_case',
                         'S012': 'The default argument value is mutable',
                         }
    
    def get_abs_names(self) -> list:
        """Walking a directory tree and printing the names of the directories and files"""
        logging.debug('get_abs_names...')
        abs_names = []
        for dirpath, dirnames, files_ in os.walk(self.target, topdown=True):
            logging.debug(dirpath)
            for file_name in files_:
                if file_name.endswith('.py'):
                    logging.debug((dirpath, '\\' + file_name))
                    abs_names.append(os.path.join(dirpath, file_name))
        return abs_names
    
    @staticmethod
    def check_s001(text):
        """check_length"""
        if len(text) > 79:
            return 'T00 long'
    
    @staticmethod
    def check_s002(expr: str):
        """Check if Indentation is a multiple of 4."""
        if expr.startswith(' '):
            parse = re.match(r'\ +', expr)
            return 'Ok' if len(parse.group()) % 4 == 0 else 'Not Ok'
    
    @staticmethod
    def check_s003(expr: str):
        """check_semicolon"""
        # logging.info('check_s003...')
        if expr.startswith('#'):
            return False
        elif expr.find(';'):
            # logging.debug(f'expr: {expr}')
            # case with inline comment expr = 'pass; # comment;'
            parse = re.match(r'([\S\D]+)(#[\S\D]+)', expr)  # match='pass; # comment;
            # logging.debug(f'parse= {parse}')
            if parse:
                statement = parse.group(1).strip()
            # case without inline comment
            else:
                statement = expr.strip()
            # logging.debug(f'statement= {statement}')
            # logging.debug(statement.endswith(';'))
            return statement.endswith(';')
    
    @staticmethod
    def check_s004(expr: str):
        """check_inline_comment
        Return True if there are less than 2 spaces between statement and # """
        # logging.debug('check_s004...')
        # logging.debug(expr)
        if expr.find('#') > 0:
            # logging.debug(expr.find('#'))
            comment_start = expr.index('#')
            # logging.debug(expr.index('#'))
            return expr[comment_start - 2:comment_start:1] != '  '
        else:
            return None
    
    @staticmethod
    def check_s005(expr: str):
        """check_todo"""
        # logging.info('check_s005')
        if expr.startswith('#'):
            # logging.debug(f'expr: {expr}')
            parse = re.match(r'#.?[tT][Oo][Dd][Oo]', expr)
            # logging.debug(f'parse: {parse}')
            if parse:
                return True
        elif expr.find('#'):
            # logging.debug(f'expr: {expr}')
            parse = re.findall(r'# ?[tT][Oo][Dd][Oo]', expr)
            # logging.debug(f'parse: {parse}')
            if parse:
                return True
    
    @staticmethod
    def check_s007(expr: str):
        """1 space between the construction name and the object name"""
        search_construction = re.findall('(class |def )', expr, flags=re.I)
        if search_construction:
            # logging.info(search_construction)
            s007 = re.search(r'(class|def) [^\s]+', expr, flags=re.I)
            if not s007:
                # logging.debug(line)
                return search_construction[0].strip()
    
    @staticmethod
    def check_s008(expr):
        search_class = re.findall('(class )', expr, flags=re.I)
        if search_class:
            logging.info('def check_s008')
            s008 = re.search(r'(class)[\s]+([A-Z][a-zA-z0-9]+)(:|\()', expr)
            logging.debug(f's009: {s008}')
            return bool(s008)
        else:
            return 'Not a class'
    
    @staticmethod
    def check_s009(expr: str):
        """Function name function_name should be written in snake_case"""
        search_def = re.findall('(def )', expr, flags=re.I)
        if search_def:
            s009 = re.search(r'(def)[\s]+([-a-z_]+)\(', expr)
            logging.info('def check_s009...')
            logging.debug(f's009: {s009}')
            return bool(s009)
        else:
            return 'Not a function'
    
    @staticmethod
    def check_snake_case(expr: str):
        """Test if variable/argument name is written in snake_case"""
        logging.info('check_snake_case...')
        check_ = re.match(r'([a-z_][a-z0-9_]+)$', expr)
        logging.debug(f'check_: {check_}')
        return bool(check_)
    
    @staticmethod
    def check_immutability(tested_obj):
        """Check type of tested_obj.
        Return True if tested_obj is hashable and -> immutable"""
        # Constants are immutable.
        # Immutable containers (like tuples) are hashable if their elements are hashable
        # and -> immutable
        # frozensets are immutable and hashable.
        logging.info('check_immutability ...')
        logging.debug(type(tested_obj))
        if isinstance(tested_obj, ast.Tuple):
            if hash(tested_obj.elts):
                logging.debug('tested_obj is immutable and hashable')
                return True
        elif isinstance(tested_obj, ast.Constant):
            logging.debug('tested_obj is immutable and hashable')
            return True
    
    def check_ast_nodes(self, filename):
        """find ast.FunctionDef node and analyze that node: make 3 checks"""
        logging.info('check_ast_nodes...')
        logging.debug(f'filename: {filename}')
        with open(filename, 'r', encoding='utf-8') as file:
            code = file.read()
            try:
                tree = ast.parse(code)
                # lines = [None] + code.splitlines()  # None at [0] so we can index lines from 1
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        logging.info('node: ast.FunctionDef')
                        function_node = node
                        self.mistakes[function_node.lineno] = set()
                        function_name = node.name
                        logging.debug(f'function_name: {function_name}')
                        # check for error S010
                        function_args = [a.arg for a in function_node.args.args]
                        logging.debug(f'function_args: {function_args}')
                        for arg in function_args:
                            if not self.check_snake_case(arg):
                                self.mistakes[function_node.lineno].add(('S010', arg))
                        # check for error S011
                        logging.info(f'FunctionDef {function_name}: ast.Assign')
                        for obj in function_node.body:
                            if isinstance(obj, ast.Assign):
                                self.mistakes[obj.lineno] = set()
                                var_name = [name.id for name in obj.targets][0]
                                logging.debug(var_name)
                                if not self.check_snake_case(var_name):
                                    self.mistakes[obj.lineno].add(('S011', var_name))
                        # check for error S012
                        function_args_defaults = [d for d in function_node.args.defaults]
                        logging.debug(f'args_default: {function_args_defaults}')
                        for default_value in function_args_defaults:
                            if not self.check_immutability(default_value):
                                self.mistakes[function_node.lineno].add(('S012', ))
            except IndentationError as err:
                logging.error(err)
            except SyntaxError as err:
                logging.error(err)
    
    
    def check_file(self, filename):
        logging.info('check_file...')
        logging.debug(f'filename: {filename}')
        with open(filename, 'r', encoding='utf-8') as file:
            empty_line_count = 0
            for number, line in enumerate(file):
                # try:
                if (number + 1) not in self.mistakes.keys():
                    self.mistakes[number + 1] = set()
                # self.mistakes[number + 1] = []
                if self.check_s001(line):
                    self.mistakes[number + 1].add(('S001', ))
                if self.check_s002(line) == 'Not Ok':
                    self.mistakes[number + 1].add(('S002', ))
                if self.check_s003(line):
                    self.mistakes[number + 1].add(('S003', ))
                if self.check_s004(line):
                    self.mistakes[number + 1].add(('S004', ))
                if self.check_s005(line):
                    self.mistakes[number + 1].add(('S005', ))
                if self.check_s007(line):
                    self.mistakes[number + 1].add(('S007', self.check_s007(line)))
                if not self.check_s008(line):
                    self.mistakes[number + 1].add(('S008', ))
                if not self.check_s009(line):
                    self.mistakes[number + 1].add(('S009', ))
                # check_s006
                if line == '\n':
                    # logging.warning(r"line == '\n'")
                    empty_line_count += 1
                    # logging.warning(f'empty_line_count: {empty_line_count}')
                else:
                    if empty_line_count > 2:
                        # logging.warning(f'empty_line_count: {empty_line_count}')
                        self.mistakes[number + 1].add(('S006', ))
                    empty_line_count = 0
                    # logging.warning(f'empty_line_count: {empty_line_count}')
                    # except KeyError as err:
                    #     logging.warning(err)
                    #     self.mistakes[number + 1] = set()
                    #     continue
    
    def process_result(self):
        new_m = dict()
        for key, value in self.mistakes.items():
            if value:
                # new_m[key] = sorted(list(set(value)))
                new_m[key] = sorted(list(value))
        logging.debug(new_m)
        return new_m
    
    def print_sorted_results(self, file_):
        """File: Line X: Code Message"""
        logging.info("print_sorted_results")
        for lineno in sorted(self.mistakes.keys()):
            for error in self.mistakes[lineno]:
                if len(error) == 2:
                    logging.info('len(error) == 2:')
                    logging.debug(f'{file_}: Line {lineno}: {error}')
                    template = string.Template(self.messages[error[0]])
                    logging.debug(self.messages[error[0]])
                    logging.debug(template)
                    msg = template.substitute(name=error[1])
                    logging.info('template.substitute(name=error[1])')
                    logging.debug(f'msg: {msg}')
                    print(f'{file_}: Line {lineno}: {error[0]} {msg}')
                else:
                    print(f'{file_}: Line {lineno}: {error[0]} {self.messages[error[0]]}')
                    

    def start(self) -> None:
        # PREPARATION
        if self.target.endswith('.py'):
            logging.info('case 1')
            files = [self.target, ]
        else:
            logging.info('case 2')  # directory
            files = self.get_abs_names()
        logging.debug(f'files: {files}')
        # ANALYZING
        logging.info('ANALYZING')
        for file in sorted(files):
            # logging.debug(file)
            self.check_file(file)
            self.check_ast_nodes(file)
            self.mistakes = self.process_result()
            # pprint(self.mistakes)
            self.print_sorted_results(file)
            self.mistakes = dict()


# TESTING input
# input_path = 'test\test_1.py'
# input_path = r'C:\Users\Тоша\PycharmProjects\FirstProject\test'
# input_path = '\test'
# input_path = '\task'
# target = input_path
logging.info('START')
# logging.debug(f'input: {input_path}')

target = target.replace('\t', '\\t')
target = target.replace('\a', '\\a')
logging.debug(f'target: {target}')

new = StaticCodeAnalyzer(target)

if __name__ == '__main__':
    new.start()
