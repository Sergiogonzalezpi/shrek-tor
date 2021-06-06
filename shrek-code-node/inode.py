#!/usr/bin/python

import shrek_protocols.protocol_sendrecv as psr
import shrek_protocols.protocol_control as pctrl
import shrek_protocols.protocol_security as psec
import time


''' -Protocol_INode----------------------------------------------------------------- '''

# iniciar las configuraciones del nodo



def configuration():
    ## Descargar configuracion de host
    pctrl.get_config_files()
    ## Configurar el nodo
    pctrl.set_info_host('hostconfig.json', 1990)
    my_ip, my_port = pctrl.get_info_host('hostconfig.json', 'host')
    return (my_ip,my_port)

# solicitud de certificados inicio de la ejecucion del nodo - nodo de seguridad

def create_request_cert():
    ## Creacion de solicitud de certificado

    file_priv_key = 'privkey.pem'
    file_pub_key = 'pubkey.pem'
    file_req_cert = 'request.crs'
    psec.generate_priv_key(file_priv_key)
    psec.extract_pub_key(file_priv_key, file_pub_key)
    psec.request_certificate(file_priv_key, 'ES', 'Madrid', 'UPM', my_ip, file_req_cert)

def exchange_pubkey(my_ip, my_port, opc):
    ## Conseguir claves de ca / control
    msg = 'solicitar clave pub'
    ip_target, port_target = pctrl.get_info_host('hostconfig.json', opc)
    print(str((my_ip, my_port, msg)))
    confirm_msg = psr.send(str((my_ip, my_port, msg)), str(ip_target), int(port_target))
    if(str(confirm_msg) == 'ACK!'):
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
            file = open('pubkeyCA.pem', 'w')
            file.write(str(pubkeyCA))
            file.close()
            print('MATCH-FINAL!!!!!!!!!!!!!!!')


my_ip, my_port = configuration()
myhost = 'host'
exchange_pubkey(my_ip, my_port, 'ca')
exchange_pubkey(my_ip, my_port, 'ctrl')
print(my_ip,my_port)

''' ------------------------------------------------------------------------------- '''