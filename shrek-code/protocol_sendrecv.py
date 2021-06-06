#!/usr/bin/python

import socket
import struct
import sys

def send(message, ip_target, port_target):
    print("[+] Enviando a server ip<" + ip_target + "> - port<" + str(port_target) + "> ...")
    sckt = socket.socket()
    sckt.connect((ip_target, port_target))
    sckt.send(message)
    respuesta = sckt.recv(4096)
    sckt.close()
    return respuesta


def recive(ip_source, port_source):
    print("[+] Iniciando server ...")
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (str(ip_source), int(port_source))
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    print("[+] Starting server ...")
    # Listen for incoming connections
    sock.listen(1)
    print("[+] Server wait connection ...")
    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
        print("[+] Accepted connection with ip<" + str(client_address) + ">")

        try:
            # Receive the data in small chunks and retransmit it
            while True:
                print("[+] Server listening ...")
                data = connection.recv(4096)
                if data:
                    connection.sendall('ACK!')
                    connection.close()
                    sock.close()
                    return data
                else:
                    print('no data from', client_address)
                    connection.close()
                    sock.close()
                    break
        finally:
            # Clean up the connection
            connection.close()
            sock.close()