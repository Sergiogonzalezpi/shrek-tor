#!/usr/bin/python

import os
import hashlib
from socket import gethostname

# Digital Certificate - CA Protocols

def create_certificate_CA(route_privkey, country, city, organization, ip, name_certificate):
    command = 'openssl req -x509 -sha256 -nodes -newkey rsa:2048 -keyout ' + route_privkey + '.pem -out ' + name_certificate + '.crt -days 365 -subj /C=' + country + '/ST=' + city + '/L=' + city + '/O=' + organization + '/OU=' + organization + '/CN=' + ip + '/'
    execution(command)

def sign_certificate_CA(csr_name_file, certificate_CA, private_key_CA, name_certificate_signed):
    command = 'openssl x509 -req -days 365 -in ' + csr_name_file + '.csr -CA ' + certificate_CA + '.crt -CAkey ' + private_key_CA + '.pem -out ' + name_certificate_signed + '.crt'
    execution(command)

# Administration Keys - Nodes Protocols

def generate_priv_key(name_private_key):
    command = 'openssl genrsa -out ' + name_private_key + '.pem 2048'
    execution(command)

def extract_pub_key(route_privkey, route_pubkey):
    # route_privkey.pem
    # route_pubkey.pem
    command = 'openssl rsa -in ' + route_privkey + ' -out ' + route_pubkey + ' -pubout'
    execution(command)

def extract_priv_key(route_privkey, route_pubkey):
    # route_privkey.pem & route_pubkey.pem
    command = 'rsa -in ' + route_privkey + ' -out ' + route_pubkey + ' -pubout'
    execution(command)

# Digital Certificate - Nodes Protocols

def get_certified(name_certificate):
    # name_certificate.crt
    command = 'openssl x509 -in ' + name_certificate + ' -text -noout'
    execution(command)

def request_certificate(route_priv_key, country, city, organization, name, name_certificate):
    # route_priv_key.pem
    # name_certificate.csr
    # name <- ip
    command = 'openssl req -new -newkey rsa:2048 -nodes -keyout ' + route_priv_key + ' -out ' + name_certificate + ' -subj \"/C=' + country + '/ST=' + city + '/L=' + city + '/O=' + organization + '/OU=' + organization + '/CN=' + name + '/\"'
    execution(command)

# Authentication - Nodes Protocols

def sign_resume(route_privkey, route_resume_sign, route_resume):
    command = 'openssl dgst -c -sign ' + route_privkey + '.pem -out ' + route_resume_sign + '.sign ' + route_resume + '.hash'
    execution(command)

def verified_resume(route_pubkey, route_resume_sign, route_resume):
    command = 'openssl dgst -c -verify ' + route_pubkey + '.pem -signature ' + route_resume_sign + '.sign ' + route_resume + '.hash'
    execution(command)

# Integrity - Node Protocols

def generate_resume(route_file, route_hash ):
    h = hashlib.sha1()
    file = open(route_file, 'rb')
    file_data = file.read()
    file.close()
    h.update(file_data)
    file = open(route_hash, 'a')
    file.write(h.hexdigest())
    file.close()

def compare_resume(route_hash_source, route_hash_target):
    file_source = open(route_hash_source, 'rb')
    hash_source = file_source.read()
    file_target = open(route_hash_target, 'rb')
    hash_target = file_target.read()
    return str(hash_source) == str(hash_target)

# Encrypt RSA - Node Protocol

def encrypt_rsa(pub_key, file_to_encrypt, file_output):
    execution('openssl rsautl -encrypt -pubin -inkey ' + pub_key + ' -in ' + file_to_encrypt + ' -out ' + file_output)

def decrypt_rsa(priv_key, file_to_decrypt, file_output):
    execution('openssl rsautl -decrypt -inkey ' + priv_key + ' -in ' + file_to_decrypt + ' -out ' + file_output)

# Execution commands

def execution(command):
    try:
        if os.system(command) != 0:
            raise Exception('Failed command')
        return True
    except:
        print('Failed command')
        return False




# Test Protocols

#generate_priv_key('privkeyprueba')
#extract_pub_key('privkeyprueba', 'pubkeyprueba')
#request_certificate('tempkey', 'ES', 'Madrid', 'Shrek-Tor', 'prueba', 'usersolicition')
#create_certificate_CA('privkey', 'ES', 'Madrid', 'Shrek-Tor', gethostname(), 'CACertificate')
#sign_certificate_CA('usersolicition', 'CACertificate', 'privkey', 'certificateuser')

'''
-----------------------------------------------------------------------------------------
def generate_resume(route_hash, route_file):
    command = 'openssl dgst -sha1 -out ' + route_hash + ' ' + route_file
    execution(command)
-----------------------------------------------------------------------------------------
'''