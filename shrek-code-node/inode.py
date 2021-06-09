#!/usr/bin/python

'''
import utility_node as utln
import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import utility_node as utln
'''

import shrek_utilities.utility_node as utln
import shrek_protocols.protocol_sendrecv as psr
import shrek_protocols.protocol_control as pctrl
import shrek_protocols.protocol_security as psec
import time

''' -Protocol_INode----------------------------------------------------------------- '''

# Variables
my_host = 'node'
my_port = 1990
pub_key_ca = 'pubkeyca.pem'

# Configurate
print('[+]--------Configurando nodo ...')
my_ip = utln.configuration(my_port)

# Exchange keys
print('[+]--------Intercambio de clave publica ...')
utln.req_exchange_pubkey(my_ip, my_port, 'ca')

# Create request certificate
print('[+]--------Creacion de solicitud de certificado ...')
utln.create_request_cert(my_ip)
print('[+]--------Solicitud de firmado de certificado ...')
utln.req_cert_ca(my_ip, my_port, pub_key_ca)

print('[+]--------Add este host a la red ...')
ip_ctrl, port_ctrl = pctrl.get_info_host('hostconfig.json', 'ctrl')
time.sleep(1)
psr.send(str((my_ip, my_port, 'new host')), ip_ctrl, port_ctrl)
time.sleep(1)
my_pub_key = pctrl.files('pubkey.pem', 'read')
psr.send(my_pub_key, ip_ctrl, port_ctrl)

while True:
    print('[+] Wait request ...')
    verified = False
    message = psr.recive(my_ip, my_port)
    ip_target, port_target, request = eval(message)
    print('[+]--------Request: <' + request + '>')
    if request == 'send data':
        networkhostfile = 'networkhosts.json'
        temproutefile = 'temproute.json'
        temp_ip = 'tempip.temp'
        temp_ip_enc = 'tempip.enc'
        temp_privaes = 'tepmprivaes.pem'
        temp_privaes_enc = 'tepmprivaes.enc'
        temp_pubrsa = 'temppubrsa.pem'
        message = psr.recive(my_ip, my_port)
        pctrl.files(temproutefile, 'write', message)


''' ------------------------------------------------------------------------------- '''

