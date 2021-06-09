#!/usr/bin/python

'''Imports'''
'''
import utility_node as utln
import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import utility_node as utln
import json
'''

import shrek_utilities.utility_node as utln
import shrek_protocols.protocol_sendrecv as psr
import shrek_protocols.protocol_control as pctrl
import shrek_protocols.protocol_security as psec
import time
import json

''' -Protocol_INode----------------------------------------------------------------- '''

# Variables
my_host = 'node'
my_port = 1990
pub_key_ca = 'pubkeyca.pem'
pub_key = 'pubkey.pem'
priv_key = 'privkey.pem'

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
pctrl.execution('openssl x509 -inform pem -in certificate.crt -out pubkey.pem -pubkey -noout')
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
    ip_source, port_source, request = eval(message)
    print('[+]--------Request: <' + request + '>')
    if request == 'send data':
        networkhostfile = 'networkhosts.json'
        temproutefile = 'temproute.json'
        temp_ip = 'tempip.temp'
        temp_ip_enc = 'tempip.enc'
        temp_privaes = 'tepmprivaes.pem'
        temp_privaes_enc = 'tepmprivaes.enc'
        temp_pubrsa = 'temppubrsa.pem'
        message_enc = 'tempmessage.enc'
        message_dec = 'tempmessage.dec'
        message = psr.recive(my_ip, my_port)
        json_obj = json.loads(message)
        dict_obj = eval(str(json_obj))
        json_str = json.dumps(str(dict_obj), indent=4)
        pctrl.files(temproutefile, 'write', json_str)
        json_data = dict_obj['route'].pop(0)
        ip_data = json_data['ip']
        key_data = json_data['key']
        message_enc_str = dict_obj['message']
        pctrl.files(temp_ip_enc, 'write', ip_data)
        pctrl.files(temp_privaes_enc, 'write', key_data)
        pctrl.files(message_enc, 'write', message_enc_str)
        psec.decrypt_rsa(priv_key, temp_privaes_enc, temp_privaes)
        print('-----------desencriptar private aes')
        psec.decrypt_aes(temp_privaes, temp_ip_enc, temp_ip)
        print('-----------desencriptar ip')
        psec.decrypt_aes(temp_privaes, message_enc, message_dec)
        print('-----------desencriptar message')
        dict_obj['message'] = str(pctrl.files(message_dec, 'read'))
        json_obj = json.dumps(str(dict_obj), indent=4)
        ip_target = ' '
        port_target = ' '
        json_str = pctrl.files(temproutefile, 'read')
        json_file = json.loads(str(json_str))
        json_obj = eval(str(json_file))
        for count in range(0, len(json_obj['hosts'])):
            if str(ip_data) == json_obj['hosts'][count]['ip']:
                ip_target = json_obj['hosts'][count]['ip']
                port_target = json_obj['hosts'][count]['port']
        time.sleep(1)
        psr.send(str((my_ip, my_port, 'send data')), ip_target, int(port_target))
        time.sleep(1)
        psr.send(str(json_obj), ip_target, int(port_target))

''' ------------------------------------------------------------------------------- '''

