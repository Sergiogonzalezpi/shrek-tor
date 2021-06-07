#!/usr/bin/python

import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time

''' -Protocol_NodeCA----------------------------------------------------------------- '''

# iniciar las configuraciones del nodo

def configuration():
    #   Download configure host
    # pctrl.get_config_files() # Only if the node is connect to internet direct

    ## Configurar el nodo
    pctrl.set_info_host('hostconfig.json', 5000)

    my_ip, my_port = pctrl.get_info_host('hostconfig.json', 'host')
    return (my_ip, my_port)

def config_security(ip):
    # Creacion de los certificados de la CA

    ## Claves asimetricas
    psec.create_certificate_CA('privkeyCA.pem', 'ES', 'Madrid', 'UPM', ip, 'certificadoCA.cert')
    psec.extract_pub_key('privkeyCA.pem', 'pubkeyCA.pem')

def exchange_keys(my_ip, my_port):
    recibe = psr.recive(str(my_ip), int(my_port))
    ip_target, port_taget, solicitud = eval(str(recibe))
    if str(solicitud) == "solicitar clave pub":
        pubkeynode = psr.recive(str(my_ip), int(my_port))
        file = open('pubkeynode.pem', 'w')
        file.write(str(pubkeynode))
        file.close()
        file = open('pubkeyCA.pem', 'rb')
        file_data = file.read()
        file.close()
        time.sleep(1)
        ack = psr.send(str(file_data), str(ip_target), int(port_taget))
        if str(ack) == 'ACK!':
            print('MATCH-FINAL!!!!!!!!!!!!!!!')

my_ip, my_port = configuration()
myhost = 'ca'
config_security(my_ip)
while True:
    exchange_keys(my_ip, my_port)
pctrl.execution('rm pubkeynode*')
print((my_ip, my_port))

''' ------------------------------------------------------------------------------- '''