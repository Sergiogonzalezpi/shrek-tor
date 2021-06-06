#!/usr/bin/python

import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec
import time


''' -Protocol_INode----------------------------------------------------------------- '''

# iniciar las configuraciones del nodo

my_ip = ''
my_port = ''

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

def exchange():
    ## Conseguir claves de ca

    msg = 'solicitar clave pub'
    my_ip, my_port = pctrl.get_info_host('hostconfig.json', 'host')
    ip_ca, port_ca = pctrl.get_info_host('hostconfig.json', 'ca')
    print(str((my_ip, my_port, msg)))
    confirm_msg = psr.send(str((my_ip, my_port, msg)), str(ip_ca), int(port_ca))
    if(str(confirm_msg) == 'ACK!'):
        print('MATCH-1!!!')
        file = open('pubkey.pem', 'rb')
        file_data = file.read()
        file.close()
        time.sleep(0.5)
        recibe = psr.send(str(file_data), str(ip_ca), int(port_ca))
        if str(recibe) == 'ACK!':
            print('MATCH-2!!!')
        pubkeyCA = str(psr.recive(str(my_ip), int(my_port)))
        if pubkeyCA:
            file = open('pubkeyCA.pem', 'w')
            file.write(str(pubkeyCA))
            file.close()
            print('MATCH-FINAL!!!!!!!!!!!!!!!')



my_ip, my_port = configuration()
print(my_ip,my_port)

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