# Easy Rider Bus Company 5/6
import logging
import json
import re

logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class Rider:
    fields = {'bus_id': int,
              'stop_id': int,
              'stop_name': str,
              'next_stop': int,
              'stop_type': str,  # 1 character
              'a_time': str}

    format_errors = {'stop_name': 0,
                     'stop_type': 0,
                     'a_time': 0}

    def __init__(self):
        self.data = None
        self.errors = {'bus_id': 0,
                       'stop_id': 0,
                       'stop_name': 0,
                       'next_stop': 0,
                       'stop_type': 0,
                       'a_time': 0}
        self.format_errors = {'stop_name': 0,
                              'stop_type': 0,
                              'a_time': 0}
        self.bus_lines = dict()
        self.stops = {'Start stops': set(),
                      'Transfer stops': set(),
                      'Finish stops': set()}
        self.a_time_errors = []

    def get_data(self):
        self.data = json.loads(input())
        # _str = '[{"bus_id" : 128, "stop_id" : 3, "stop_name" : "", "next_stop" : 5, "stop_type" : "", "a_time" : "08:19"}, {"bus_id" : 128, "stop_id" : 5, "stop_name" : "Fifth Avenue", "next_stop" : 7, "stop_type" : "O", "a_time" : "08:25"}, {"bus_id" : 128, "stop_id" : "7", "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:37"}, {"bus_id" : "", "stop_id" : 2, "stop_name" : "Pilotow Street", "next_stop" : 3, "stop_type" : "S", "a_time" : ""}, {"bus_id" : 256, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 6, "stop_type" : "", "a_time" : "09:45"}, {"bus_id" : 256, "stop_id" : 6, "stop_name" : "Sunset Boulevard", "next_stop" : 7, "stop_type" : "", "a_time" : "09:59"}, {"bus_id" : 256, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : "0", "stop_type" : "F", "a_time" : "10:12"}, {"bus_id" : 512, "stop_id" : 4, "stop_name" : "Bourbon Street", "next_stop" : 6, "stop_type" : "S", "a_time" : "08:13"}, {"bus_id" : "512", "stop_id" : 6, "stop_name" : "Sunset Boulevard", "next_stop" : 0, "stop_type" : 5, "a_time" : "08:16"}]'
        # self.data = json.loads(_str)

    def check_type(self):
        """Check that the data types match.
        Check that the required fields are filled in."""
        logging.info('...def check1...')
        for entry in self.data:
            logging.debug(entry)
            for key in list(Rider.fields.keys()):
                count = 0
                if key == 'stop_type':
                    if not (isinstance(entry[key], str)) or (isinstance(entry[key], str) and len(entry[key]) > 1):
                        logging.debug(key)
                        count += 1
                elif not (type(entry[key]) == Rider.fields[key]):
                    logging.debug(key)
                    count += 1
                elif key in ('stop_name', 'a_time'):
                    if not (len(entry[key]) > 0):
                        logging.debug(key)
                        count += 1
                current_count = self.errors[key]
                self.errors.update({key: current_count + count})
        logging.debug(self.errors)

    def check_format(self):
        """Check that the data format complies with the documentation."""
        logging.info('...def check_format...')
        count0, count1, count2 = 0, 0, 0
        for entry in self.data:
            logging.debug(entry)
            correct_suffix = re.match(r'[A-Z].+[ ](?=Road$|Avenue$|Boulevard$|Street$)', entry['stop_name'])
            if not (correct_suffix and len(entry['stop_name']) > 0):
                logging.debug('stop_name')
                count0 += 1
            if entry['stop_type'] not in ('S', 'O', "F", ""):
                logging.debug('stop_type')
                count1 += 1
            military_time = re.match(r'^([01]\d|2[0-3]):?([0-5]\d)$', entry['a_time'])
            if not military_time and len(entry['a_time']) > 0:
                logging.debug('a_time')
                count2 += 1
        self.format_errors.update({'stop_name': count0})
        self.format_errors.update({'stop_type': count1})
        self.format_errors.update({'a_time': count2})
        logging.debug(self.format_errors)

    def check_lines(self):
        """how many bus lines we have and how many stops there are on each line"""
        logging.info('...def check_lines...')
        for entry in self.data:
            logging.debug(entry)
            # logging.debug(entry['bus_id'], entry['stop_id'])
            if entry['bus_id'] not in list(self.bus_lines.keys()):
                self.bus_lines[entry['bus_id']] = [(entry['stop_id'], entry['stop_type'], entry['stop_name'],
                                                    entry['a_time'])]
            else:
                current_values = self.bus_lines[entry['bus_id']]
                current_values.append((entry['stop_id'], entry['stop_type'], entry['stop_name'], entry['a_time']))
                self.bus_lines.update({entry['bus_id']: current_values})

    def check_stops(self):
        logging.info('...def check_stops')
        all_stop_names = []
        for bus_line, stops_info in list(self.bus_lines.items()):
            stop_type = []
            for stop in stops_info:
                all_stop_names.append(stop[2])
                stop_type.append(stop[1])
                if stop[1] == 'S':
                    current = self.stops['Start stops']
                    current.add(stop[2])
                    self.stops.update({'Start stops': current})
                elif stop[1] == 'F':
                    current = self.stops['Finish stops']
                    current.add(stop[2])
                    self.stops.update({'Finish stops': current})
            if stop_type.count('F') > 1 or stop_type.count('S') > 1:
                print(f'bus line {bus_line} has more than one starting point (S) or one final stop (F).')
                exit()
            elif not (stop_type.count('F') == 1 and stop_type.count('S') == 1):
                print(f'There is no start or end stop for the line: {bus_line}.')
        logging.debug(all_stop_names)
        for stop_name in all_stop_names:
            if len(stop_name) > 1 and all_stop_names.count(stop_name) > 1:
                current = self.stops['Transfer stops']
                current.add(stop_name)
                self.stops.update({'Transfer stops': current})
        logging.debug(self.stops)

    def check_time(self):
        logging.info('...def check_time')
        for bus_line, stops_info in list(self.bus_lines.items()):
            for index in range(len(stops_info)):
                try:
                    logging.debug(stops_info[index][3], stops_info[index + 1][3])
                    if stops_info[index][3] >= stops_info[index + 1][3]:
                        self.a_time_errors.append((bus_line, stops_info[index + 1][2]))
                        break
                except IndexError:
                    break
                except ValueError as e:
                    logging.debug(e)
                    continue

    def display_errors(self):
        logging.info('...def display_errors')
        # print(f'Type and required field validation: {sum(list(self.errors.values()))} errors')
        # for key, value in self.errors.items():
        #     print(f'{key}: {value}')
        # logging.debug(sum(list(self.format_errors.values())))
        # print(f'Format validation: {sum(list(self.format_errors.values()))} errors')
        # for key, value in self.format_errors.items():
        #     print(f'{key}: {value}')
        # print('Line names and number of stops:')
        # for key, value in self.bus_lines.items():
        #     print(f'bus_id: {key}, stops: {len(value)}')
        # for key, value in self.stops.items():
        #     print(f"{key}: {len(value)} {sorted(list(value))}")
        # stage 5/6
        print('Arrival time test:')
        logging.debug(self.a_time_errors)
        if not self.a_time_errors:
            print('OK')
        else:
            for error in self.a_time_errors:
                print(f'bus_id line {error[0]}: wrong time on station {error[1]}')

    def validation(self):
        logging.info('...def validation')
        self.get_data()
        # self.check_type()
        # self.check_format()
        self.check_lines()
        # self.check_stops()
        self.check_time()
        self.display_errors()


def main():
    new = Rider()
    new.validation()


if __name__ == '__main__':
    main()
