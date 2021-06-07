#!/usr/bin/python

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

''' -Protocol_INode----------------------------------------------------------------- '''


# iniciar las configuraciones del nodo


def configuration():
    #   Download configure host
    # pctrl.get_config_files() # Only if the node is connect to internet direct

    #   Configure node
    pctrl.set_info_host('hostconfig.json', 1990)
    my_ip, my_port = pctrl.get_info_host('hostconfig.json', 'host')
    return (my_ip, my_port)


# solicitud de certificados inicio de la ejecucion del nodo - nodo de seguridad

def create_request_cert(ip):
    ## Creacion de solicitud de certificado
    file_priv_key = 'privkey.pem'
    file_pub_key = 'pubkey.pem'
    file_req_cert = 'request.crs'
    psec.generate_priv_key(file_priv_key)
    psec.extract_pub_key(file_priv_key, file_pub_key)
    psec.request_certificate(file_priv_key, 'ES', 'Madrid', 'UPM', ip, file_req_cert)


def exchange_pubkey(my_ip, my_port, opc):
    #   Conseguir claves de ca / control
    msg = 'solicitar clave pub'
    ip_target, port_target = pctrl.get_info_host('hostconfig.json', opc)
    print(str((my_ip, my_port, msg)))
    confirm_msg = psr.send(str((my_ip, my_port, msg)), str(ip_target), int(port_target))
    if (str(confirm_msg) == 'ACK!'):
        print('MATCH-1!!!')
        file = open('pubkey.pem', 'rb')
        file_data = file.read()
        file.close()
        time.sleep(0.5)
        recibe = psr.send(str(file_data), str(ip_target), int(port_target))
        if str(recibe) == 'ACK!':
            print('MATCH-2!!!')
        pubkeyCA = str(psr.recive(str(my_ip), int(my_port)))
        if pubkeyCA:
            file = open('pubkey' + opc + '.pem', 'w')
            file.write(str(pubkeyCA))
            file.close()
            print('MATCH-FINAL!!!!!!!!!!!!!!!')


# Configuraciones del nodo

my_ip, my_port = configuration()
myhost = 'host'

# Generacion de claves y certificados

create_request_cert(my_ip)

# Intercambio de claves

exchange_pubkey(my_ip, my_port, 'ca')
exchange_pubkey(my_ip, my_port, 'ctrl')

# Comunicacion Nodo + Ctrl

## Get ips Ctrl

ip_ctrl, port_ctrl = pctrl.get_info_host('hostconfig.json', 'ctrl')

priv_key_aes = 'privkeyaes.pem'
priv_key_aes_enc = 'privkeyaes.enc'
ctrl_pub_key = 'pubkeyctrl.pem'
file_host = 'hostconfig.json'
file_host_enc = 'hostinfo.enc'

psec.generate_priv_key_AES(priv_key_aes)

psec.encrypt_rsa(ctrl_pub_key, priv_key_aes, priv_key_aes_enc)

psec.encrypt_aes(priv_key_aes, file_host, file_host_enc)

file = open(priv_key_aes_enc, 'rb')
file_data = file.read()
file.close()

time.sleep(1)
ack = psr.send(str(file_data), ip_ctrl, int(port_ctrl))

print(ack)

file = open(file_host_enc, 'rb')
file_data = file.read()
file.close()

time.sleep(1)
ack = psr.send(str(file_data), ip_ctrl, int(port_ctrl))

print(ack)

print(my_ip, my_port)

''' ------------------------------------------------------------------------------- '''
