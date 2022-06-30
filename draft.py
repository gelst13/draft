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
0.time operation:
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
import time
from datetime import timedelta

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
    def delete_row(key):
        try:
            conn = sqlite3.connect('TimeZoneReminder.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contact WHERE contact_name = "%s"' % key)
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            print("Failed to delete record from contact table", error)
        finally:
            if conn:
                conn.close()


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
                  'JST': (9, 'Japan Standard Time'),
                  'MSK': (3, 'Moscow Standard Time'),
                  'PST': (-8, 'Pacific Standard Time', 1),
                  }

    @staticmethod
    def calculate_time(time_obj, time_interval: list):
        """ how much time will it be in ..2 hours?
        Take time object.
        Return str
        """
        time0 = list(map(int, time.strftime("%H:%M", time_obj).split(':')))
        hours, minutes = time0[0], time0[1]
        time1 = timedelta(hours=hours, minutes=minutes)
        print(time1)  # CHECK
        hours2, minutes2 = hours + time_interval[0], minutes + time_interval[1]
        time2 = timedelta(hours=hours2, minutes=minutes2)
        return str(time2)[:5]

    def time_operation(self):
        self.call += 0
        while True:
            print('''\nAvailable time operations:
0-display the time that will come after a certain time period
1-display current time in another time zone
2-convert local time in another time zone:
3-convert time of another time zone into my local time
bbb - go back
''')
            operation = input()
            if operation == 'bbb':
                self.start()
            if operation == '0':
                time_period = list()
                time_period.append(int(input('enter how many hours forward (00-24):> ')))
                time_period.append(int(input('enter how many minutes forward (00-59):> ')))
                current_local_time = time.localtime()
                print(f"In {time_period[0]} hours {time_period[1]} minutes it'll be:")
                print(self.calculate_time(current_local_time, time_period))
                self.time_operation()
            tz = input('Enter the name of time zone or hours of time difference to UTC/GMT:> ')
            if operation == '1':
                print(f'current time in {tz} time zone: ...')
            elif operation == '2':
                local_time = input('Enter local time in format 00:00:> ')
                print(f'local {local_time} is ... in {tz} time zone')
            elif operation == '3':
                your_friend_time = input('Enter time from another time zone in format 00:00:> ')
                print(f'{your_friend_time} of {tz} time zone corresponds to ... your local time')









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
                print(f'time for {data_for_search.capitalize()} now: ...')

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
                location = input('Where this contact lives?:> ').capitalize()
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
        # [ contact_name / platform / comment / location / zone_name / difference_to_utc ]
        contact_to_change = input('\nEnter contact name/nick to be changed:> ').capitalize()
        if contact_to_change not in InfoBase.select_column('contact_name'):
            print('error: no such contact')
            self.change_contact()

        record_to_change = InfoBase.select_row('contact_name', contact_to_change)
        print(record_to_change)
        new_record = [x for x in record_to_change[0]]
        change = input('\nchoose action:\ndel - delete contact\nccc - change contact\nbbb - go back\n> ')
        if change == 'bbb':
            self.start()
        elif change == 'del':
            InfoBase.delete_row(contact_to_change)
            print('Contact deleted')
        elif change == 'ccc':
            while True:
                print('''What field do you wish to change:
                0 - contact name
                1 - platform
                2 - comment
                3 - location
                4 - zone name
                5 - difference to UTC
                sss - save changes''')
                field_no = input()
                try:
                    if field_no == 'sss':
                        print('save')
                        InfoBase.delete_row(contact_to_change)
                        InfoBase.transfer_to_sql(*new_record)
                        break
                    print(record_to_change[0][int(field_no)])
                    new_value = input('Change to:> ')
                    print(new_record)
                    if field_no == '5':  # difference to UTC keep as float
                        new_record[int(field_no)] = float(new_value)
                    elif field_no == '4':  # zone name
                        new_record[int(field_no)] = new_value.upper()
                    else:
                        new_record[int(field_no)] = new_value.capitalize()
                    print(new_record)
                except ValueError:
                    print('wrong command')
                    continue

    actions = {'00': time_operation,
               '11': add_contact,
               '22': see_info,
               '33': change_contact,
               }

    def start(self):
        sql_operation = InfoBase()
        sql_operation.create_table()
        while True:
            print('\nchoose action:\n00.time operation\n11.add contact\n22.see contact info'
                  '\n33.change contact\n44.exit')
            self.command = input('> ')
            if self.command == '44':
                exit()
            elif self.command == '000':
                sql_operation.print_contact_table()
            elif self.command not in list(TimeKeeper.actions.keys()):
                print('Incorrect command. Enter 00, 11, 22, 33 or 44')
            else:
                TimeKeeper.actions[self.command.lower()](self)


def main():
    new = TimeKeeper()
    new.start()


if __name__ == '__main__':
    main()
