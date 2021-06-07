#!/usr/bin/python

import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time


priv_key_aes = 'privkeyaes.pem'
priv_key_aes_enc = 'privkeyaes.enc'
ca_pub_key = 'pubkeyca.pem'
my_pub_key = 'pubkey.pem'
my_pub_key_enc = 'pubkey.enc'

psec.generate_priv_key_AES(priv_key_aes)

psec.encrypt_rsa(ca_pub_key, priv_key_aes, priv_key_aes_enc)

psec.encrypt_aes(priv_key_aes, my_pub_key, my_pub_key_enc)

file = open(priv_key_aes_enc, 'rb')
file_data = file.read()
file.close()

time.sleep(1)
ack = psr.send(str(file_data), '172.12.0.200', 5000)

print(ack)

file = open(my_pub_key_enc, 'rb')
file_data = file.read()
file.close()

time.sleep(1)
ack = psr.send(str(file_data), '172.12.0.200', 5000)

print(ack)

