#!/usr/bin/python
# -*- coding: utf-8
import logging
from pprint import pprint
import re


logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')
logging.disable(10)


def check_length(text):
    if len(text) > 79:
        return 'T00 long'


def check_indentation(expr: str):
    """Check if Indentation is a multiple of 4."""
    if expr.startswith(' '):
        parse = re.match(r'\ +', expr)
        return 'Ok' if len(parse.group()) % 4 == 0 else 'Not Ok'


def check_semicolon(expr: str):
    # logging.info('check_semicolon...')
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


def check_inline_comment(expr: str):
    """Return True if there are less than 2 spaces between statement and # """
    # logging.debug('check_inline_comment...')
    # logging.debug(expr)
    if expr.find('#') > 0:
        # logging.debug(expr.find('#'))
        comment_start = expr.index('#')
        # logging.debug(expr.index('#'))
        return expr[comment_start - 2:comment_start:1] != '  '
    else:
        return None


def check_todo(expr: str):
    """Check if Less than 2 spaces before inline comments."""
    logging.info('check_todo')
    if expr.startswith('#'):
        logging.debug(f'expr: {expr}')
        parse = re.match(r'#.?[tT][Oo][Dd][Oo]', expr)
        logging.debug(f'parse: {parse}')
        if parse:
            return True
    elif expr.find('#'):
        logging.debug(f'expr: {expr}')
        parse = re.findall(r'# ?[tT][Oo][Dd][Oo]', expr)
        logging.debug(f'parse: {parse}')
        if parse:
            return True


messages = {'S001': 'T00 long',
            'S002': 'Indentation is not a multiple of four',
            'S003': 'Unnecessary semicolon after a statement',
            'S004': 'Less than two spaces before inline comments',
            'S005': 'TODO found',
            'S006': 'More than two blank lines preceding a code line',
            }
mistakes = dict()  # {'line' : [errors]}


# filename = r'C:\Users\Тоша\PycharmProjects\try.py'
# filename = 'r' + input()
filename = input()
# filename = 'bad.py'
# filename = 'test_3.py'
empty_line_count = 0
with open(filename, 'r', encoding='utf-8') as file:
    for number, line in enumerate(file):
        mistakes[number + 1] = []
        if check_length(line):
            mistakes[number + 1].append('S001')
        if check_indentation(line) == 'Not Ok':
            mistakes[number + 1].append('S002')
        if check_semicolon(line):
            logging.debug(number + 1)
            mistakes[number + 1].append('S003')
        if check_inline_comment(line):
            mistakes[number + 1].append('S004')
        if check_todo(line):
            mistakes[number + 1].append('S005')
        if line == '\n':
            empty_line_count += 1
        else:
            if empty_line_count > 2:
                mistakes[number + 1].append('S006')
                empty_line_count = 0


def process_result(data: dict):
    new_m = dict()
    for key, value in mistakes.items():
        if value:
            new_m[key] = sorted(list(set(value)))
    return new_m


def print_sorted_results(data: dict):
    """Line X: Code Message"""
    for lineno, errors in data.items():
        for error in errors:
            print(f'Line {lineno}: {error} {messages[error]}')


mistakes = process_result(mistakes)
print_sorted_results(mistakes)
