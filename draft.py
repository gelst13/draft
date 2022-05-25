# $Flashcards 6/7
"""

"""
import csv
import io
import logging
import os
import random
import shutil
import sys

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class LoggerOut:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.filename = filename

    def write(self, message):
        self.terminal.write(message)
        with open(self.filename, "a") as file:
            print(message, file=file, flush=True, end='')

    def flush(self):
        pass


class LoggerIn:
    def __init__(self, filename):
        self.terminal = sys.stdin
        self.filename = filename

    def readline(self):
        entry = self.terminal.readline()
        with open(self.filename, "a") as file:
            print(entry.rstrip(), file=file, flush=True)
        return entry


default_log = 'default.txt'
sys.stdout = LoggerOut(default_log)
sys.stdin = LoggerIn(default_log)


class Flashcards:
    initial_string = ''
    log = io.StringIO(initial_string)
    
    def __init__(self, cmd_commands):
        self.cmd_commands = cmd_commands
        self.auto_export = False
        self.cards = dict()  # {"term":"definition, mistakes"}
        self.answer = ''
        self.errors = 0  # flag for hardest_card()
        self.quantity = 0
        self.command = ''
        self.imported_cards = []
        self.h_card = ''  # the term or terms that the user makes most mistakes with:
    
    def add(self):
        """add a card - create a new flashcard with a unique term and definition.
        """
        logging.info(' def add...')
        print('The card:')
        term = Flashcards.get_data(self, 'term')
        print('The definition of the card:')
        definition = Flashcards.get_data(self, 'definition')
        self.cards.update({term: (definition, 0)})
        logging.debug(self.cards)
        print(f'The pair ("{term}":"{definition}") has been added.')
    
    def remove(self):
        """remove a card"""
        logging.info('def remove...')
        print('Which card?')
        card = input()
        Flashcards.log.write(card + '\n')
        if card in list(self.cards.keys()):
            del self.cards[card]
            print('The card has been removed.')
        else:
            print(f"Can't remove '{card}': there is no such card.")
        logging.debug(self.cards)
    
    def import_cards(self, data=None):
        """load cards from file"""
        logging.info('def import_cards...')
        self.imported_cards = []
        if not data:
            print('File name:')
            filename = input()
            Flashcards.log.write(filename + '\n')
        else:
            logging.debug(f'starting auto_import from {data}')
            filename = data
        if not os.access(filename, os.F_OK):  # check if directory exists
            print('File not found.')
        else:
            with open(filename, 'r', encoding='utf-8') as cards_file:
                file_reader = csv.reader(cards_file, delimiter=",")
                for line in file_reader:  # Read each line
                    if line == ['term', 'definition', 'error count'] or line == []:
                        pass
                    else:
                        self.imported_cards.append(line)
            logging.debug(self.imported_cards)
            print(f'{len(self.imported_cards)} cards have been loaded.')
            self.update_memory()
            logging.debug(self.cards)
    
    def update_memory(self):
        """imported cards have priority:
        if you import a card with the name that already exists in the memory,
        the card from the file should overwrite the one in memory."""
        logging.info('def update_memory...')
        for new_card in self.imported_cards:
            try:
                self.cards.update({new_card[0]: (new_card[1], int(new_card[2]))})
            except KeyError as err:
                print(err)
                continue
    
    def export(self, data=None):
        """save cards to file"""
        logging.info('def export')
        if not data:
            print('File name:')
            filename = input()
            Flashcards.log.write(filename + '\n')
        else:
            filename = data
        logging.info(f'starting export in {filename}')
        with open(f'{filename}', 'w', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['term', 'definition', 'error count'])  # column names
            for term, definition in self.cards.items():
                csv_writer.writerow([term, definition[0], definition[1]])
        print(f'{len(self.cards.keys())} cards have been saved.')
    
    def ask(self):
        """ask the user about the number of cards they want
        and then prompt them for definitions"""
        logging.info('def ask...')
        print('How many times to ask?')
        questions_number = int(input())
        Flashcards.log.write(str(questions_number) + '\n')
        for _ in range(questions_number):
            question = random.choice(list(self.cards.keys()))
            print(f'Print the definition of "{question}":')
            mistake = Flashcards.check_answers(self, question)
            if mistake == 1:
                self.errors = 1  # this is a flag, necessary for hardest_card()
                self.cards.update({question: (self.cards[question][0], self.cards[question][1] + 1)})
        logging.debug(self.cards)
    
    def exit_app(self):
        logging.info('def exit_app')
        logging.debug(self.auto_export)
        if self.auto_export:
            logging.info('starting auto_export...')
            Flashcards.export(self, self.cmd_commands['auto_export'][1])
        else:
            print('Bye bye!')
        # Flashcards.log.close()
        exit()
    
    def save_log(self):
        """save all the lines that have been input in/output to the console to the file"""
        logging.info('def save_log')
        self.quantity = 0
        print('File name:')
        # log_name = 'log.log'
        log_name = input()
        Flashcards.log.write(log_name + '\n')
        # with open(log_name, 'w', encoding='utf-8') as file:
        #     Flashcards.log.seek(0)
        #     file.write(Flashcards.log.read())
        shutil.copyfile('default.txt', log_name)
        print('The log has been saved.')
    
    def hardest_card(self):
        logging.info('def hardest_card...')
        logging.debug(self.h_card)
        if self.errors != 0:
            max_errors = 0
            for card in self.cards.keys():
                if self.cards[card][1] > max_errors:
                    self.h_card = card
                    max_errors = self.cards[card][1]
            print(f'The hardest card is "{self.h_card}". You have {self.cards[self.h_card][1]} errors answering it.')
            logging.debug(f'The hardest card is "{self.h_card}". You have {self.cards[self.h_card][1]} errors answering it.')
        else:
            print('"There are no cards with errors."')
    
    def reset_stats(self):
        """set the count of mistakes to 0 for all the cards"""
        logging.info('def reset_stats ...')
        self.quantity = 0
        for card in self.cards.keys():
            self.cards.update({card: (self.cards[card][0], 0)})
        self.errors = 0
        print('Card statistics have been reset.')
        print(self.cards)
    
    actions = {'add': add,
               'remove': remove,
               'import': import_cards,
               'export': export,
               'ask': ask,
               'exit': exit_app,
               'log': save_log,
               'hardest card': hardest_card,
               'reset stats': reset_stats,
               }
    
    def get_data(self, category):
        logging.info('def get_data ...')
        word = input()
        Flashcards.log.write(word + '\n')
        if category == 'term':
            # terms = [self.cards[key][0] for key in list(self.cards.keys())]
            # if word in terms:
            if word in list(self.cards.keys()):
                # print(f'The {category} "{word}" already exists. Try again:')
                print('The <term/definition> already exists. Try again:')
                return Flashcards.get_data(self, category)
            else:
                return word
        elif category == 'definition':
            # definitions = [self.cards[key][1] for key in list(self.cards.keys())]
            # if word in definitions:
            definitions = [value[0] for value in self.cards.values()]
            # if word in list(self.cards.values()):
            if word in definitions:
                # print(f'The {category} "{word}" already exists. Try again:')
                print('The <term/definition> already exists. Try again:')
                return Flashcards.get_data(self, category)
            else:
                return word
    
    # def create_cards(self, index):
    #     print(f'The term for card #{index}:')
    #     # term = input()
    #     term = Flashcards.get_data(self, 'term')
    #     # term = input()
    #     print(f'The definition for card #{index}:')
    #     # definition = input()
    #     definition = Flashcards.get_data(self, 'definition')
    #     # definition = input()
    #     self.cards.update({index: (term, definition)})
    
    def check_answers(self, question):
        logging.info('def check_answers ...')
        reverse_dict = dict()
        # for term, definition in self.cards.values():
        for term, definition in self.cards.items():
            reverse_dict[definition[0]] = term
        # for index in list(self.cards.keys()):
        #     print(f'Print the definition of "{self.cards[index][0]}"')
        
        answer = input()
        Flashcards.log.write(answer + '\n')
        if answer == self.cards[question]:
            print('Correct!')
            return 0
        else:
            if answer in list(reverse_dict.keys()):
                print(f'Wrong. The right answer is "{self.cards[question][0]}", '
                      f'but your definition is correct for "{reverse_dict[answer]}".')
                return 1
            else:
                print(f'Wrong. The right answer is "{self.cards[question][0]}".')
                return 1
    
    def start(self):
        logging.info('def start ...')
        if self.cmd_commands['auto_import']:
            Flashcards.import_cards(self, self.cmd_commands['auto_import'][1])
        if self.cmd_commands['auto_export']:
            self.auto_export = True
        logging.debug(f'self.auto_export = {self.auto_export}')
        while True:
            print('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
            self.command = input()
            Flashcards.log.write(self.command + '\n')
            try:
                Flashcards.actions[self.command.lower()](self)
            except KeyError:
                continue
        
        # print('Input the number of cards:')
        # self.quantity = int(input())
        # Flashcards.create_cards(self, 1)
        # for index in range(2, self.quantity + 1):
        #     Flashcards.create_cards(self, index)
        # logging.debug(self.cards)
        # self.check_answers()


def parse_args(args_data):
    params = {'auto_export': None, 'auto_import': None}
    if len(args_data) > 1:
        for arg in args_data:
            if arg.startswith('--export_to'):
                ex_file = arg.split('=')[1]
                params.update({'auto_export': (True, ex_file)})
            elif arg.startswith('--import_from'):
                imp_file = arg.split('=')[1]
                params.update({'auto_import': (True, imp_file)})
        return params
    else:
        return params


def main():
    logging.info('def main ...')
    cmd_args = sys.argv  # like ['flashcards.py', '--export_to=states.txt']
    logging.debug(cmd_args)
    parsed_args = parse_args(cmd_args)  # [{'auto_export': None}, {'auto_import': None}]
    # or [{'auto_export': (True, 'states.txt')}, {'auto_import': None}]
    logging.debug(parsed_args)
    new = Flashcards(parsed_args)
    new.start()


if __name__ == '__main__':
    main()
