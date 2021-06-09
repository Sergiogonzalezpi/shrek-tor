#!/usr/bin/python

import socket
import struct
import sys

def send(message, ip_target, port_target):
    sckt = socket.socket()
    sckt.connect((str(ip_target), int(port_target)))
    sckt.send(message)
    respuesta = sckt.recv(4096)
    sckt.close()
    return str(respuesta)


def recive(ip_source, port_source):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (str(ip_source), int(port_source))
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1)
    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        try:
            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(4096)
                if data:
                    connection.sendall('ACK!')
                    connection.close()
                    sock.close()
                    return str(data)
                else:
                    connection.close()
                    sock.close()
                    break
        finally:
            # Clean up the connection
            connection.close()
            sock.close()