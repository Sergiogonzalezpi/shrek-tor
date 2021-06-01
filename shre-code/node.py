#!/usr/bin/python

import protocol_sendrecv as psr
import protocol_control as pctrl
import protocol_security as psec

#my_ip, my_port = pctrl.get_info_host('hostconfig.json')

#print((my_ip, my_port))

json_str = pctrl.json_ToString('config.json')

# print('data', json_str)

psr.send(json_str, '172.17.0.2', 1990)

''' -Protocol_Node----------------------------------------------------------------- '''

# solicitud de certificados inicio de la ejecucion del nodo - nodo de seguridad

    ## Conseguir claves de ca

msg = 'solicitar clave pub'
ip_ca = ''
port_ca = 0
psr.send(msg, ip_ca, port_ca)

    ## Creacion de solicitud de certificado

file_priv_key = ''
file_req_cert = ''
my_ip = ''
psec.generate_priv_key(file_priv_key)
psec.request_certificate(file_priv_key,'ESP','Madrid','UPM', my_ip, file_req_cert)

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
ip_control, port_control = pctrl.get_info_host(file_name_config)

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