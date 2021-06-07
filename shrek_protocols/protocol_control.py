#!/usr/bin/python

import os
import json
import socket
import random
import base64


# Network Configuration - Control Protocol

def keep_ip(route_config_file, ip, port):
    exists = False
    file = open(route_config_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    host_index = len(json_data['host'])
    if host_index != 0:
        for position in range(0, host_index):
            if json_data['host'][position]['ip'] == ip:
                exists = True
    if not exists:
        json_data['host'].append({})
        json_data['host'][host_index]['ip'] = ip
        json_data['host'][host_index]['port'] = port
        json_obj = json.dumps(json_data, indent=4)
        file = open(route_config_file, 'w')
        file.write(json_obj + '\n')
        file.close()


def set_info_host(route_config_file, port):
    file = open(route_config_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    hostname = socket.gethostname()
    json_data['host']['ip'] = socket.gethostbyname(hostname)
    json_data['host']['port'] = port
    json_obj = json.dumps(json_data, indent=4)
    file = open(route_config_file, 'w')
    file.write(json_obj + '\n')
    file.close()


def get_info_host(route_config_file, opc):
    file = open(route_config_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    ip = json_data[str(opc)]['ip']
    port = json_data[str(opc)]['port']
    return (ip, port)


# Tunneling Network - Control Protocol

def add_host_to_route(route_config_file, ip, port):
    file = open(route_config_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    index = len(json_data['hosts'])
    json_data['hosts'].append({})
    json_data['hosts'][index]['ip'] = ip
    json_data['hosts'][index]['port'] = port
    json_obj = json.dumps(json_data, indent=4)
    file = open(route_config_file, 'w')
    file.write(json_obj + '\n')
    file.close()


def set_instructions_tunnel(route_config_file):
    exists = False
    file = open(route_config_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    host_index = len(json_data['hosts'])


# Load config files - Node Protocol

def get_config_files():
    execution('wget https://raw.githubusercontent.com/Sergiogonzalezpi/shrek-tor/main/hostconfig.json')


# Utilities

#   Read and write files

def files(file_input, wr, message = ''):
    if str(wr) == 'write':
        opc = 'w'
    else:
        opc = 'rb'
    file = open(file_input, opc)
    if str(wr) == 'write':
        file.write(message)
        file.close()
    else:
        file_data = file.read()
        file.close()
        return file_data
    return 'Close file ...'


#   Execution commands

def execution(command):
    try:
        if os.system(command) != 0:
            raise Exception('Failed command')
        return True
    except:
        print('Failed command')
        return False


#   String formatting - Node Protocol

def json_toString(json_file):
    file = open(json_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    return str(json_data)


def str_base64(str_n):
    return base64.b64encode(str(str_n))


def base64_str(base_str):
    return base64.b64decode(str(base_str))

