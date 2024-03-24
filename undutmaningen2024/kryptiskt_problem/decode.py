from pwn import *
import requests

#
#   Get content from a https-website 
#

def get_website(url):
    reply = ""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Successfully connected to the website")
            reply = response.text
        else:
            print(f"Failed to retrieve the website, status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return reply 
    
#
#   Get the PCAP-file from the wierd service running on port 29182
#   Send first 127 byte from the key to get 127 decrypted bytes. 
#   Then included 127 decrypted bytes + 127 bytes of the key in the next reques and so on... 
#

def get_pcap_file(key):
    host = 'ebefa92f.0x4d555354.se'
    port = 29182
    enclen = 127
    recv_bytes = b''

    key = bytes.fromhex(key)
    print(f"Key length: {len(key)}")
  
    while len(recv_bytes) < len(key):
        requestChunk = recv_bytes + key[len(recv_bytes):len(recv_bytes) + enclen]
        io = remote(host, port)
        io.send(requestChunk)
        print(requestChunk)
        reply = io.recvall(timeout=1.5)
        recv_bytes += reply[len(recv_bytes):len(recv_bytes) + enclen]

    print(recv_bytes)

    open('985_BT.PCAP', 'wb').write(recv_bytes)

#
#   XOR two stings - Vernam style 
#

def hex_xor(hex1, hex2):
    bytes1 = bytes.fromhex(hex1)
    bytes2 = bytes.fromhex(hex2)
    
    xor_result = bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))
    
    try:
        return xor_result.decode('utf-8')
    except UnicodeDecodeError:
        return "Result cannot be decoded to UTF-8"

#
#   Dump data from tshark for a given stream number
#

def run_tshark(number):
    command = "tshark -r 985_BT.PCAP -Y 'frame.number == " +  str(number) + "' -V | grep 'Data: ' | awk -F': ' '{print $2}'"

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print("Command output:")
            print(result.stdout)
        else:
            print("Error:")
            print(result.stderr)
        
        return result.stdout

    except Exception as e:
        print("Error occured while running tshark")
        print(str(e))

    return ""

def matchFlag(text):
    pattern = r'undut{[A-Za-z0-9]+}'
    matches = re.findall(pattern, text)
    return matches

def matchHexAscii(text):
    pattern = r'\b[0-9a-fA-F]{20,}'
    matches = re.findall(pattern, text)
    return matches

if __name__ == '__main__':

    # Get the key from website 
    site_data = get_website("https://ebefa92f.0x4d555354.se/")
    matches = matchHexAscii(site_data)
    result = ''.join(matches)  

    # Get the file by using the key 
    get_pcap_file(result)
    
    # Get echo request/response (packet 15 and 16)
    str1 = run_tshark(15)
    str2 = run_tshark(16)

    # XOR result 
    result = hex_xor(str1, str2)
    print("XOR Result: ", matchFlag(result))
