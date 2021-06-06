#!/usr/bin/python

import os
import json
import socket
import random

# Network Configuration - Control Protocol

def keep_ip(route_config_file, ip, port):
    exists = False
    file = open(route_config_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    host_index = len(json_data['host'])
    if(host_index != 0):
        for position in range(0,host_index):
            if(json_data['host'][position]['ip'] == ip):
                exists = True
    if(exists == False):
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
    return (ip,port)

def json_toString(json_file):
    file = open(json_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    return str(json_data)

# Tunneling Network - Control Protocol

def set_instructions_tunnel(route_config_file):
    exists = False
    file = open(route_config_file, 'rb')
    file_data = file.read()
    file.close()
    json_data = json.loads(str(file_data))
    json_data = dict(json_data)
    host_index = len(json_data['host'])


# Load config files - Node Protocol

def get_config_files():
    execution('wget https://raw.githubusercontent.com/Sergiogonzalezpi/shrek-tor/main/hostconfig.json')

# Execution commands

def execution(command):
    try:
        if os.system(command) != 0:
            raise Exception('Failed command')
        return True
    except:
        print('Failed command')
        return False