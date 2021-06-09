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

''' -Protocol_NodeCtrl----------------------------------------------------------------- '''

# Variables
my_host = 'ctrl'
my_port = 5000
pub_key_ca = 'pubkeyca.pem'
count_num_host = 0
networkhostfile = 'networkhosts.json'

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


while True:
    print('[+] Wait request ...')
    verified = False
    message = psr.recive(my_ip, my_port)
    ip_target, port_target, request = eval(message)
    print('[+]--------Request: <' + request + '>')
    if request == 'new host':  # -------------------------------------------
        file_temp = 'tempfile.temp'
        pub_key_node = psr.recive(my_ip, my_port)
        print(pub_key_node)
        utln.new_host(ip_target, port_target, pub_key_node)
        json_file = pctrl.files(networkhostfile, 'read')
        json_data = json.loads(json_file)
        generate_route = eval(str(json_data))
        count_num_host = len(generate_route['hosts'])
        print('    (-) Added ' + str(count_num_host) + ' hosts')
    elif request == 'send data':  # -------------------------------------------
        networkhostfile = 'networkhosts.json'
        temproutefile = 'temproute.json'
        temp_ip = 'tempip.temp'
        temp_ip_enc = 'tempip.enc'
        temp_privaes = 'tepmprivaes.pem'
        temp_privaes_enc = 'tepmprivaes.enc'
        temp_pubrsa = 'temppubrsa.pem'
        first_node_ip = ' '
        first_node_port = ' '
        temp_message = 'tempmsg.temp'
        temp_message_enc = 'tempmsg.enc'
        message = psr.recive(my_ip, my_port)
        if count_num_host > 1:
            nodes = []
            nodes.append(random.randint(0, count_num_host-1))
            validate = False
            nodes.append(-1)
            while validate:
                nodes[1] = random.randint(0, count_num_host-1)
                if not nodes[0] == nodes[1]:
                    validate = True
            pctrl.execution('cp ' + networkhostfile + ' ' + temproutefile)
            json_file = pctrl.files(temproutefile, 'read')
            json_data = json.loads(json_file)
            generate_route = eval(str(json_data))
            generate_route['route'] = []
            for i in range(0, 1):
                if i<1:
                    pctrl.files(temp_ip, 'write', generate_route['hosts'][nodes[i+1]]['ip'])
                else:
                    pctrl.files(temp_ip, 'write', '172.12.0.1')
                pctrl.files(temp_pubrsa, 'write', generate_route['hosts'][nodes[i]]['pubkey'])
                pctrl.files(temp_message, 'write', str(message))
                psec.generate_priv_key_AES(temp_privaes)
                psec.encrypt_rsa(temp_pubrsa, temp_privaes, temp_privaes_enc)
                psec.encrypt_aes(temp_privaes, temp_ip, temp_ip_enc)
                psec.encrypt_aes(temp_privaes, temp_message, temp_message_enc)
                message = pctrl.files(temp_message_enc, 'read')
                ip_enc = pctrl.files(temp_ip_enc, 'read')
                key_enc = pctrl.files(temp_privaes_enc, 'read')
                generate_route['message'] = message
                generate_route['route'].append({})
                generate_route['route'][i]['ip'] = str(ip_enc)
                generate_route['route'][i]['key'] = str(key_enc)
            first_node_ip = generate_route['hosts'][nodes[0]]['ip']
            first_node_port = generate_route['hosts'][nodes[0]]['port']
            json_obj = json.dumps(str(generate_route), indent=4)
            pctrl.files(temproutefile, 'write', str(json_obj + '\n'))
            time.sleep(1)
            psr.send(str((my_ip, my_port, 'send data')), first_node_ip, first_node_port)
            time.sleep(1)
            psr.send(str(json_obj), first_node_ip, first_node_port)

''' ------------------------------------------------------------------------------- '''
