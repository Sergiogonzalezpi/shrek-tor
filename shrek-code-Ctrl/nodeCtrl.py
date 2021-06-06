#!/usr/bin/python

import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time

''' -Protocol_NodeCtrl----------------------------------------------------------------- '''

# Iniciar las configuraciones del nodo

def configuration():
    ## Descargar configuracion de host
    pctrl.get_config_files()

    ## Configurar el nodo
    pctrl.set_info_host('hostconfig.json', 5000)

    my_ip, my_port = pctrl.get_info_host('hostconfig.json', 'host')
    return (my_ip, my_port)

# Creacion de los certificados de la CA

def config_security(ip):
    ## Claves asimetricas
    psec.create_certificate_CA('privkeyCtrl.pem', 'ES', 'Madrid', 'UPM', ip, 'certificadoCtrl.cert')
    psec.extract_pub_key('privkeyCtrl.pem', 'pubkeyCtrl.pem')

# Intercambio de claves

def send_exchange_keys(my_ip, my_port):
    recibe = psr.recive(str(my_ip), int(my_port))
    ip_target, port_taget, solicitud = eval(str(recibe))
    if str(solicitud) == "solicitar clave pub":
        pubkeynode = psr.recive(str(my_ip), int(my_port))
        file = open('pubkeynode.pem', 'w')
        file.write(str(pubkeynode))
        file.close()
        file = open('privkeyCtrl.pem', 'rb')
        file_data = file.read()
        file.close()
        time.sleep(1)
        ack = psr.send(str(file_data), str(ip_target), int(port_taget))
        if str(ack) == 'ACK!':
            print('MATCH-FINAL!!!!!!!!!!!!!!!')

def req_exchange_pubkey(my_ip, my_port, opc):
    ## Conseguir claves de ca / control
    msg = 'solicitar clave pub'
    ip_target, port_target = pctrl.get_info_host('hostconfig.json', opc)
    print(str((my_ip, my_port, msg)))
    confirm_msg = psr.send(str((my_ip, my_port, msg)), str(ip_target), int(port_target))
    if(str(confirm_msg) == 'ACK!'):
        print('MATCH-1!!!')
        file = open('pubkeyCtrl.pem', 'rb')
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

# Ejecucion

my_ip, my_port = configuration()
myhost = 'ctrl'
config_security(my_ip)
req_exchange_pubkey(my_ip, my_port, 'ca')
send_exchange_keys(my_ip, my_port)
print((my_ip, my_port))

''' ------------------------------------------------------------------------------- '''