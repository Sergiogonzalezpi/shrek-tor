#!/usr/bin/python
'''
import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time
import random
import json
'''

from distlib.compat import raw_input
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

priv_key_aes = 'privkeyaes.pem'
priv_key_aes_enc = 'privkeyaes.enc'
my_pub_key = 'pubkey.pem'
my_priv_key = 'privkey.pem'
file_msg = 'tempfiledata.temp'
file_msg_enc = 'tempfiledata.enc'
pub_key_node = 'pubkeynode.pem'

while True:
    message_input = str(raw_input('Mensaje: '))

    print('[+]--------Solicitud clave publica ...')
    time.sleep(1)
    psr.send('pubkey', '172.12.0.3', 1990)
    pubkey_str = psr.recive('172.12.0.4', 1990)
    file = open(pub_key_node, 'w')
    file.write(str(pubkey_str))
    file.close()

    print('[+]--------Encriptacion de datos ...')
    psec.generate_priv_key_AES(priv_key_aes)

    file = open(file_msg, 'w')
    file.write(message_input)
    file.close()

    psec.encrypt_rsa(pub_key_node, priv_key_aes, priv_key_aes_enc)

    psec.encrypt_aes(priv_key_aes, file_msg, file_msg_enc)

    file = open(priv_key_aes_enc, 'rb')
    file_data = file.read()
    file.close()
    print(str(file_data))

    print('[+]--------Enviando datos ...')

    time.sleep(1)
    ack = psr.send(str(file_data), '172.12.0.3', 1990)

    print(ack)

    file = open(file_msg_enc, 'rb')
    file_data = file.read()
    file.close()

    time.sleep(1)
    ack = psr.send(str(file_data), '172.12.0.3', 1990)

    print(ack)

    print('[+]--------Datos enviados ...')