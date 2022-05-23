# !/usr/bin/python
# -*- coding: utf-8
# $Text-Based Browser 5/6
"""

"""
import logging
import os
import re
import requests
import sys
from bs4 import BeautifulSoup
from collections import deque

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class InvalidUrl(Exception):
    def __str__(self):
        # return 'InvalidUrl error:  URL is incorrect, it must contain at least one dot'
        return 'Incorrect URL'


class UnacceptableUrl(Exception):
    """how to add exact url in error message?"""
    
    def __repr__(self):
        return 'UnacceptableUrl error: {url} can not be accessed'
    
    def __str__(self):
        return self.__repr__()


class Browser:
    browser_stack = deque()
    tag_list = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li']
    
    def __init__(self, directory):
        self.command = ''
        self.url = None
        self.r = None
        self.readable_text = list()
        self.directory = directory
        self.session = requests.Session()
    
    def check_url(self):
        logging.info("checking self.command if it's a valid URL")
        if '.' not in self.command:
            raise InvalidUrl
    
    def connect(self):
        """Check connection: request' status code"""
        try:
            logging.info('connecting ...')
            logging.debug('https://' + self.url)
            headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'}
            response = self.session.get('https://' + self.url, headers=headers)
            if response.status_code == 200:
                logging.debug(response.status_code)
                self.r = response
                return 1
        except requests.exceptions.RequestException:
            logging.info('No connection!')
            logging.error(response.status_code)
    
    def request(self):  # Create response-object and save it to self.r
        if Browser.connect(self) == 1:
            soup = BeautifulSoup(self.r.content, 'html.parser')
            for tag in Browser.tag_list:
                logging.info(tag)
                for result in soup.find_all(tag):
                    t = result.text
                    t = t.lstrip('\n')
                    t = t.replace('\n', '')
                    if t not in self.readable_text:
                        if t != '' or t != ' ':
                            self.readable_text.append(t)
            print(*self.readable_text, sep='\n')
            self.save_website()
    
    def get_filename(self):
        domain = re.search('[.a-z]{3,4}$', self.url)
        return self.url[:domain.start()]
    
    def print_saved_webpage(self):
        logging.debug(f'printing {self.url} ...')
        with open(f'{self.directory}/{self.get_filename()}', 'r', encoding='utf-8') as f:
            print(f.read())
    
    def save_website(self):
        Browser.browser_stack.append(self.url)
        logging.debug(f'current page is:    https://www.{self.url} ')
        with open(f"{self.directory}/{self.get_filename()}", 'w', encoding='utf-8') as file:
            for line in self.readable_text:
                if not re.match('^[\\n ]+$', line) or not re.match('^[ ]+|$', line) or not re.match('^[ ]+$', line):
                    line = line.replace('\n', ' ')
                    file.write(line.lstrip() + '\n')
        logging.debug('The website is successfully saved.')
        logging.debug(f'contents of {self.directory}: {os.listdir(self.directory)}')
    
    def start(self):
        logging.info('start...')
        # self.command = 'docs.python.org'
        while True:
            self.command = input()
            logging.debug(f'user_input: {self.command}')
            if self.command == 'exit':
                exit()
            # elif self.command in ('nytimes', 'bloomberg'):
            #     # if the string corresponds to the name of any file with a web page you saved before
            #     with open(f'{self.directory}/{self.command}', 'r', encoding='utf-8') as f:
            #         for line in f:
            #             print(line)
            elif self.command == 'back' and len(Browser.browser_stack) < 2:
                pass
            elif self.command == 'back':
                logging.info('--back')
                Browser.browser_stack.pop()
                self.url = Browser.browser_stack.pop()
                self.request()
                Browser.print_saved_webpage(self)
            else:
                try:
                    self.check_url()
                    self.url = self.command
                    self.request()
                    Browser.print_saved_webpage(self)
                    # self.command = 'exit'
                except KeyError as err:
                    print(f'UnacceptableUrl error: url "{self.command}" can not be accessed')
                except InvalidUrl as err:
                    print(err)
                    continue


def main():
    directory = sys.argv[1]  # get a name from a command line for a folder to save pages in
    # directory = 'dir'
    logging.debug(f'create directory: {directory}')
    if not os.access(directory, os.F_OK):  # check if directory exists
        os.mkdir(directory)  # create a single directory.
    new = Browser(directory)
    logging.debug(new)
    new.start()


if __name__ == '__main__':
    main()
