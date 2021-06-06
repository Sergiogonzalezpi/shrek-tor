#!/usr/bin/python

import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time


priv_key_aes = 'privkeyaes.pem'
priv_key_aes_enc = 'privkeyaes.enc'
my_pub_key = 'pubkeyCA.pem'
my_priv_key = 'privkeyCA.pem'
pub_key_node_enc = 'pubkeynode.enc'
pub_key_node_dec = 'pubkeynode.dec'

message = psr.recive('172.12.0.200', 5000)

file = open(priv_key_aes_enc, 'w')
file.write(str(message))
file.close()

psec.decrypt_rsa(my_priv_key, priv_key_aes_enc, priv_key_aes)

file = open(priv_key_aes, 'rb')
file_data = file.read()
file.close()

print(file_data)

message = psr.recive('172.12.0.200', 5000)

file = open(pub_key_node_enc, 'w')
file.write(str(message))
file.close()

psec.decrypt_aes(priv_key_aes, pub_key_node_enc, pub_key_node_dec)

file = open(pub_key_node_dec, 'rb')
file_data = file.read()
file.close()

print(file_data)