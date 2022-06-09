# $TimeZoneReminder
"""
DESCRIPTION:
command-line script that allows you to:
- keep info about your contacts' time zones
- display: 1) "what time is it now at his place?"
               [my current local time] and [contact's current time]
           2) "what time should we plan for a call? what time will be at his place when it's .. o'clock here?"
               [my local time] and [contact's time]
- easily convert time (my local time into chosen time zone and vice versa)

settings: my local time zone is UTC +3
-----
SQL
contact = (PK) contact_name / platform / comment / location / zone_name / difference_to_utc
keep info in sql db
filter contact's list by:
- time zone
- difference_to_utc
- communicating platform
----
menu:
0.convert time:
- my local time into chosen time zone
- time of some event in another time zone into my local time
1.add contact
! contact names must be unique
2.see contact info
- display info for a contact name
- or show sorted list of contacts and then choose from that list
3.change existing contact(just delete, rename or change some info in its record)
4.exit
----
* user can type contact_names/platform in any registry, but the program capitalize them
----
tasks:
def convert_time(self):
    a. my local time into chosen time zone
    b. vice versa

def extract_time(self):
    my time = UTC +3
    take difference_to_utc and calculate difference to my time,
    return my time

+ def see_info(self): DONE, 2 pomodoros
    choice = input('show list of contacts? Y/N:> ')
    data_for_search = input('Enter data for search(contact name/time zone):> ')

def change_contact(self):
    change existing contact(just delete, rename or change some info in its record)

- retrieve your current time zone from your device settings
- convert float time like 2.5 hours
- make it work from command-line
- clean it, check code style
- try refactoring technics
- apply everything possible from the theory
- write unit tests
"""
import logging
import re
import sqlite3


logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class InfoBase:
    # def __init__(self, contact_name, platform, comment, location, zone_name, difference_to_utc):
    #     self.contact_name = contact_name
    #     self.platform = platform
    #     self.comment = comment
    #     self.location = location
    #     self.zone_name = zone_name
    #     self.difference_to_utc = difference_to_utc
    def __init__(self):
        self.n = 0

    @staticmethod
    def create_table():
        with sqlite3.connect('TimeZoneReminder.db') as conn:
            cursor = conn.cursor()

            cursor.execute("""CREATE TABLE if not exists contact (contact_name VARCHAR(255) PRIMARY KEY,
                                                                  platform VARCHAR(255), 
                                                                  comment VARCHAR(255), 
                                                                  location VARCHAR(255),
                                                                  zone_name VARCHAR(255), 
                                                                  difference_to_utc FLOAT)""")
            conn.commit()

    @staticmethod
    def transfer_to_sql(contact_name, platform, comment, location, zone_name, difference_to_utc):
        with sqlite3.connect('TimeZoneReminder.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contact(contact_name, platform, comment, location, zone_name, difference_to_utc)"
                " VALUES (?, ?, ?, ?, ?, ?)", (contact_name, platform, comment, location, zone_name, difference_to_utc))
            conn.commit()

    @staticmethod
    def select_column(column_name):
        with sqlite3.connect('TimeZoneReminder.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select %s from contact' % column_name)
            data_ = cursor.fetchall()
            conn.commit()
            return [x[0] for x in data_]

    @staticmethod
    def select_data(key_word):
        """('Enter data for search(contact name/platform/time zone/time difference)"""
        # Never do this - insecure! using Python's string operations to assemble queries is not safe
        # , as they are vulnerable to SQL injection attacks
        with sqlite3.connect('TimeZoneReminder.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM contact WHERE contact_name = "%s"' % key_word)
            data_ = cursor.fetchall()
            conn.commit()
            return data_

    @staticmethod
    def select_row(column, key_word):
        """('Enter data for search(contact name/platform/time zone/time difference)"""
        # Never do this - insecure! using Python's string operations to assemble queries is not safe
        # , as they are vulnerable to SQL injection attacks
        with sqlite3.connect('TimeZoneReminder.db') as conn:
            cursor = conn.cursor()
            if column == 'difference_to_utc':
                cursor.execute('SELECT * FROM contact WHERE %s = "%f"' % (column, key_word))
            else:
                cursor.execute('SELECT * FROM contact WHERE %s = "%s"' % (column, key_word))
            data_ = cursor.fetchall()
            conn.commit()
            return data_

    @staticmethod
    def print_contact_table():
        with sqlite3.connect('TimeZoneReminder.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select * from contact')
            data_ = cursor.fetchall()
            conn.commit()
        print('the table contact / TimeZoneReminder.db: ')
        print('| contact_name | platform | comment | location | zone_name | difference_to_utc |')
        print(*data_, sep='\n')

    # def run(self):
        # self.create_table()
        # new_contact = ('ko', 'home', 'cat', 'Vlg', None, 0,)
        # transfer_to_sql(contact_name, platform, comment, location, zone_name, difference_to_utc)
        # self.transfer_to_sql()
        # self.print_contact_table()


class TimeKeeper:
    def __init__(self):
        self.new_contact = ''
        self.command = ''
        self.call = 0

    # {'zone_short_name': (difference_to_utc, zone_ful_name, 1 - if seasonal
    # time_zones keeps standard(winter) time for seasonal zones
    # summer daylight time = standard(winter) zone time - 1)}
    time_zones = {'UTC': (0, ''),
                  'ART': (-3, 'Argentina Time'),
                  'EST': (-5, 'Eastern Standard Time', 1),
                  'IST': (5.5, 'India Standard Time'),
                  'PST': (-8, 'Pacific Standard Time', 1),
                  'JST': (9, 'Japan Standard Time')}

    def convert_time(self):
        self.call += 0
        print('''it's possible to convert time:
a. my local time into chosen time zone
b. time of some event in another time zone into my local time''')

    def extract_time(self):
        """my time = UTC +3
        take difference_to_utc and calculate difference to my time,
        return my time"""

        pass

    def see_info(self):
        self.call += 0
        choice = input('\nshow list of contacts? Y/N:> ')
        if choice.lower() == 'y':
            print(sorted(x.capitalize() for x in InfoBase.select_column('contact_name')))
        elif choice.lower() == 'n':
            data_for_search = input('Enter data for search(contact name/platform/time zone/time difference):> ')
            if data_for_search.capitalize() in InfoBase.select_column('platform'):
                print(f'Contacts from {data_for_search.capitalize()}')
                print(InfoBase.select_row('platform', data_for_search.capitalize()))
            elif data_for_search in TimeKeeper.time_zones.keys():
                print(f'Contacts from {data_for_search}')
                print(InfoBase.select_row('zone_name', data_for_search.upper()))
            elif re.match('[-+]?[0-9.]', data_for_search):
                print(f'Contacts from UTC {data_for_search}:')
                print(InfoBase.select_row('difference_to_utc', float(data_for_search)))
            else:
                print('Contact info:')
                print(InfoBase.select_row('contact_name', data_for_search.capitalize()))

    def add_contact(self):
        # contact = (PK) contact_name / platform / comment / location / zone_name / difference_to_utc
        while True:
            contact_name = input('\nEnter contact name/nick:> ').capitalize()
            # ! contact names must be unique, check_contact_name uniqueness:
            if contact_name in InfoBase.select_column('contact_name'):
            # if contact_name in InfoBase.select_contact_name():
                print(f'Contact {contact_name} already exists. You can not add another contact with such name')
                self.add_contact()
            else:
                platform = input('Where do you communicate? (Discord, Skype, Telegram, WhatsApp):> ').capitalize()
                comment = input('Additional info/ commentary:> ')
                location = input('Where this contact lives?:> ')
                time_zone = input('Enter the name of time zone or hours of time difference to UTC/GMT:> ')
                if time_zone.isalpha():
                    zone_name = time_zone.upper()
                    difference_to_utc = None
                    break
                elif re.match('[-+]?[0-9.]', time_zone):
                    zone_name = None
                    difference_to_utc = float(time_zone)
                    break
                else:
                    print('Incorrect format. Try again!')
        self.new_contact = (contact_name, platform, comment, location, zone_name, difference_to_utc)
        print(self.new_contact)
        # sql_operation = InfoBase(*self.new_contact)
        # sql_operation.run()
        InfoBase.transfer_to_sql(*self.new_contact)

    def change_contact(self):
        self.call += 0
        contact_name = input('Enter contact name/nick to be changed: >')

    actions = {'0': convert_time,
               '1': add_contact,
               '2': see_info,
               '3': change_contact,
               }

    def start(self):
        sql_operation = InfoBase()
        sql_operation.create_table()
        while True:
            print('\nchoose action:\n0.convert time\n1.add contact\n2.see contact info'
                  '\n3.change contact\n4.exit')
            self.command = input('> ')
            if self.command == '4':
                exit()
            elif self.command == '00':
                sql_operation.print_contact_table()
            elif self.command not in list(TimeKeeper.actions.keys()):
                print('Incorrect command. Enter number from 0 to 4')
            else:
                TimeKeeper.actions[self.command.lower()](self)


def main():
    new = TimeKeeper()
    new.start()


if __name__ == '__main__':
    main()
