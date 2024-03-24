## 
## We got some insights from the malicious rar-file that was sent to the victims computer.
## In a jpg-file there is a script hidden. It is reovered from reading the end of the file
## by doing xor on two bytes from two lists in the JPG-file
##  segment_k = image_data[-4934:-2467]
##  segment_v = image_data[-2467:]
## 
## To exctract the JPG-file use tshark: 
## tshark -r raring.pcap -Y "http.response and http.content_type contains \"image/jpeg\"" -T fields -e http.file_data
## 
## Pipe the data from tshark directly:
## tshark -r raring.pcap -Y "http.response and http.content_type contains \"image/jpeg\"" -T fields -e http.file_data | python3.9 decrypt_img.py

import sys

def extract_hidden_data(image_data):
    # Extract the two data segments from the end of the file.
    segment_k = image_data[-4934:-2467]
    segment_v = image_data[-2467:]

    # Return the extracted segments.
    return segment_k, segment_v

def xor_and_convert(k, v):
    if len(k) != len(v):
        raise ValueError("The lists must be of the same length")

    # Perform bitwise XOR between corresponding elements in k and v
    xor_result = [k[i] ^ v[i] for i in range(len(k))]

    # Convert the result to an ASCII string
    result_str = ''.join(chr(num) for num in xor_result)

    return result_str

# Check if there is data to read from standard input
if not sys.stdin.isatty():
    # Data is being piped in, read from standard input
    input_source = sys.stdin
    print("Read data from stdin")
else:
    # No data is being piped in, open and read from a file instead
    filename = 'imgHex.txt'
    input_source = open(filename, 'r')

hex_data = input_source.read().strip()

# Convert to binary format
binary_data = bytes.fromhex(hex_data)

# Use the extract_hidden_data function to extract the hidden data segments
segment_k, segment_v = extract_hidden_data(binary_data)

# Use xor_and_convert to decrypt and convert the data
hidden_code = xor_and_convert(segment_k, segment_v)

print("Hidden code: ", hidden_code)
