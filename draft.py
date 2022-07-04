# $TimeZoneReminder
"""
DESCRIPTION:
command-line script that allows you to:
- keep info about your contacts' time zones
- display: "what time is it now at smbd's place?"
            [my current local time] and [contact's current time]
- easily convert time (my local time into chosen time zone and vice versa)
"what time should we plan for a call? what time will be at his place when it's .. o'clock here?"
            [my local time] and [contact's time]

settings: my local time zone is UTC +3
-----
SQL
contact = (PK) contact_name / platform / comment / location / zone_name / utc_offset
keep info in sql db
filter contact's list by:
- time zone
- utc_offset
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
- unique names: don't allow add existing names, warn about that and offer: change contact, add, go back


- make it work from command-line
- clean it, check code style
- try refactoring technics
- apply everything possible from the theory
- write unit tests
"""
import datetime
import logging
import pytz
import re
import sqlite3
import time
from dateutil.tz import tzoffset, tzlocal, tz

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class InfoBase:
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
                                                                  utc_offset FLOAT)""")
            conn.commit()

    @staticmethod
    def transfer_to_sql(contact_name, platform, comment, location, zone_name, utc_offset):
        with sqlite3.connect('TimeZoneReminder.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO contact(contact_name, platform, comment, location, zone_name, utc_offset)"
                " VALUES (?, ?, ?, ?, ?, ?)", (contact_name, platform, comment, location, zone_name, utc_offset))
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
            if column == 'utc_offset':
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
    def select_all():
        with sqlite3.connect('TimeZoneReminder.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select * from contact')
            data_ = cursor.fetchall()
            conn.commit()
        return data_

    @staticmethod
    def print_contact_table():
        print('table: contact / TimeZoneReminder.db: ')
        print('| contact_name  | platform | comment                          | location | zone_name | utc_offset |')
        content = InfoBase.select_all()
        for entry in content:
            # print(*entry, sep=' | ')
            print('{0:15} | {1:10} | {2:50} | {3:6}  | {4:9}  | {5:9} '.format(entry[0],
                  entry[1], entry[2], entry[3], str(entry[4]), str(entry[5])))
        print(f'Number of entries: {len(content)}')


class TimeKeeper:
    def __init__(self):
        self.new_contact = ''
        self.command = ''
        self.call = 0

    # {'zone_short_name': (utc_offset, zone_ful_name, 1 - if seasonal
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

    tz_olson = {'UTC': 'Etc/UTC',
                'ART': 'America/Argentina/Buenos_Aires',
                'CST': 'US/Central',
                'EST': 'US/Eastern',
                'IST': 'Asia/Kolkata',
                'JST': 'Asia/Tokyo',
                'MSK': 'Europe/Moscow',
                'PST': 'US/Pacific',
                'TURKEY': 'Europe/Istanbul'
                }

    @staticmethod
    def calculate_time(time_obj, time_interval: list):
        """ how much time will it be in ..2 hours?
        Take time object.
        Return str
        """
        time0 = list(map(int, time.strftime("%H:%M", time_obj).split(':')))
        hours, minutes = time0[0], time0[1]
        time1 = datetime.timedelta(hours=hours, minutes=minutes)
        hours2, minutes2 = hours + time_interval[0], minutes + time_interval[1]
        time2 = datetime.timedelta(hours=hours2, minutes=minutes2)
        return str(time2)[:5]

    @staticmethod
    def show_current_time(tz_data):
        """convert current local time into another time zone
        Return str"""
        print(tz_data)
        try:
            offset = datetime.timedelta(hours=float(tz_data))
            tz_ = datetime.timezone(offset)
            return datetime.datetime.now(tz_).strftime('%d-%m-%Y %H:%M')
        except ValueError:
            # try:
            tz_ = pytz.timezone(TimeKeeper.tz_olson[tz_data.upper()])
            return datetime.datetime.now(tz_).strftime('%d-%m-%Y %H:%M')
            # except KeyError as e:
            #     print(f'there are no {tz_data.upper()} time zone in my database. Try again with offset')
            #     return False
        # print(f"current time in {tz_data} time zone: {datetime.datetime.now(tz_).strftime('%d-%m-%Y %H:%M')}")


    @staticmethod
    def date_constructor(zone_info, date: list, time0: list):
        """Return time zone-aware object"""
        if isinstance(zone_info, float):
            # time from local time zone
            return datetime.datetime(date[0], date[1], date[2], time0[0], time0[1], 0,
                                     tzinfo=tzoffset(None, int(zone_info * 3600)))
            # tz_from_pytz = pytz.timezone(zone_info)
            # return tz_from_pytz.localize(datetime.datetime(date[0], date[1], date[2], time0[0], time0[1]))
        try:
            # if user provided offset
            return datetime.datetime(date[0], date[1], date[2], time0[0], time0[1], 0,
                                     tzinfo=tzoffset(None, int(float(zone_info) * 3600)))  # in seconds
        except ValueError:
            try:
                # if user entered valid zone name
                tz_from_pytz = pytz.timezone(TimeKeeper.tz_olson[zone_info.upper()])
                return tz_from_pytz.localize(datetime.datetime(date[0], date[1], date[2], time0[0], time0[1]))
            except KeyError:
                print(f'there are no {zone_info} time zone in my database. Try again with offset to UTC')


    @staticmethod
    def convert_time(tz_from, tz_to, time_):
        """

        :return:
        """
        time0 = list(map(int, time_.split(':')))
        date = list(map(int, datetime.datetime.now().strftime('%Y-%m-%d').split('-')))  # [2022, 6, 29]
        dt = TimeKeeper.date_constructor(tz_from, date, time0)
        print(f'datetime aware constructed: {dt}')  # CHECK
        if not dt:
            return False
        dt_utc = dt.astimezone(pytz.utc)
        print(f' UTC {dt_utc}')  # CHECK
        if isinstance(tz_from, float):
            # from local
            # if user provided offset
            hours = int(str(float(tz_to)).split('.')[0])
            minutes = int(str(float(tz_to)).split('.')[1])
            offset_ = datetime.timedelta(hours=hours, minutes=minutes)
            tz_from_offset = datetime.timezone(offset_, name='UNKNOWN')
            dt_converted = dt_utc.astimezone(tz=tz_from_offset)
            # if user entered valid zone name
            # tz_pytz = pytz.timezone(TimeKeeper.tz_olson[tz_to.upper()])
            # dt_converted = dt_utc.astimezone(tz_pytz)
            print(f" [{dt.strftime('%H:%M %d-%m-%Y')}] your local time = "
                  f"[{dt_converted.strftime('%H:%M %d-%m-%Y')}] {tz_to} time zone.")

        else:
            # to local
            dt_converted = dt_utc.astimezone(tz_to)
            print(f"[{dt.strftime('%H:%M %d-%m-%Y')} {tz_from}] time zone = "
                  f"[{dt_converted.strftime('%H:%M %d-%m-%Y')}] your local time.")

    def time_operation(self):
        self.call += 0
        while True:
            print('''\nAvailable time operations:
0-display the time that will come after a certain time period
1-display current time in another time zone
2-convert time(local time to some other time zone or vice versa)
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

            if operation == '1':
                tz_data = input('Enter the name of time zone or offset (hours of time difference) to UTC/GMT:> ')
                time_now = self.show_current_time(tz_data)
                if time_now:
                    print(f"current time in {tz_data} time zone: {time_now}")
            elif operation == '2':
                from_local = input('convert local time? y/n ')
                if from_local.lower() == 'y':
                    tz_from = float(datetime.datetime.now().astimezone().strftime('%z')) / 100  # get local offset
                    tz_to = input('Enter the destination time zone: name or offset to UTC/GMT:> ')
                elif from_local.lower() != 'n':
                    print('Wrong command!')
                    self.time_operation()
                else:
                    tz_from = input('Enter the original time zone: name or offset to UTC/GMT:> ')
                    tz_to = tz.tzlocal()  # get local tz from PC

                _time = input('Enter time in format 00:00:> ')
                self.convert_time(tz_from, tz_to, _time)
            elif operation == '3':
                your_friend_time = input('Enter time from another time zone in format 00:00:> ')
                print(f'{your_friend_time} of {tz} time zone corresponds to ... your local time')

    def see_info(self):
        self.call += 0
        print('\nList of contacts: ')
        print(sorted(x.capitalize() for x in InfoBase.select_column('contact_name')))
        if not self.check_if_db_empty():
            self.start()
        data_for_search = input('Enter data for search(contact name/platform/time zone/time difference):> ')
        if data_for_search.capitalize() in InfoBase.select_column('platform'):
            result = InfoBase.select_row('platform', data_for_search.capitalize())
            print(f'Contacts from {data_for_search.capitalize()}:')
            print(result if result else 'no such entries')
        elif data_for_search in TimeKeeper.time_zones.keys():
            result = InfoBase.select_row('zone_name', data_for_search.upper())
            print(f'Contacts from {data_for_search}')
            print(result if result else 'no such entries')
        elif re.match('[-+]?[0-9.]', data_for_search):
            result = InfoBase.select_row('utc_offset', float(data_for_search))
            print(f'Contacts from UTC {data_for_search}:')
            print(result if result else 'no such entries')
        else:
            print('Contact info:')
            # [('Bo', 'Discord', 'Bocanada Hyperskill star', 'Seul', 'JST', 9.0)]
            data = InfoBase.select_row('contact_name', data_for_search.capitalize())
            print(data == list())
            if data == list():
                print('no such entries')
                self.start()
            else:
                print(data[0])
                if data[4]:
                    contact_time_now = self.show_current_time(data[0][4])
                else:
                    contact_time_now = self.show_current_time(data[0][5])
                if contact_time_now:
                    print(f'time for {data_for_search.capitalize()} now: {contact_time_now}')

    def add_contact(self):
        # contact = (PK) contact_name / platform / comment / location / zone_name / utc_offset
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
                    utc_offset = None
                    break
                elif re.match('[-+]?[0-9.]', time_zone):
                    zone_name = None
                    utc_offset = float(time_zone)
                    break
                else:
                    print('Incorrect format. Try again!')
        self.new_contact = (contact_name, platform, comment, location, zone_name, utc_offset)
        print(self.new_contact)
        # sql_operation = InfoBase(*self.new_contact)
        # sql_operation.run()
        InfoBase.transfer_to_sql(*self.new_contact)

    def change_contact(self):
        # [ contact_name / platform / comment / location / zone_name / utc_offset ]
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
                        InfoBase.delete_row(contact_to_change)
                        InfoBase.transfer_to_sql(*new_record)
                        print('saved')
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

    @staticmethod
    def check_if_db_empty():
        return 0 if not InfoBase.select_all() else 1

    def start(self):
        sql_operation = InfoBase()
        sql_operation.create_table()
        print('Contact base is empty' if self.check_if_db_empty() == 0 else '')
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
    print('''  _______ _                  ______                  _____                _           _           
 |__   __(_)                |___  /                 |  __ \              (_)         | |          
    | |   _ _ __ ___   ___     / / ___  _ __   ___  | |__) |___ _ __ ___  _ _ __   __| | ___ _ __ 
    | |  | | '_ ` _ \ / _ \   / / / _ \| '_ \ / _ \ |  _  // _ \ '_ ` _ \| | '_ \ / _` |/ _ \ '__|
    | |  | | | | | | |  __/  / /_| (_) | | | |  __/ | | \ \  __/ | | | | | | | | | (_| |  __/ |   
    |_|  |_|_| |_| |_|\___| /_____\___/|_| |_|\___| |_|  \_\___|_| |_| |_|_|_| |_|\__,_|\___|_|   
                                                                                                  
                                                                                                  ''')
    new = TimeKeeper()
    new.start()


if __name__ == '__main__':
    main()
