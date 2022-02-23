# $Coffee Machine
"""functionality that simulates a real coffee machine

Stage 4/6. Possible operations are:
1)sell coffee (offer to buy one cup of coffee)
2)fill the supplies (coffee machine must get replenished)
3)take out money from the coffee machine
"""
import logging


logging.basicConfig(filename='coffee-machine.log', level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
# logging.debug('DEBUG message')
# logging.info('INFO message')
# logging.warning('WARNING message')
# logging.error('ERROR message')
# logging.critical('CRITICAL message')


class WrongCommandError(Exception):
    def __str__(self):
        return "Unknown command!"


class CoffeeMachine:
    n_ph = 0
    
    def __init__(self):
        """The initializer of the class.

        Arguments:
        initial_store: dict
        current_store: dict
        """
        self.initial_store = {'money': 550, 'water': 400, 'milk': 540, 'coffee beans': 120, 'cups': 9}
        self.current_store = self.initial_store
   
    def __new__(cls, *args, **kwargs):
        if cls.n_ph == 0:
            cls.n_ph += 1
            return object.__new__(cls)
        return None

    def __repr__(self):
        return f'CoffeeMachine object with:\n' \
               f'initial stock: {self.initial_store}\n'

    def __str__(self):
        return self.__repr__()
    
    def calculate_store(self, data: dict) -> dict:
        """Take dict with data about sales or added supplies"""
        current_result = {'money': 0, 'water': 0, 'milk': 0, 'coffee beans': 0, 'cups': 0}
        for key in list(self.initial_store.keys()):
            current_result[key] = self.initial_store[key] - data[key]
        return current_result
    
    @staticmethod
    def print_status(dict_):
        """Print initial or current stock"""
        print('The coffee machine has:')
        print(f'{dict_["water"]} ml of water',
              f'{dict_["milk"]} ml of milk',
              f'{dict_["coffee beans"]} g of coffee beans',
              f'{dict_["cups"]} disposable cups',
              f'${dict_["money"]} of money',
              sep='\n')
    
    def machine_menu(self):
        CoffeeMachine.print_status(self.initial_store)
        print()
        action = input('Write action (buy, fill, take):\n')
        if action == 'buy':
            logging.debug('action == buy')
            sales = CoffeeMachine.sell()
            self.current_store = CoffeeMachine.calculate_store(self, sales)
        elif action == 'fill':
            logging.debug('action == fill')
            added_supplies = CoffeeMachine.fill()
            self.current_store = CoffeeMachine.calculate_store(self, added_supplies)
        elif action == 'take':
            # give all the money
            logging.debug('action == take')
            print(f'I gave you ${self.initial_store["money"]}')
            self.current_store.update({'money': 0})
        else:
            raise WrongCommandError
        print()
        CoffeeMachine.print_status(self.current_store)
    
    @staticmethod
    def choose_coffee() -> str:
        """Return coffee_chosen: espresso, latte, cappuccino"""
        coffee_types = {'1': 'espresso', '2': 'latte', '3': 'cappuccino'}
        coffee_chosen = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n')
        if coffee_chosen in coffee_types.keys():
            return coffee_types[coffee_chosen]
        else:
            raise WrongCommandError
    
    @staticmethod
    def sell() -> dict:
        """User must choose one of three types of coffee"""
        sales = {'money': 0, 'water': 0, 'milk': 0, 'coffee beans': 0, 'cups': 0}
        recipes = {'espresso': {'water': 250, 'milk': 0, 'coffee beans': 16, 'price': 4},
                   'latte': {'water': 350, 'milk': 75, 'coffee beans': 20, 'price': 7},
                   'cappuccino': {'water': 200, 'milk': 100, 'coffee beans': 12, 'price': 6},
                   }
        # Ask user:
        coffee = CoffeeMachine.choose_coffee()
        sales['money'] += (-recipes[coffee]['price'])
        sales['water'] += recipes[coffee]['water']
        sales['milk'] += recipes[coffee]['milk']
        sales['coffee beans'] += recipes[coffee]['coffee beans']
        sales['cups'] += 1
        return sales
    
    @staticmethod
    def fill() -> dict:
        """Replenish supplies."""
        supplies = {'money': 0}
        print('Write how many ml of water you want to add:')
        supplies['water'] = -int(input())
        print('Write how many ml of milk you want to add:')
        supplies['milk'] = -int(input())
        print('Write how many grams of coffee beans you want to add:')
        supplies['coffee beans'] = -int(input())
        print('Write how many disposable cups of coffee you want to add:')
        supplies['cups'] = -int(input())
        return supplies


def main():
    try:
        new_operation = CoffeeMachine()
        CoffeeMachine.machine_menu(new_operation)
    except WrongCommandError as err:
        logging.error(err)


if __name__ == '__main__':
    main()
