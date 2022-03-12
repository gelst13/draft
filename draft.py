#!/usr/bin/python
# -*- coding: utf-8
import re


def check_length(text):
    if len(text) > 79:
        return 'Too long'


def check_indentation(expr: str):
    """Check if Indentation is a multiple of 4."""
    if expr.startswith(' '):
        parse = re.match(r'\ {4}', expr)
        return 'Ok' if parse else 'Not Ok'


def check_todo(expr: str):
    """Check if Less than 2 spaces before inline comments."""
    if expr.find('#'):
        parse = re.findall(r'# ?[tT][oO][Dd][oO]', expr)
        if parse:
            return True


s001 = []
s002 = []
s005 = []
s006 = []


def print_results():
    for index in s001:
        print(f'Line {index}: S001 Too long')
    for index in s002:
        print(f'Line {index}: S002 Indentation is not a multiple of four;')
    for index in s005:
        print(f'Line {index}: S005 TODO found')
    for index in s006:
        print(f'Line {index}: S006 More than 2 blank lines preceding a code line.')


# filename = r'C:\Users\Тоша\PycharmProjects\try.py'
# filename = 'r' + input()
filename = 'bad.py'
empty_line_count = 0
with open(filename, 'r', encoding='utf-8') as file:
    for number, line in enumerate(file):
        if check_length(line):
            # print(number + 1)
            s001.append(number + 1)
        if check_indentation(line) == 'Not Ok':
            # print(line)
            s002.append(number + 1)
        if check_todo(line):
            s005.append(number + 1)
        if line == '\n':
            empty_line_count += 1
        else:
            if empty_line_count > 2:
                s006.append(number + 1)
                empty_line_count = 0


print_results()


