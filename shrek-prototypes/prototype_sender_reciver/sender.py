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
my_host = 'ctrl'
my_port = 5000
pub_key_ca = 'pubkeyca.pem'
count_num_host = 0

# Configurate
print('[+]--------Configurando nodo ...')
my_ip = utln.configuration(my_port)

priv_key_aes = 'privkeyaes.pem'
priv_key_aes_enc = 'privkeyaes.enc'
ca_pub_key = 'pubkeyca.pem'
my_pub_key = 'pubkey.pem'
my_pub_key_enc = 'pubkey.enc'
file_msg = 'tempfiledata.temp'
file_msg_enc = 'tempfiledata.enc'

psec.generate_priv_key_AES(priv_key_aes)

file = open(file_msg, 'w')
file.write(str('hola'))
file.close()

psec.encrypt_rsa('pubkeynode.pem', priv_key_aes , priv_key_aes_enc)

psec.encrypt_aes(priv_key_aes, file_msg, file_msg_enc)

file = open(priv_key_aes_enc, 'rb')
file_data = file.read()
file.close()
print(str(file_data))

time.sleep(1)
ack = psr.send(str(file_data), '172.12.0.2', 1990)

print(ack)

file = open(file_msg_enc, 'rb')
file_data = file.read()
file.close()

time.sleep(1)
ack = psr.send(str(file_data), '172.12.0.2', 1990)

print(ack)
