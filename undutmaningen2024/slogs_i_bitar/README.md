## Challange 

Kettil "The Pot" Halfdanson, the resistance's top potter, has disappeared, and his workshop is a complete mess. Harriet suspects that one of the smashed pots might be a clue, but to be sure, she needs to gather all the pieces. Help her! The pieces might be hard to find, but most are probably right in front of your eyes.

Hint: Some bytes may need to be reversed, but which ones?

![Included image](slogs_i_bitar/result.png)

### Solve

Try histogram or analyze the image bytes. 

## Analyze bytes in the image 
```
image_bytes = image.tobytes()
# Count number of even and odd bytes 
even_count = sum(1 for byte in image_bytes if byte % 2 == 0)
odd_count = len(image_bytes) - even_count  
```

```
Even bytes 7556  <-- Decoded data
Odd bytes: 131573
```

## Reverse order of even bytes 

01110010 --> 01001110   --- LSB = 0 (Even byte) 
       
```
reversed_byte = 0
for _ in range(8):
   reversed_byte = (reversed_byte << 1) | (byte & 1)
   byte >>= 1
return int(reversed_byte)
```
Flag is in the decoded bytes

## Decode the second message

Second message is just base64-encoded in the first message

```
Henrietta and Gerald had ran in circles for hours trying to pick up all the tiny
little pieces from the ground. "I'm sorry, I'm so sorry", cried Gerald as he
frantically searched the grass, "I didn't mean to break it". As the sun slowly
began to set, Henrietta took a last look under the table.
"Here it is!" she blurted out. This is such a nice suprise,
we didn't have to be so fright, the last bit was hidden in plain sight,
almost like playing tag, here's your flag:

    undut{XXXXXXX}

Gerald helped Henrietta glue and put the pot together again the next morning.
After they matched up all pieces, some alpha numerical symbols emerged
wrapping around the clay pot.

     (################################)
     /                                \
    /__________________________________\
   |     _________________________      |
   |    /                         \     |
   |   (  To Harald, from Mommy<3  )    |
   |    \_________________________/     |
   |                                    |
   |ICAgICAvIFwKICAgIC8gXyBcCiAgIHwgLyBcIHwKICAgfHwgICB8fCBfX19fX19fCiAgIHx8ICAgfHwgfFwgICAgIFwKICAgfHwgICB8fCB8fFwgICAgIFwKICAgfHwgICB8fCB8fCBcICAgIHwKICAgfHwgICB8fCB8fCAgXF9fLwogICB8fCAgIHx8IHx8ICAgfHwKICAgIFxcXy8gXF8vIFxfLy8KICAgLyAgIF8gICAgIF8gICBcCiAgLyAgICAgICAgICAgICAgIFwKICB8ICAgIE8gICAgIE8gICAgfAogIHwgICBcICBfX18gIC8gICB8CiAvICAgICBcIFxfLyAvICAgICBcCi8gIC0tLS0tICB8ICAtLS0tLSAgXAp8ICAgICBcX18vfFxfXy8gICAgIHwKXCAgICAgICB8X3xffCAgICAgICAvCiBcX19fX18gICAgICAgX19fX18vCiAgICAgICBcICAgICAvCiAgICAgICB8ICAgICB8CgpLb20gdGlsbCBldmVudGV0IHDlIEhpc3Rvcmlza2EgTXVzZWV0IGkgQXByaWwKb2NoIGJlcuR0dGEgb20gZGluIHVuZC11cHBsZXZlbHNlIGb2ciBvc3MhClJlZ2lzdHJlcmEgZGlnIHDlOiBodHRwczovL3VuZHV0bWFuaW5nLnNlLw==|
   |                                    |
   \------------------------------------/
    \    O    O    O    O    O    O    /
     \________________________________/

     / \
    / _ \
   | / \ |
   ||   || _______
   ||   || |\     \
   ||   || ||\     \
   ||   || || \    |
   ||   || ||  \__/
   ||   || ||   ||
    \\_/ \_/ \_//
   /   _     _   \
  /               \
  |    O     O    |
  |   \  ___  /   |
 /     \ \_/ /     \
/  -----  |  -----  \
|     \__/|\__/     |
\       |_|_|       /
 \_____       _____/
       \     /
       |     |

Kom till eventet på Historiska Museet i April
och berätta om din und-upplevelse för oss!
Registrera dig på: https://undutmaning.se/
```

