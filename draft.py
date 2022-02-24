# $Coffee Machine
"""functionality that simulates a real coffee machine

Stage 5/6. Possible operations are: buy, fill, take, remaining, exit.
If the coffee machine doesn't have enough resources to make coffee,
the program should output 'can't make a cup of coffee' and what is missing.
if the user types "buy"  and then changes his mind
he can type "back" to return into the main cycle.
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
    
    def calculate_store(self, data: 'dict with data about sales or added supplies') -> dict:
        """Take dict with data about sales or added supplies"""
        current_result = {'money': 0, 'water': 0, 'milk': 0, 'coffee beans': 0, 'cups': 0}
        for key in list(self.current_store.keys()):
            current_result[key] = self.current_store[key] - data[key]
        return current_result
    
    @staticmethod
    def print_status(dict_: 'initial_store or current_store'):
        """Print initial or current stock"""
        print('The coffee machine has:')
        print(f'{dict_["water"]} ml of water',
              f'{dict_["milk"]} ml of milk',
              f'{dict_["coffee beans"]} g of coffee beans',
              f'{dict_["cups"]} disposable cups',
              f'${dict_["money"]} of money',
              sep='\n')
    
    def machine_menu(self):
        while True:
            action = input('Write action (buy, fill, take, remaining, exit):\n')
            
            if action == 'buy':
                print()
                logging.debug('action == buy')
                # ASK USER
                user_answer = CoffeeMachine.choose_coffee()
                # when user types 'back', CoffeeMachine.choose_coffee() return empty dict
                if user_answer == dict():
                    # let's go back to machine menu
                    CoffeeMachine.machine_menu(self)
                else:
                    sales = CoffeeMachine.sell(self, user_answer)
                    self.current_store = CoffeeMachine.calculate_store(self, sales)
                    print()
            elif action == 'fill':
                print()
                logging.debug('action == fill')
                added_supplies = CoffeeMachine.fill()
                self.current_store = CoffeeMachine.calculate_store(self, added_supplies)
                print()
            elif action == 'take':
                # give all the money
                print()
                logging.debug('action == take')
                print(f'I gave you ${self.current_store["money"]}')
                self.current_store.update({'money': 0})
                print()
            elif action == 'remaining':
                print()
                CoffeeMachine.print_status(self.current_store)
                print()
            elif action == 'exit':
                exit()
            else:
                raise WrongCommandError
        
        # CoffeeMachine.print_status(self.current_store)
    
    @staticmethod
    def choose_coffee() -> dict:
        """Return coffee_chosen as dict."""
        recipes = {'espresso': {'water': 250, 'milk': 0, 'coffee beans': 16, 'price': 4},
                   'latte': {'water': 350, 'milk': 75, 'coffee beans': 20, 'price': 7},
                   'cappuccino': {'water': 200, 'milk': 100, 'coffee beans': 12, 'price': 6},
                   }
        coffee_types = {'1': 'espresso', '2': 'latte', '3': 'cappuccino'}
        coffee_chosen = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:\n')
        if coffee_chosen in coffee_types.keys():
            return recipes[coffee_types[coffee_chosen]]
        elif coffee_chosen == 'back':
            logging.debug('coffee_chosen == back')
            return dict()
        else:
            raise WrongCommandError
    
    def resources_not_enough(self, recipe):
        # recipe = {'water': 250, 'milk': 0, 'coffee beans': 16, 'price': 4}
        for key, value in self.current_store.items():
            try:
            
                if key == 'cups' and value == 0:
                    print(f'Sorry, not enough {key}!')
                    return True
                elif value < recipe[key]:
                    print(f'Sorry, not enough {key}!')
                    return True
                # else:
                #     continue
            except KeyError:
                continue
    
    def sell(self, coffee) -> 'sales dict':
        """User must choose one of three types of coffee"""
        sales = {'money': 0, 'water': 0, 'milk': 0, 'coffee beans': 0, 'cups': 0}
        coffee_possible = CoffeeMachine.resources_not_enough(self, coffee)
        if coffee_possible:
            return sales
        else:
            print('I have enough resources, making you a coffee!')
            sales['money'] += (-coffee['price'])
            sales['water'] += coffee['water']
            sales['milk'] += coffee['milk']
            sales['coffee beans'] += coffee['coffee beans']
            sales['cups'] += 1
            return sales

    fill_commands = {
        'water': 'Write how many ml of water do you want to add:',
        'milk': 'Write how many ml of milk do you want to add:',
        'coffee beans': 'Write how many grams of coffee beans do you want to add:',
        'cups': 'Write how many disposable cups of coffee do you want to add',
    }
    
    @staticmethod
    def fill() -> 'added supplies dict':
        """Replenish supplies."""
        
        supplies = {'money': 0}
        for key in list(CoffeeMachine.fill_commands.keys()):
            print(CoffeeMachine.fill_commands[key])
            supplies.update({key: -int(input())})
        return supplies


def main():
    try:
        new_operation = CoffeeMachine()
        CoffeeMachine.machine_menu(new_operation)
    except WrongCommandError as err:
        logging.error(err)


if __name__ == '__main__':
    main()
