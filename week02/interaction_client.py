#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Project Name: Python005-01
@Author: 'Hyman MA'
@Email: 'hymanjma@gmail.com'
@Time: 2020/12/3 23:33
"""
import sys
sys.path.append('.')
import socket
from week02.interaction_config import *
import os
import struct


def interaction_client():
    """
    interaction client, connect and send text or file to server
    :return:
    """

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
    except socket.error as e:
        print(e)
        print('connect fail...')
        sys.exit(1)

    print(s.recv(1024).decode('utf-8'))

    while True:
        todo = input('1: send text 2: send file 3:quit >>')
        if todo == '1':
            send_text_handle(s)

            recv_data = s.recv(1024)
            if not recv_data:
                break
            else:
                print('receive data: {}'.format(recv_data.decode('utf-8')))
        elif todo == '2':
            file_path = input('please enter file path: ')
            file_path = file_path.encode()

            if os.path.isfile(file_path):
                send_file_handle(s, file_path)
            else:
                print('file path not exist, please retry')
                continue
        elif todo == '3':
            sys.exit(1)
        else:
            print('error todo code, please enter correct todo code')
            continue

    s.close()


def send_text_handle(s):
    """
    send text to server
    :param s: socket
    :return:
    """

    text_data = input('enter text: ')
    s.sendall(b'1::' + text_data.encode())


def send_file_handle(s, file_path):
    """
    send file to server
    :param s: socket
    :param file_path: bytes
    :return:
    """

    struct.calcsize('128sl')
    file_head = struct.pack('128sl', os.path.basename(file_path),
                            os.stat(file_path).st_size)
    s.send(b'2::' + file_head)
    print('start send, file path: {}'.format(file_path))

    with open(file_path, 'rb') as f:
        while True:
            sd = f.read(1024)
            if not sd:
                print('file {} send complete'.format(file_path))
                break
            s.send(b'2::' + sd)


if __name__ == '__main__':
    interaction_client()

