
import hashlib
from Crypto.Util.number import bytes_to_long, long_to_bytes
from gmpy2 import iroot
from Crypto.Hash import SHA256, SHA1
import re
from pwn import *

#   According to Bleichenbachers #06 RSA signing vunarbility  
#   for small e, e=3 a signature can be forged by using the following scheme
#   0x00 0x01 0xff ... 0xff 0x00 ANS.1 HASH SHA1(m) GARBAGE(not 0xff)

asn1_headers_by_type = {
    "MD2": bytes.fromhex("3020300c06082a864886f70d020205000410"),
    "MD5": bytes.fromhex("3020300c06082a864886f70d020505000410"),
    "SHA-1": bytes.fromhex("3021300906052b0e03021a05000414"),
    "SHA-256": bytes.fromhex("3031300d060960864801650304020105000420"),
    "SHA-384": bytes.fromhex("3041300d060960864801650304020205000430"),
    "SHA-512": bytes.fromhex("3051300d060960864801650304020305000440")
}

def forge_signature(message, key_len, e):
    prefix = b'\x00\x01\xff\x00'   
    asn1Header = asn1_headers_by_type["SHA-1"]
    hash_message = hashlib.sha1(message).digest()
    block = prefix + asn1Header + hash_message
    block += ((key_len // 8) - len(block)) * b'\x3c'
    forged_sig = iroot(bytes_to_long(block), e)[0] + 1
    return hex(forged_sig + 1)[2:]

def forge_signature_padding(message, key_len, e):
    prefix = b'\x00\x01\xff'   
    asn1Header = asn1_headers_by_type["SHA-1"]
    hash_message = hashlib.sha1(message).digest()
    padding = ((key_len // 8) - len(prefix + asn1Header + hash_message)  - 1) * b'\xc3'
    padding += b'\x09\x00'
    block = prefix + padding + asn1Header + hash_message
    print(f"len{len(block)}")
    forged_sig = iroot(bytes_to_long(block), e)[0] - 1
    return hex(forged_sig + 1)[2:]

def pwn():
    #s = remote('0.cloud.chals.io', 17352)  
    s = remote('localhost', 3000)
    response = s.recv()
    s.sendline("1".encode())
    response = s.recv().decode()
    message = response.split('\n')[2].strip()
    print(f"Meddelande som ska signeras: {message}")

    signature = forge_signature_padding(bytes.fromhex(message), 1024, 3)
    
    print(signature.encode('utf-8'))

    s.sendline(signature.encode('utf-8'))
    response = s.recv(1024)

    print(response)

pwn()