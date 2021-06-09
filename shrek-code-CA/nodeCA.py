#!/usr/bin/python

# import utility_node as utln
# import protocol_sendrecv as psr
# import protocol_control as pctrl
# import protocol_security as psec

import shrek_utilities.utility_node as utln
import shrek_protocols.protocol_sendrecv as psr
import shrek_protocols.protocol_control as pctrl
import shrek_protocols.protocol_security as psec
import time

''' -Protocol_NodeCA----------------------------------------------------------------- '''

# Variables
my_host = 'ca'
my_port = 5000
pub_key_ca = 'pubkeyca.pem'
certificate = 'certificate.crt'
pubkey = 'pubkey.pem'
privkey = 'privkey.pem'

# Configurate
my_ip = utln.configuration(my_port)

# Create certificate
utln.config_security_ca(my_ip)

# Wait to instruction
while True:
    print('[+] Wait request ...')
    verified = False
    message = psr.recive(my_ip, my_port)
    ip_target, port_target, request = eval(message)
    print('[+]--------Request: <' + request + '>')
    if request == 'req pubkey':
        pubkey = pctrl.files('pubkey.pem', 'read')
        time.sleep(1)
        ack = psr.send(pubkey, ip_target, port_target)
    elif request == 'sign cert':
        temp_key_pub_node = 'ntemppubkey.pem'
        temp_request_csr = 'ntemprequest.csr'
        temp_certificate_node = 'ntempcertificate.crt'
        print('    (-) recibir solicitud de certificado')
        utln.recive_encrypt_file(my_ip, my_port, temp_request_csr)
        print('    (-) recibir pubkeynode')
        pubkey_node_str = psr.recive(my_ip, my_port)
        pctrl.files(temp_key_pub_node, 'write', pubkey_node_str)
        print('    (-) firmar certificado')
        psec.sign_certificate_CA(temp_request_csr, certificate, privkey, temp_certificate_node)
        cert_str = pctrl.files(temp_certificate_node, 'read')
        print('    (-) enviar certificado firmado')
        time.sleep(1)
        psr.send(cert_str, ip_target, port_target)
        #pctrl.execution('rm ntemp*')
print('[+]--------Finish', (my_ip, my_port))

''' ------------------------------------------------------------------------------- '''
