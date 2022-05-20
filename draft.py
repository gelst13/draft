# !/usr/bin/python
# -*- coding: utf-8
# $Text-Based Browser 4/4
"""

"""
import logging
import os
import requests
import sys
from collections import deque

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class InvalidUrl(Exception):
    def __str__(self):
        return 'InvalidUrl error:  URL is incorrect, it must contain at least one dot'


class UnacceptableUrl(Exception):
    """how to add exact url in error message?"""
    
    def __repr__(self):
        return 'UnacceptableUrl error: {url} can not be accessed'
    
    def __str__(self):
        return self.__repr__()


class Browser:
    browser_stack = deque()
    
    def __init__(self, directory):
        self.command = ''
        self.url = None
        self.r = None
        self.directory = directory

    
    def check_url(self):
        logging.info("checking self.command if it's a valid URL")
        if '.' not in self.command:
            raise InvalidUrl
    
    def connect(self):
        try:
            headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'}
            self.r = requests.get('https://' + self.url, headers=headers)
            logging.debug('https://' + self.url)
            logging.debug(self.r.status_code)
            if self.r.status_code == 200:
                return 1
        except requests.exceptions.RequestException:
            logging.info('No connection!')
    
    def request(self):  # Create response-object and save it to self.r
        # Check Status
        if Browser.connect(self) == 1:
            # Getting the webpage with results of translation
            headers = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.5'}
            self.r = requests.get('https://' + self.url, headers=headers)
            self.save_website()
    
    def print_saved_webpage(self, filename):
        with open(f'{self.directory}/{filename}', 'r', encoding='utf-8') as f:
            print(f.read())
            # for line in f:
            #     print(line)
    
    def save_website(self):
        Browser.browser_stack.append(self.url)
        logging.debug(f'current page is:    https://www.{self.url} ')
        with open(f"{self.directory}/{self.url}", 'w', encoding='utf-8') as file:
            website_content = self.r.content.decode("utf-8")
            file.write(website_content)
        logging.debug(os.listdir(self.directory))
        
    
    def start(self):
        logging.info('start...')
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
            else:
                try:
                    self.check_url()
                    self.url = self.command
                    self.request()
                    Browser.print_saved_webpage(self, self.url)
                    # Browser.open_website(self)
                    
                    # self.start()
                except KeyError as err:
                    print(f'UnacceptableUrl error: url "{self.command}" can not be accessed')
                except InvalidUrl as err:
                    print(err)
                    continue


def main():
    directory = sys.argv[1]  # get a name from a command line for a folder to save pages in
    logging.debug(f'create directory: {directory}')
    if not os.access(directory, os.F_OK):  # check if directory exists
        os.mkdir(directory)  # create a single directory.
    new = Browser(directory)
    logging.debug(new)
    new.start()


if __name__ == '__main__':
    main()
