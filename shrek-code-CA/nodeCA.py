#!/usr/bin/python

import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time

''' -Protocol_NodeCA----------------------------------------------------------------- '''

ip_ca = ''
port_ca = ''

# iniciar las configuraciones del nodo

def configuration():
    ## Descargar configuracion de host
    pctrl.get_config_files()

    ## Configurar el nodo
    pctrl.set_info_host('hostconfig.json', 5000)

    my_ip, my_port = pctrl.get_info_host('hostconfig.json', 'host')
    return (my_ip, my_port)

def config_security():
    # Creacion de los certificados de la CA

    ## Claves asimetricas
    psec.create_certificate_CA('privkeyCA.pem', 'ES', 'Madrid', 'UPM', ip_ca, 'certificadoCA.cert')
    psec.extract_pub_key('privkeyCA.pem', 'pubkeyCA.pem')

def exchange_keys(opc):
    ip_ca, port_ca = pctrl.get_info_host('hostconfig.json', opc)
    recibe = psr.recive(str(ip_ca), int(port_ca))
    ip_target, port_taget, solicitud = eval(str(recibe))
    if str(solicitud) == "solicitar clave pub":
        pubkeynode = psr.recive(str(ip_ca), int(port_ca))
        file = open('pubkeynode.pem', 'w')
        file.write(str(pubkeynode))
        file.close()
        file = open('privkeyCA.pem', 'rb')
        file_data = file.read()
        file.close()
        time.sleep(1)
        ack = psr.send(str(file_data), str(ip_target), int(port_taget))
        if str(ack) == 'ACK!':
            print('MATCH-FINAL!!!!!!!!!!!!!!!')

ip_ca, port_ca = configuration()
print((ip_ca, port_ca))

''' ------------------------------------------------------------------------------- '''

# comparte la informacion a la red - nodo de control

     ## Conseguir claves de control

msg = 'solicitar clave pub'
ip_ctrl = ''
port_ctrl = 0
psr.send(msg, ip_ctrl, port_ctrl)

    ## Escucha de clave pub - nodo control
my_ip = ''
my_port = 0
psr.recive(my_ip,my_port)

    ## Extraccion de ips
file_name_config = ''
ip_control, port_control = pctrl.get_info_host(file_name_config,'host')

    ## Enviar la configuracion del nodo
msg = ''
psr.send(msg, ip_control, port_control)

''' ------------------------------------------------------------------------------- '''

# espera a envio de mensajes de la red

        ## procesamiento del mensaje  - informacion de control
        ## reenvio de mensajes - send

        ## si no existe pedir nuevas instrucciones a control

''' ------------------------------------------------------------------------------- '''

# revisar