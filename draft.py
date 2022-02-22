# $Coffee Machine
"""functionality that simulates a real coffee machine"""


class CoffeeMachine:
    """Creation of the CoffeeMachine object and related functionality."""
    
    ingredients_per_cup = {'water': 200, 'milk': 50, 'coffee beans': 15}
    n_ph = 0
    
    def __init__(self):
        """The initializer of the class.

        Arguments:
        available - {'water': _, 'milk': _, 'coffee beans': _}
        """
        # self.ingredients = CoffeeMachine.ingredient_calculator()
        self.ingredients = None
        self.available = CoffeeMachine.request_amounts()  # stock of ingredients
        self.cups_needed = CoffeeMachine.request_cups_num()
    
    def __new__(cls, *args, **kwargs):
        if cls.n_ph == 0:
            cls.n_ph += 1
            return object.__new__(cls)
        return None
    
    def __repr__(self):
        return f'CoffeeMachine object with:\n' \
               f'stock of ingredients: {self.available}\n'
    
    def __str__(self):
        return self.__repr__()
    
    @staticmethod
    def print_process():
        file_name = 'process.txt'
        # file_name = r'C:\Users\Тоша\PycharmProjects\Coffee Machine\Coffee Machine\task\machine\process.txt'
        with open(file_name, 'r') as f:
            for line in f:
                print(line.strip('\n'))
    
    def ingredient_calculator(self):
        """for stage 2/6"""
        quantity = self.cups_needed  # the numbers of coffee drinks
        # ingredients_per_cup = {'water': 200, 'milk': 50, 'coffee beans': 15}
        result = {'cups': quantity}
        for key, value in CoffeeMachine.ingredients_per_cup.items():
            result.update({key: CoffeeMachine.ingredients_per_cup[key] * quantity})
        return result
    
    def print_needed_supplies(self):
        """for stage 2/6"""
        print(self.ingredients)
        keys_ = list(self.ingredients.keys())
        print(f'For {self.ingredients[keys_[0]]} cups of coffee you will need:',
              f'{self.ingredients[keys_[1]]} ml of water',
              f'{self.ingredients[keys_[2]]} ml of milk',
              f'{self.ingredients[keys_[3]]} g of coffee beans', sep='\n')
    
    @staticmethod
    def request_amounts():
        """Request the amounts of water, milk, and coffee beans available at the moment."""
        result = dict()
        print('Write how many ml of water the coffee machine has:')
        result['water'] = int(input())
        print('Write how many ml of milk the coffee machine has:')
        result['milk'] = int(input())
        print('Write how many grams of coffee beans the coffee machine has:')
        result['coffee beans'] = int(input())
        return result
    
    @staticmethod
    def request_cups_num():
        """Ask for the number of cups a user needs."""
        print('Write how many cups of coffee you will need:')
        return int(input())
    
    def calculator(self):
        """for stage 3/6"""
        # self.cups_needed  # the numbers of coffee drinks
        calc = []
        for key in self.available.keys():
            calc.append(self.available[key] // CoffeeMachine.ingredients_per_cup[key])
        cups_possible = min(calc)
        if cups_possible == self.cups_needed:
            print('Yes, I can make that amount of coffee')
        elif cups_possible > self.cups_needed:
            n = cups_possible - self.cups_needed
            print(f'Yes, I can make that amount of coffee (and even {n} more than that)')
        else:
            print(f'No, I can make only {cups_possible} cups of coffee')


new_order = CoffeeMachine()
# new_order.print_needed_supplies()
new_order.calculator()
