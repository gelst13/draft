# $Duskers 4/6
import argparse
import logging
import time
from random import Random

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')

hub = r"""║════════════════════════════════════════════════════════════════════════════════║

  ╬   ╬╬╬╬╬╬╬   ╬     ╬   ╬╬╬╬╬╬╬   ╬     ╬   ╬╬╬╬╬╬╬   ╬
  ╬╬╬╬╬     ╬╬╬╬╬     ╬╬╬╬╬     ╬╬╬╬╬     ╬╬╬╬╬     ╬╬╬╬╬
      ╬╬╬╬╬╬╬             ╬╬╬╬╬╬╬             ╬╬╬╬╬╬╬
     ╬╬╬   ╬╬╬           ╬╬╬   ╬╬╬           ╬╬╬   ╬╬╬
     ╬       ╬           ╬       ╬           ╬       ╬

║════════════════════════════════════════════════════════════════════════════════║
║                  [Ex]plore                          [Up]grade                  ║
║                  [Save]                             [M]enu                     ║
║════════════════════════════════════════════════════════════════════════════════║"""


class GamePlay:
    global hub
    n_ph = 0

    def __init__(self, _seed, min_durations, max_durations, locations):
        """The initializer of the class."""
        # self.seed = int(seed)
        self.min_durations = int(min_durations)
        self.max_durations = int(max_durations)
        self.locations = locations
        self.command = ''
        self.player_name = ''
        self.staticmethod_object = 0
        self.search_data = dict()
        self.titanium = 0
        self.short_sleep = 0.0001
        self.game_seed = Random()
        self.game_seed.seed(_seed)

        self.animation_seed = Random()
        self.animation_seed.seed(time.time())

    tytle = r"""
     #####                   #####
    #     #   ##   #####    #     # #    # ###### ###### #    #
    #        #  #    #      #     # #    # #      #      ##   #
    #       #    #   #      #     # #    # #####  #####  # #  #
    #       ######   #      #   # # #    # #      #      #  # #
    #     # #    #   #      #    #  #    # #      #      #   ##
     #####  #    #   #       #### #  ####  ###### ###### #    # """

    robots = r"""║════════════════════════════════════════════════════════════════════════════════║

       ██ ██      ██ ██      ██ ██
        █ █        █ █        █ █
       █████      █████      █████
       ██ ██      ██ ██      ██ ██
       ██ ██      ██ ██      ██ ██"""

    panel = f"""
║════════════════════════════════════════════════════════════════════════════════║
║                  [Ex]plore                          [Up]grade                  ║
║                  [Save]                             [M]enu                     ║
║════════════════════════════════════════════════════════════════════════════════║"""

    commands = ['play', 'high', 'help', 'exit', 'back', 'yes', 'no',
                'menu', 'm', 'main', 'save', 'ex', 'up', 's']

    menu = """
    |========================|
    |           MENU         |
    |                        |
    |[Back] to game          |
    |Return to [Main] Menu  |
    |[Save] and exit         |
    |[Exit] game             |
    |========================|"""

    the_question = """Are you ready to begin?\n[Yes] [No] Return to [Main]Menu"""

    def __new__(cls, *args, **kwargs):
        if cls.n_ph == 0:
            cls.n_ph += 1
            return object.__new__(cls)
        return None

    def __repr__(self):
        return f'GamePlay object with:\n' \
               f'self.staticmethod_object: {self.staticmethod_object}\n'

    def __str__(self):
        return self.__repr__()

    # def random_generator(self):
    #     r = random.random()
    #     print(r)
    #     if self.min_durations < int(r * 10) < self.max_durations:
    #         print(int(r * 10))
    #     elif int(r * 10) >= self.max_durations:
    #         return self.max_durations
    #     else:
    #         return self.min_durations

    def ask_for_command(self):
        print()
        # print('Your command:')
        self.command = input('Your command: ')

    def print_hub(self):
        print(GamePlay.robots)
        print(f'  Titanium: {self.titanium}')
        print(GamePlay.panel)

    def play(self):
        print()
        # print('Enter your name:')
        self.player_name = input('Enter your name: ')
        print()
        print(f'Greetings, player {self.player_name}!')
        print(GamePlay.the_question)
        self.command = input()

    def yes(self):
        # print("Great, now let's go code some more ;)")
        GamePlay.print_hub(self)
        self.ask_for_command()

    def no(self):
        self.staticmethod_object += 1
        print()
        print('How about now.')
        print(GamePlay.the_question)
        self.command = input()

    def high(self):
        self.staticmethod_object += 1
        print()
        print('No scores to display.\n    [Back]')
        self.command = input()

    def help(self):
        self.staticmethod_object += 1
        print()
        print('Coming SOON! Thanks for playing!')
        exit()

    def animated_print(self, text, _interval):
        logging.info('def animated_print')
        logging.debug(text)
        logging.debug(f'time_interval = {_interval}')
        if self.min_durations == 0 and self.max_durations == 0:
            print(text)
        else:
            for t in text:
                print(t, end="")
                time.sleep(_interval)
            print()

    def search(self):
        # self.slow_print('Searching')
        print("Searching", end="")
        interval = int(self.animation_seed.randint(self.min_durations, self.max_durations))
        self.animated_print(interval * "." + "\n", 1)
        if not self.search_data:
            # random.seed(self.seed)
            # self.search_data[1] = (random.choice(self.locations), random.randint(10, 100))
            self.search_data[1] = (self.game_seed.choice(self.locations), self.game_seed.randint(10, 100))

        else:
            next_search_num = list(self.search_data.keys())[-1] + 1
            # random.seed(self.seed)
            # self.search_data[next_search_num] = (random.choice(self.locations), random.randint(10, 100))
            self.search_data[next_search_num] = (self.game_seed.choice(self.locations), self.game_seed.randint(10, 100))
        for item in self.search_data.items():
            print(f'[{item[0]}] {item[1][0]}')
        print()
        print('[S] to continue searching')
        self.ask_for_command()

    def ex(self):
        # random.seed(self.seed)
        # max_number_of_locations = random.randint(1, 9)
        max_number_of_locations = self.game_seed.randint(1, 9)

        GamePlay.search(self)
        while True:
            if self.command.lower() == 's':
                if list(self.search_data.keys())[-1] == max_number_of_locations:
                    print('Nothing more in sight.\n      [Back]\n')
                    self.command = input('Your command: ')
                else:
                    GamePlay.search(self)
            elif self.command.lower() == 'back':
                self.command = 'yes'
                break
            elif int(self.command) in list(self.search_data.keys()):
                num = int(self.command)
                # self.slow_print('Deploying robots')
                print("Deploying robots", end="")
                interval = int(self.animation_seed.randint(self.min_durations, self.max_durations))
                self.animated_print(interval * ".", 1)
                print(f'{self.search_data[num][0]} explored successfully, with no damage taken.')
                acquired_titanium = self.search_data[num][1]
                self.titanium += acquired_titanium
                print(f'Acquired {acquired_titanium} lumps of titanium')
                self.search_data = dict()
                self.command = 'yes'
                break

    def up(self):
        self.staticmethod_object += 1
        print()
        print('Coming SOON! Thanks for playing!')
        exit()

    def save(self):
        self.staticmethod_object += 1
        print()
        print('Coming SOON! Thanks for playing!')
        exit()

    actions = {
        'play': play,
        'save': save,
        'yes': yes,
        'no': no,
        'up': up,
        'ex': ex,
        'help': help,
        'high': high,
    }

    def start(self):
        # print(GamePlay.tytle)
        self.animated_print(GamePlay.tytle, self.short_sleep)
        print('[Play]')
        print('[High] scores')
        print('[Help]')
        print('[Exit]')
        self.ask_for_command()

        while True:
            if self.command.lower() not in GamePlay.commands:
                print('Invalid input')
                self.ask_for_command()
            elif self.command.lower() in GamePlay.actions:
                GamePlay.actions[self.command.lower()](self)
            elif self.command.lower() == 'main':
                self.start()
            elif self.command.lower() == 'm':
                print(GamePlay.menu)
                self.ask_for_command()
            # elif self.command.lower() == 'yes':
            #     print()
            #     # print("Great, now let's go code some more ;)")
            #     GamePlay.print_hub(self)
            #     self.ask_for_command()
            elif self.command.lower() == 'back':
                GamePlay.print_hub(self)
                self.ask_for_command()
            # elif self.command.lower() == 's':
            #     GamePlay.search(self)
            elif self.command.lower() == 'exit':
                print()
                print('Thanks for playing, bye!')
                exit()


def get_args():
    """Get arguments from command line. Return parser object with attributes."""

    parser = argparse.ArgumentParser(description="This program receives 4 arguments")
    parser.add_argument("seed", nargs='?', default='10',
                        help="Type number to set a starting point for randint")
    parser.add_argument("min_durations", type=int, nargs='?', default=0,
                        help="Specify min durations of animation")
    parser.add_argument("max_durations", type=int, nargs='?', default=0,
                        help="Specify max durations of animation")
    parser.add_argument("places", help="Type possible locations", nargs='?',
                        default='High,street/Green,park/Destroyed,Arch')
    return parser.parse_args()


def main():
    logging.info(time.asctime(time.gmtime()))
    args = get_args()
    seed, min_durations, max_durations = args.seed, args.min_durations, args.max_durations
    places = args.places
    locations = [location.replace(',', ' ') for location in places.split('/')]
    logging.debug(args)
    new_game = GamePlay(seed, min_durations, max_durations, locations)
    new_game.start()


if __name__ == '__main__':
    main()
