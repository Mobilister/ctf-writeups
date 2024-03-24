from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import sys

# Use the following tshark command to extract the SSL-traffic:
# tshark -r raring.pcap -Y "tls && ip.addr == 10.0.2.20" -V -T fields -e tcp.payload
# 
# First message in the SSL exchange is a 256 byte encrypted session key
# That is the 16 byte generated sessionKey that we found from the reverse shell script 
# When encrypted with a RSA-key that is 2048 the result will be 256 byte! 
# The session key is then used through out the complete session. 
# Each message will first contain a 16 byte nounce and a 16 byte tag that is included in the payload

# Decrypt the session key given the private key that is located on file
def decrypt_session_key(private_key_path, encryptedSessionKey):
    # Read in the private key
    with open(private_key_path, 'rb') as private_key_file:
        private_key = RSA.import_key(private_key_file.read())

    # Create a PKCS1_OAEP cipher object
    cipher = PKCS1_OAEP.new(private_key)

    # Decrypt the session key
    session_key = cipher.decrypt(encryptedSessionKey)

    return session_key

# Decrypt a single message
def decrypt_AES_GCM(key, nonce, tag, ciphertext):
    cipher = AES.new(key, nonce=nonce, mode=AES.MODE_GCM)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext

private_key_path = 'private.pem'
decrypted_session_key = ""

# Check if there is data to read from standard input
if not sys.stdin.isatty():
    # Data is being piped in, read from standard input
    input_source = sys.stdin
    print("Read data from stdin")
else:
    # No data is being piped in, open and read from a file instead
    filename = 'message.hex'
    input_source = open(filename, 'r')

line_count = 0  # Counter to identify the first line

for line in input_source:
    # Assume that each line contains hex data for nonce, tag, and ciphertext.
    data = line.strip()
    message = bytes.fromhex(data)

    if line_count == 0:
        # The key exchange is made in the first SSL-package (256 bytes)
        decrypted_session_key = decrypt_session_key(private_key_path, message)
        print(len(decrypted_session_key)) 
        line_count += 1  # Increase the counter after the first line has been processed
    else:
        # Update here depending on the exact length of nonce and tag
        nonce = message[:16]
        tag = message[16:32]
        ciphertext = message[32:]

        # Assume that the decrypted_session_key is available and correct.
        plaintext = decrypt_AES_GCM(decrypted_session_key, nonce, tag, ciphertext)
    
        string_data = plaintext.decode('utf-8')
        print(string_data)
