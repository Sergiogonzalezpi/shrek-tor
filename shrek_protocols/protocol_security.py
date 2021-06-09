#!/usr/bin/python

import os
import hashlib
from socket import gethostname


# Digital Certificate - CA Protocols

def create_certificate_CA(route_privkey, country, city, organization, ip, name_certificate):
    command = 'openssl req -x509 -sha256 -nodes -newkey rsa:2048 -keyout ' + route_privkey + ' -out ' + name_certificate + ' -days 365 -subj /C=' + country + '/ST=' + city + '/L=' + city + '/O=' + organization + '/OU=' + organization + '/CN=' + ip + '/'
    execution(command)


def sign_certificate_CA(csr_name_file, certificate_CA, private_key_CA, name_certificate_signed):
    command = 'openssl x509 -req -days 365 -in ' + csr_name_file + ' -CA ' + certificate_CA + ' -CAkey ' + private_key_CA + ' -set_serial 000 -out ' + name_certificate_signed
    execution(command)


# Administration Keys - Nodes Protocols

def generate_priv_key_AES(name_private_key):
    command = 'openssl rand -out ' + name_private_key + ' -base64 48'
    execution(command)

def generate_priv_key(name_private_key):
    command = 'openssl genrsa -out ' + name_private_key + ' 2048'
    execution(command)


def extract_pub_key(route_privkey, route_pubkey):
    # route_privkey.pem
    # route_pubkey.pem
    command = 'openssl rsa -in ' + route_privkey + ' -out ' + route_pubkey + ' -pubout'
    execution(command)


def extract_priv_key(route_privkey, route_pubkey):
    # route_privkey.pem & route_pubkey.pem
    command = 'openssl rsa -in ' + route_privkey + ' -out ' + route_pubkey + ' -pubout'
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
    command = 'openssl dgst -c -sign ' + route_privkey + ' -out ' + route_resume_sign + ' ' + route_resume
    execution(command)


def verified_resume(route_pubkey, route_resume_sign, route_resume):
    command = 'openssl dgst -c -verify ' + route_pubkey + ' -signature ' + route_resume_sign + ' ' + route_resume
    execution(command)


# Integrity - Node Protocols

def generate_resume(route_file, route_hash):
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


# Encrypt RSA - Node Protocol + CA Protocol

def encrypt_rsa(pub_key, file_to_encrypt, file_output):
    execution('openssl rsautl -encrypt -pubin -inkey ' + pub_key + ' -in ' + file_to_encrypt + ' -out ' + file_output)


def decrypt_rsa(priv_key, file_to_decrypt, file_output):
    execution('openssl rsautl -decrypt -inkey ' + priv_key + ' -in ' + file_to_decrypt + ' -out ' + file_output)


# Encrypt AES - Node Protocol + CA Protocol

def encrypt_aes(pub_key, file_to_encrypt, file_output):
    execution('openssl enc -aes-256-cbc -pass file:' + pub_key + ' -in ' + file_to_encrypt + ' -out ' + file_output + ' -pbkdf2')


def decrypt_aes(priv_key, file_to_decrypt, file_output):
    execution('openssl enc -aes-256-cbc -d -pass file:' + priv_key + ' -in ' + file_to_decrypt + ' -out ' + file_output + ' -pbkdf2')


# Execution commands

def execution(command):
    try:
        if os.system(command) != 0:
            raise Exception('Failed command')
        return True
    except:
        print('Failed command')
        return False


