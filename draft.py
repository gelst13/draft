"""
when started: checkif db exists
case not: create db table with fields
(zone name / seasonal / difference to UTC / difference to Msk / Msk time / contacts / locations / info
keep info in sql db
filter contact's list by:
- time zone
- communicating platform


0.convert time:
- my local time into chosen time zone
- time of some event in another time zone into my local time
1.see contact info
- enter contact name
- or show sorted list of contacts and then choose from that list
2.add contact
! contact names must be unique
3.change contact
4.exit
"""
import logging
import re


logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class TimeKeeper:
    def __init__(self):
        self.data = dict()
        self.command = ''
        self.call = 0

    time_zones = {'UTC': (0, ''),
                  'ART': (-3, 'Argentina Time'),
                  'IST': (5.5, 'India Standard Time'),
                  'PDT': (-7, 'Pacific Daylight Time', 1),
                  'JST': (9, 'Japan Standard Time')}

    def convert_time(self):
        self.call += 0
        print('''it's possible to convert time:
a. my local time into chosen time zone
b. time of some event in another time zone into my local time''')

    def see_info(self):
        self.call += 0
        choice = input('show list of contacts? Y/N:> ')
        data_for_search = input('Enter data for search(contact name/time zone):> ')
        print('Contact info:')

    def add_contact(self):
        self.call += 0
        contact_name = input('Enter contact name/nick: >')
        platform = input('Where do you communicate?: Discord, Skype, Telegram, WhatsApp')
        comment = input('Additional info:> ')
        while True:
            time_zone = input('Enter the name of time zone or hours of time difference to UTC/GMT')
            if time_zone.isalpha():
                zone_name = time_zone
                difference_to_UTC = TimeKeeper.time_zones[time_zone]
                break
            elif re.match('[-+]?[0-9]', time_zone):
                difference_to_UTC = int(time_zone)
                break
            else:
                print('Incorrect format. Try again!')
        self.data.update({contact_name: (platform, comment, time_zone, difference_to_UTC)})
        print(self.data)

    def change_contact(self):
        self.call += 0
        contact_name = input('Enter contact name/nick to be changed: >')

    actions = {'0': convert_time,
               '1': see_info,
               '2': add_contact,
               '3': change_contact,
               }

    def start(self):
        while True:
            print('choose action:\n0.convert time\n1.see contact info\n2.add contact'
                                 '\n3.change contact\n4.exit')
            self.command = input()
            if self.command == '4':
                exit()
            elif self.command not in list(TimeKeeper.actions.keys()):
                print('Incorrect command. Enter number from 0 to 4')
            else:
                TimeKeeper.actions[self.command.lower()](self)


def main():
    new = TimeKeeper()
    new.start()


if __name__ == '__main__':
    main()
