from pwn import *
import Crypto.Util.number as cun

# Configuration
REMOTE_IP = "challs.umdctf.io"
REMOTE_PORT = 32345
CIPHERTEXT_HEX = "d697937950b3090d56828170609a3b23f836e3cc0ed631cb9ce08c4b9785f5f3db5dee5f44adaad3630303062b61d5fa"
IV_HEX = "2652b7ae08b281594c488cf2e6daee43"
BLOCK_SIZE = 16

ciphertext = bytes.fromhex(CIPHERTEXT_HEX)
iv = bytes.fromhex(IV_HEX)
blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
blocks.insert(0, iv)

def xor_bytes(ciphertext_bytes, key_bytes):
    xored_bytes = bytes(a ^ b for a, b in zip(ciphertext_bytes, key_bytes))
    return xored_bytes

def decode_with_oracle():
    imm = []

     # Oracle is not super stable so using a file to collect the intermidiate keys
    with open('imm_keys.txt', 'w') as file:
        pass  

    # In every attemp we forge an IV and include the current block in the request (unchanged)
    # IV starts with a padding "0101010101" where 01 is the value of the current byte that is beeing processed in the forged IV 

    for i in range(len(blocks) - 1, 0, -1):  # Starts at the last block and moves backwards
        im_key = 0 
        ref_block = blocks[i] 
        validated_bytes = b''

        r = remote(REMOTE_IP, REMOTE_PORT)
        print(r.recv())

        zero_iv = [0] * BLOCK_SIZE

        for pos in range(1, BLOCK_SIZE + 1):
            padding_iv = [pos ^ b for b in zero_iv]
            
            for k in range(255, 0, -1):
                padding_iv[-pos] = k
                mod_block = bytes(padding_iv)
                payload = mod_block + ref_block
                #print(f"pos: {pos} k: {k} payload {payload.hex()}")
                
                r.sendline(payload.hex().encode())
                reply = r.recv()
                #print(reply)

                if "valid padding :)" in reply.decode():  # Make sure to decode bytes to str

                    # It is possible to get a false positive at pos 
                    # So there is an extra check to handle that 
                     
                    if pos == 1:
                        mod_block = bytearray(mod_block)  
                        mod_block[-2] ^= 1  
                        mod_block = bytes(mod_block)
                        payload = mod_block + ref_block
                        r.sendline(payload.hex().encode())
                        reply = r.recv()
                        if not "valid padding :)" in reply.decode():
                            continue
                    print(f"Byte: {pos} value: {hex(k)} payload {payload.hex()}")
                    break
            else:
                raise Exception("no valid padding byte found (is the oracle working correctly?)")

            zero_iv[-pos] = k ^ pos
            
        # We are done with one round let's do next
        r.close()
        imm.append(bytes(zero_iv))
            
        for imm_count in range(len(imm)):
            print(f"Imm: {imm[imm_count].hex()}")

        with open('imm_keys.txt', 'a') as file:
            file.write(f"Imm: {imm[len(imm)-1].hex()}\n")

def main():
   
    decode_with_oracle()

    ''' This oracle is a bit unstable - using a file to save some time '''
    imm = []
    with open('imm_keys.txt', 'r') as file:
        for line in file:
            imm.append(bytes.fromhex(line.split("Imm: ")[1]))

    str = "" 
    for i in range(0, len(imm)):
        print(f"Decode block {i} with imm {len(imm)-i-1} ")
        str += xor_bytes(blocks[i], imm[-i-1]).decode('utf-8')
    print(str)
    
if __name__ == "__main__":
    main()