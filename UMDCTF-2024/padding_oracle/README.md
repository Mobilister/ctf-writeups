# Challenge
The Baron used AES128-CBC with PKCS#7 to hide the flag. Can you recover the flag using his padding oracle?

# Solve 

In order to decode the message we will use the padding oracle to leak information about the padding. 

The solution is based on the explaination and code here: 
https://research.nccgroup.com/2021/02/17/cryptopals-exploiting-cbc-padding-oracles/

The general idea is to forge an IV for each block and get feedback from the oracle regarding the padding. 

This is how ecryption with CBC is done. The previous block is the IV of the next block. 

```
      Plaintext block 0      Plaintext block 1
             |                        |
  IV ------- ⊕          'IV --------- ⊕
             |            |           |
             |            |           |
      [Encryption key]    |    [Encryption key] 
             |            |           |
             |------------^           |
             v                        v
      Encdypted block 0        Encrypted block 1   
```

Since we start by forging a IV 01010101..xx the oracle ignore all the leading bytes and only verify the last one. 
It will tell us if the padding is correct or not. The padding can only be correct if we have guessed the correct last byte xx.  

Check the solution in padd.py

```
padding oracle % python3.9 padd.py 
[+] Opening connection to challs.umdctf.io on port 32345: Done
b"welcome!!\ngive me a ciphertext and I'll tell you if the corresponding plaintext has valid padding:\n"
Byte: 1 value: 0xfe payload 010101010101010101010101010100fedb5dee5f44adaad3630303062b61d5fa
Byte: 2 value: 0xfb payload 0202020202020202020202020202fbfddb5dee5f44adaad3630303062b61d5fa
Byte: 3 value: 0x8a payload 030303030303030303030303038afafcdb5dee5f44adaad3630303062b61d5fa
Byte: 4 value: 0x9f payload 0404040404040404040404049f8dfdfbdb5dee5f44adaad3630303062b61d5fa
Byte: 5 value: 0x42 payload 0505050505050505050505429e8cfcfadb5dee5f44adaad3630303062b61d5fa
Byte: 6 value: 0x86 payload 0606060606060606060686419d8ffff9db5dee5f44adaad3630303062b61d5fa
Byte: 7 value: 0xeb payload 070707070707070707eb87409c8efef8db5dee5f44adaad3630303062b61d5fa
Byte: 8 value: 0x98 payload 080808080808080898e4884f9381f1f7db5dee5f44adaad3630303062b61d5fa
Byte: 9 value: 0xce payload 09090909090909ce99e5894e9280f0f6db5dee5f44adaad3630303062b61d5fa
Byte: 10 value: 0x37 payload 0a0a0a0a0a0a37cd9ae68a4d9183f3f5db5dee5f44adaad3630303062b61d5fa
Byte: 11 value: 0xd1 payload 0b0b0b0b0bd136cc9be78b4c9082f2f4db5dee5f44adaad3630303062b61d5fa
Byte: 12 value: 0xe payload 0c0c0c0c0ed631cb9ce08c4b9785f5f3db5dee5f44adaad3630303062b61d5fa
Byte: 13 value: 0xbc payload 0d0d0dbc0fd730ca9de18d4a9684f4f2db5dee5f44adaad3630303062b61d5fa
Byte: 14 value: 0xbe payload 0e0ebebf0cd433c99ee28e499587f7f1db5dee5f44adaad3630303062b61d5fa
Byte: 15 value: 0x72 payload 0f72bfbe0dd532c89fe38f489486f6f0db5dee5f44adaad3630303062b61d5fa
Byte: 16 value: 0x8b payload 8b6da0a112ca2dd780fc90578b99e9efdb5dee5f44adaad3630303062b61d5fa
[*] Closed connection to challs.umdctf.io port 32345
Imm: 9b7db0b102da3dc790ec80479b89f9ff
[+] Opening connection to challs.umdctf.io on port 32345: Done
b"welcome!!\ngive me a ciphertext and I'll tell you if the corresponding plaintext has valid padding:\n"
Byte: 1 value: 0x43 payload 01010101010101010101010101010043f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 2 value: 0x6d payload 02020202020202020202020202026d40f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 3 value: 0xed payload 03030303030303030303030303ed6c41f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 4 value: 0x24 payload 04040404040404040404040424ea6b46f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 5 value: 0x2a payload 05050505050505050505052a25eb6a47f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 6 value: 0xc2 payload 06060606060606060606c22926e86944f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 7 value: 0xe9 payload 070707070707070707e9c32827e96845f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 8 value: 0x1d payload 08080808080808081de6cc2728e6674af836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 9 value: 0x45 payload 09090909090909451ce7cd2629e7664bf836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 10 value: 0x71 payload 0a0a0a0a0a0a71461fe4ce252ae46548f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 11 value: 0x88 payload 0b0b0b0b0b8870471ee5cf242be56449f836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 12 value: 0x3 payload 0c0c0c0c038f774019e2c8232ce2634ef836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 13 value: 0x13 payload 0d0d0d13028e764118e3c9222de3624ff836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 14 value: 0xd3 payload 0e0ed310018d75421be0ca212ee0614cf836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 15 value: 0xd1 payload 0fd1d211008c74431ae1cb202fe1604df836e3cc0ed631cb9ce08c4b9785f5f3
Byte: 16 value: 0xa2 payload a2cecd0e1f936b5c05fed43f30fe7f52f836e3cc0ed631cb9ce08c4b9785f5f3
[*] Closed connection to challs.umdctf.io port 32345
Imm: 9b7db0b102da3dc790ec80479b89f9ff
Imm: b2dedd1e0f837b4c15eec42f20ee6f42
[+] Opening connection to challs.umdctf.io on port 32345: Done
b"welcome!!\ngive me a ciphertext and I'll tell you if the corresponding plaintext has valid padding:\n"
Byte: 1 value: 0x2 payload 01010101010101010101010101010002d697937950b3090d56828170609a3b23
Byte: 2 value: 0x9c payload 02020202020202020202020202029c01d697937950b3090d56828170609a3b23
Byte: 3 value: 0x86 payload 03030303030303030303030303869d00d697937950b3090d56828170609a3b23
Byte: 4 value: 0xa7 payload 040404040404040404040404a7819a07d697937950b3090d56828170609a3b23
Byte: 5 value: 0x81 payload 050505050505050505050581a6809b06d697937950b3090d56828170609a3b23
Byte: 6 value: 0xba payload 06060606060606060606ba82a5839805d697937950b3090d56828170609a3b23
Byte: 7 value: 0x23 payload 07070707070707070723bb83a4829904d697937950b3090d56828170609a3b23
Byte: 8 value: 0x1b payload 08080808080808081b2cb48cab8d960bd697937950b3090d56828170609a3b23
Byte: 9 value: 0x19 payload 09090909090909191a2db58daa8c970ad697937950b3090d56828170609a3b23
Byte: 10 value: 0xf0 payload 0a0a0a0a0a0af01a192eb68ea98f9409d697937950b3090d56828170609a3b23
Byte: 11 value: 0xff payload 0b0b0b0b0bfff11b182fb78fa88e9508d697937950b3090d56828170609a3b23
Byte: 12 value: 0x50 payload 0c0c0c0c50f8f61c1f28b088af89920fd697937950b3090d56828170609a3b23
Byte: 13 value: 0xe0 payload 0d0d0de051f9f71d1e29b189ae88930ed697937950b3090d56828170609a3b23
Byte: 14 value: 0xfd payload 0e0efde352faf41e1d2ab28aad8b900dd697937950b3090d56828170609a3b23
Byte: 15 value: 0x10 payload 0f10fce253fbf51f1c2bb38bac8a910cd697937950b3090d56828170609a3b23
Byte: 16 value: 0x63 payload 630fe3fd4ce4ea000334ac94b3958e13d697937950b3090d56828170609a3b23
[*] Closed connection to challs.umdctf.io port 32345
Imm: 9b7db0b102da3dc790ec80479b89f9ff
Imm: b2dedd1e0f837b4c15eec42f20ee6f42
Imm: 731ff3ed5cf4fa101324bc84a3859e03
Decode block 0 with imm 2 
Decode block 1 with imm 1 
Decode block 2 with imm 0 
UMDCTF{I_l0vE_p@dINg_0rAClE_@tTacKS}\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c\x0c
```
