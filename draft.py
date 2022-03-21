# !/usr/bin/python
# -*- coding: utf-8
# $Static Code Analyzer
import logging
import os
import re
import sys

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')

logging.disable(20)

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
                         'S007': "Too many spaces after ' '",
                         'S008': 'Class name class_name should be written in CamelCase',
                         'S009': 'Function name function_name should be written in snake_case',
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
    
    def check_file(self, filename):
        logging.info('check_file...')
        logging.debug(f'filename: {filename}')
        with open(filename, 'r', encoding='utf-8') as file:
            empty_line_count = 0
            for number, line in enumerate(file):
                self.mistakes[number + 1] = []
                if self.check_s001(line):
                    self.mistakes[number + 1].append('S001')
                if self.check_s002(line) == 'Not Ok':
                    self.mistakes[number + 1].append('S002')
                if self.check_s003(line):
                    # logging.debug(number + 1)
                    self.mistakes[number + 1].append('S003')
                if self.check_s004(line):
                    self.mistakes[number + 1].append('S004')
                if self.check_s005(line):
                    self.mistakes[number + 1].append('S005')
                if self.check_s007(line):
                    self.mistakes[number + 1].append(('S007', self.check_s007(line)))
                if not self.check_s008(line):
                    self.mistakes[number + 1].append('S008')
                if not self.check_s009(line):
                    self.mistakes[number + 1].append('S009')
                # check_s006
                if line == '\n':
                    # logging.warning(r"line == '\n'")
                    empty_line_count += 1
                    # logging.warning(f'empty_line_count: {empty_line_count}')
                else:
                    if empty_line_count > 2:
                        # logging.warning(f'empty_line_count: {empty_line_count}')
                        self.mistakes[number + 1].append('S006')
                    empty_line_count = 0
                    # logging.warning(f'empty_line_count: {empty_line_count}')
    
    def process_result(self):
        new_m = dict()
        for key, value in self.mistakes.items():
            if value:
                new_m[key] = sorted(list(set(value)))
        return new_m
    
    def print_sorted_results(self, file_):
        """Line X: Code Message"""
        for lineno in sorted(self.mistakes.keys()):
            for error in self.mistakes[lineno]:
                if error[0] == 'S007':
                    message = f"Too many spaces after '{error[1]}'"
                    print(f'{file_}: Line {lineno}: {error[0]} {message}')
                else:
                    print(f'{file_}: Line {lineno}: {error} {self.messages[error]}')
    
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
            self.process_result()
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
