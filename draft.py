# $Flashcards 4/7
"""

"""
import logging


logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')




class Flashcards:
    def __init__(self):
        self.cards = dict()
        self.answer = ''
        self.quantity = 0
    
    def get_data(self, category):
        word = input()
        if category == 'term':
            terms = [self.cards[key][0] for key in list(self.cards.keys())]
            if word in terms:
                print(f'The {category} "{word}" already exists. Try again:')
                return Flashcards.get_data(self, category)
            else:
                return word
        elif category == 'definition':
            definitions = [self.cards[key][1] for key in list(self.cards.keys())]
            if word in definitions:
                print(f'The {category} "{word}" already exists. Try again:')
                return Flashcards.get_data(self, category)
            else:
                return word
         
    
    def create_cards(self, index):
        print(f'The term for card #{index}:')
        # term = input()
        term = Flashcards.get_data(self, 'term')
            # term = input()
        print(f'The definition for card #{index}:')
        # definition = input()
        definition = Flashcards.get_data(self, 'definition')
            # definition = input()
        self.cards.update({index: (term, definition)})
    
    def check_answers(self):
        reverse_dict = dict()
        for term, definition in self.cards.values():
            reverse_dict[definition] = term
        logging.debug(reverse_dict)
        for index in list(self.cards.keys()):
            print(f'Print the definition of "{self.cards[index][0]}"')
            answer = input()
            if answer == self.cards[index][1]:
                print('Correct!')
            else:
                if answer in list(reverse_dict.keys()):
                    print(f'Wrong. The right answer is "{self.cards[index][1]}", '
                          f'but your definition is correct for "{reverse_dict[answer]}".')
                else:
                    print(f'Wrong. The right answer is "{self.cards[index][1]}".')
        
    def start(self):
        print('Input the number of cards:')
        self.quantity = int(input())
        Flashcards.create_cards(self, 1)
        for index in range(2, self.quantity + 1):
            Flashcards.create_cards(self, index)
        logging.debug(self.cards)
        self.check_answers()


def main():
    new = Flashcards()
    new.start()


if __name__ == '__main__':
    main()
