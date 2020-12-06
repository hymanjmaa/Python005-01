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
import struct
from pathlib import Path

p = Path(__file__)
base_path = p.resolve().parent


def interaction_server():
    """
    start interaction server, wait client connect, receive text or file
    :return:
    """

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1)
        print('server start...')
    except socket.error as e:
        print(e)
        print('server start fail...')
        sys.exit(1)

    try:
        while True:
            conn, addr = s.accept()

            print('{} connected'.format(addr))
            conn.send(b'connect success...')

            while True:
                file_size = struct.calcsize('128sl')
                data = conn.recv(file_size + 3)
                if data.startswith(b'1::'):  # receive text
                    print('receive data: {}'.format(data.split(b'::')[1]))
                    if not data:
                        break
                    conn.sendall(data)
                elif data.startswith(b'2::'):  # receive file
                    receive_file_handle(data, conn)
                else:
                    print('illegal data, connect close')
                    conn.close()
                    break
    finally:
        s.close()


def receive_file_handle(data, conn):
    """
    save receive file
    :param data: bytes, receive data
    :param conn: live connect
    :return:
    """

    if data:
        file_name, file_length = struct.unpack('128sl', data[3:])
        file_name = file_name.strip(b'\x00')
        print('file name: {}, file size: {}'.format(file_name, file_length))

        received_size = 0
        with open(base_path.joinpath(file_name.decode('utf-8')), 'wb') as f:
            while not received_size == file_length:
                if file_length - received_size > 1024:
                    data = conn.recv(1027)
                    received_size += len(data) - 3
                else:
                    data = conn.recv(file_length - received_size + 3)
                    received_size = file_length
                f.write(data[3:])
        print('receive file end')


if __name__ == '__main__':
    interaction_server()

