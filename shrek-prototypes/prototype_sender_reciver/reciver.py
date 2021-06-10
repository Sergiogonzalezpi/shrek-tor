#!/usr/bin/python
'''
import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time
import random
import json
'''

import shrek_utilities.utility_node as utln
import json
import shrek_protocols.protocol_sendrecv as psr
import shrek_protocols.protocol_control as pctrl
import shrek_protocols.protocol_security as psec
import time
import random

# Variables
my_host = 'inodo'
my_port = 1990

# Configurate
print('[+]--------Configurando nodo ...')
my_ip = utln.configuration(my_port)

my_priv_key = 'privkey.pem'
priv_key_aes = 'privkeyaes.pem'
priv_key_aes_enc = 'privkeyaes.enc'
pub_key_node_enc = 'pubkeynode.enc'
pub_key_node_dec = 'pubkeynode.dec'
file_msg = 'tempfiledata.temp'
file_msg_enc = 'tempfiledata.enc'
my_pub_key = 'pubkey.pem'

while True:
    print('[+] Wait request ...')
    message = psr.recive('172.12.0.2', 1990)

    if message == 'pubkey':

        print('[+]--------Envio de clave publica ...')
        time.sleep(1)
        file = open(my_pub_key, 'rb')
        file_data = file.read()
        file.close()
        psr.send(str(file_data), '172.12.0.3', 1990)

    message = psr.recive('172.12.0.2', 1990)

    file = open(priv_key_aes_enc, 'w')
    file.write(str(message))
    file.close()

    psec.decrypt_rsa(my_priv_key, priv_key_aes_enc, priv_key_aes)

    file = open(priv_key_aes, 'rb')
    file_data = file.read()
    file.close()

    print(file_data)

    message = psr.recive('172.12.0.2', 1990)

    file = open(file_msg_enc, 'w')
    file.write(str(message))
    file.close()

    psec.decrypt_aes(priv_key_aes, file_msg_enc, file_msg)

    file = open(file_msg, 'rb')
    file_data = file.read()
    file.close()

    list_msg = eval(file_data)

    key_to_decrypt = list_msg[1]

    file = open(priv_key_aes, 'w')
    file.write(str(key_to_decrypt))
    file.close()

    text_to_decrypt = list_msg[0]
    file = open(file_msg_enc, 'w')
    file.write(str(text_to_decrypt))
    file.close()

    psec.decrypt_aes(priv_key_aes, file_msg_enc, file_msg)

    file = open(file_msg, 'rb')
    file_data = file.read()
    file.close()

    print(file_data)