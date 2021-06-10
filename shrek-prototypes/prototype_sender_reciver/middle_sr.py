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
file_msg = 'tempfiledata.temp'
file_msg_enc = 'tempfiledata.enc'
pub_key_node = 'pubkeynode.pem'
my_pub_key = 'pubkey.pem'

while True:
    print('[+] Wait request ...')
    message = psr.recive('172.12.0.3', 1990)

    if message == 'pubkey':
        print('[+]--------Envio de clave publica ...')
        time.sleep(1)
        file = open(my_pub_key, 'rb')
        file_data = file.read()
        file.close()
        psr.send(str(file_data), '172.12.0.4', 1990)

    message = psr.recive('172.12.0.3', 1990)

    file = open(priv_key_aes_enc, 'w')
    file.write(str(message))
    file.close()

    psec.decrypt_rsa(my_priv_key, priv_key_aes_enc, priv_key_aes)

    file = open(priv_key_aes, 'rb')
    file_data = file.read()
    file.close()

    print(file_data)

    print('[+]--------Recibiendo y desencriptando datos ...')

    message = psr.recive('172.12.0.3', 1990)

    file = open(file_msg_enc, 'w')
    file.write(str(message))
    file.close()

    new_str_send = []
    new_str_send.append(message)
    new_str_send.append(file_data)

    file = open(file_msg, 'w')
    file.write(str(new_str_send))
    file.close()

    #psec.decrypt_aes(priv_key_aes, file_msg_enc, file_msg)

    #file = open(file_msg, 'rb')
    #file_data = file.read()
    #file.close()

    print(new_str_send)



    print('[+]--------Procesamiento terminado ...')

    print('[+]--------Solicitud clave publica ...')
    psr.send('pubkey', '172.12.0.2', 1990)
    pubkey_str = psr.recive('172.12.0.3', 1990)
    file = open(pub_key_node, 'w')
    file.write(str(pubkey_str))
    file.close()

    print('[+]--------Encriptacion de datos ...')
    psec.generate_priv_key_AES(priv_key_aes)

    psec.encrypt_rsa(pub_key_node, priv_key_aes, priv_key_aes_enc)

    psec.encrypt_aes(priv_key_aes, file_msg, file_msg_enc)

    file = open(priv_key_aes_enc, 'rb')
    file_data = file.read()
    file.close()
    print(str(file_data))

    print('[+]--------Enviando datos ...')

    time.sleep(1)
    ack = psr.send(str(file_data), '172.12.0.2', 1990)

    print(ack)

    file = open(file_msg_enc, 'rb')
    file_data = file.read()
    file.close()

    time.sleep(1)
    ack = psr.send(str(file_data), '172.12.0.2', 1990)

    print(ack)

    print('[+]--------Datos enviados ...')