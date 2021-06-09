# !/usr/bin/python

'''
import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time
'''

import shrek_protocols.protocol_sendrecv as psr
import shrek_protocols.protocol_control as pctrl
import shrek_protocols.protocol_security as psec
import time

# Variables

file_hostconfig = 'hostconfig.json'
pubkey = 'pubkey.pem'
privkey = 'privkey.pem'

# iniciar las configuraciones del nodo

def configuration(port):
    #   Download configure host
    # pctrl.get_config_files() # Only if the node is connect to internet direct

    #   Configure node
    pctrl.set_info_host('hostconfig.json', int(port))
    my_ip, my_port = pctrl.get_info_host('hostconfig.json', 'host')
    return my_ip

# Certificados CA
def config_security_ca(ip):
    psec.create_certificate_CA('privkey.pem', 'ES', 'Madrid', 'UPM', ip, 'certificate.crt')
    psec.extract_pub_key('privkey.pem', 'pubkey.pem')


# solicitud de certificados inicio de la ejecucion del nodo - Nodes + Ctrl
def create_request_cert(ip):
    file_priv_key = 'privkey.pem'
    file_pub_key = 'pubkey.pem'
    file_req_cert = 'request.csr'
    psec.generate_priv_key(file_priv_key)
    psec.extract_pub_key(file_priv_key, file_pub_key)
    psec.request_certificate(file_priv_key, 'ES', 'Madrid', 'UPM', ip, file_req_cert)


# Signed request certified to CA - Nodes + Ctrl

def req_cert_ca(my_ip, my_port, pub_key_target):
    request = 'sign cert'
    file_cert_req = 'request.csr'
    file_cert_signed = 'certificate.crt'
    ca_ip, ca_port = pctrl.get_info_host(file_hostconfig, 'ca')
    send_encrypt_file(file_cert_req, pub_key_target, ca_ip, ca_port, my_ip, my_port, request)
    pubkey_str = pctrl.files(pubkey,'read')
    time.sleep(1)
    ack = psr.send(pubkey_str, ca_ip, ca_port)
    cert = psr.recive(my_ip,my_port)
    pctrl.files(file_cert_signed,'write', cert)

# Exchange pubkey - All Nodes
def req_exchange_pubkey(my_ip, my_port, opc, ip_target=' ', port_target=' '):
    msg = 'req pubkey'
    if not opc == 'node':
        ip_target, port_target = pctrl.get_info_host('hostconfig.json', opc)
    print(str((my_ip, my_port, msg)))
    confirm_msg = psr.send(str((my_ip, my_port, msg)), str(ip_target), int(port_target))
    if str(confirm_msg) == 'ACK!':
        pubkeynode = str(psr.recive(str(my_ip), int(my_port)))
        if pubkeynode:
            file = open('pubkey' + opc + '.pem', 'w')
            file.write(str(pubkeynode))
            file.close()


# Send encrypt files - All nodes

def send_encrypt_file(file_msg, node_pub_key, ip_send, port_send, my_ip, my_port, request=''):
    temp_key_aes = 'tempkeyaes.pem'
    temp_key_aes_enc = 'tempkeyaes.enc'
    temp_file_data = 'ntempfiledata.txt'
    temp_file_data_enc = 'tempfiledata.enc'

    if not request == '':
        ack = psr.send(str((my_ip, my_port, request)), str(ip_send), int(port_send))
        print(request, ack)

    psec.generate_priv_key_AES(temp_key_aes)

    try:
        open(file_msg, 'rb')
        print('copy----')
        pctrl.execution('cp ' + file_msg + ' ' + temp_file_data)
    except:
        print('create----')
        file = open(temp_file_data, 'w')
        file.write(file_msg)
        file.close()

    psec.encrypt_rsa(node_pub_key, temp_key_aes, temp_key_aes_enc)

    psec.encrypt_aes(temp_key_aes, temp_file_data, temp_file_data_enc)

    file = open(temp_key_aes_enc, 'rb')
    file_key = file.read()
    file.close()
    file = open(temp_file_data_enc, 'rb')
    file_data = file.read()
    file.close()

    time.sleep(1)
    ack = psr.send(str(file_key), str(ip_send), int(port_send))

    time.sleep(1)
    ack = psr.send(str(file_data), str(ip_send), int(port_send))

    print(ack)


# Recive encrypt files - All Nodes

def recive_encrypt_file(my_ip, my_port, outputfile=''):
    temp_key_aes = 'tempkeyaes.pem'
    temp_key_aes_enc = 'tempkeyaes.enc'
    temp_file_data_dec = 'tempfiledata.dec'
    temp_file_data_enc = 'tempfiledata.enc'

    print('[+] Wait key ...')
    message_key = psr.recive(my_ip, my_port)
    print('[+] Wait data ...')
    message_data = psr.recive(my_ip, my_port)
    print(message_key)
    print(message_data)

    file = open(temp_key_aes_enc, 'w')
    file.write(message_key)
    file.close()
    print('        (*) desencriptar privkeyaes')
    psec.decrypt_rsa(privkey, temp_key_aes_enc, temp_key_aes)

    file = open(temp_file_data_enc, 'w')
    file.write(message_data)
    file.close()
    print('        (*) desencriptar file')

    if outputfile == '':
        outputfile = temp_file_data_dec

    psec.decrypt_aes(temp_key_aes, temp_file_data_enc, outputfile)

    file = open(outputfile, 'rb')
    file_data = file.read()
    file.close()
    print(file_data)

    return file_data

# Adding new host - Node Ctrl

def new_host(new_ip, new_port, new_pubkey):
    pctrl.add_host_to_network('networkhosts.json', new_ip, new_port, new_pubkey)
