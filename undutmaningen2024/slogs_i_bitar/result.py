import PIL.Image
import base64
import re
import matplotlib.pyplot as plt
import numpy as np
import struct

## Histogram 
def make_histogram(image):
    data = np.array(image)  

    # Make Grayscale
    if len(data.shape) == 3:
        # RGB
        data = np.mean(data, axis=2)  

    # Show histogram
    plt.hist(data.ravel(), bins=256, range=[0, 256], color='gray', alpha=0.75)
    plt.title('Pixle values')
    plt.xlabel('Pixel values')
    plt.ylabel('Frequency')
    plt.show()

## Reverse bits 
def reverse_bits(byte):
    reversed_byte = 0
    for _ in range(8):
        reversed_byte = (reversed_byte << 1) | (byte & 1)
        byte >>= 1
    return int(reversed_byte)

## Count odd even bytes
def analyze_bytes(image):
    image_bytes = image.tobytes()
    # Count number of even and odd bytes 
    even_count = sum(1 for byte in image_bytes if byte % 2 == 0)
    odd_count = len(image_bytes) - even_count  

    print("Even bytes", even_count)
    print("Odd bytes:", odd_count)

# Open the image file

def decode_image(image):
    # Convert the image to bytes
    image_bytes = image.tobytes()

    # Extract bytes where the least significant bit is not set
    reversed_bytes = bytes(
        reverse_bits(byte)
        for byte in image_bytes 
        if (byte % 2 == 0)  # Use even bytes 
    )

    secretText = reversed_bytes.decode().split("THISISJUSTPADDINGPLEASEIGNORE")[0]

    print(secretText)

    # Regexp to get the base64-encoded part and decode to ISO-8859-1
    pattern = r'(?=.*[a-z0-9+/|])[A-Za-z0-9+/]{22,}(?:={1,2})?'
    b64data = ''.join(re.findall(pattern, secretText))
    decoded_bytes = base64.b64decode(b64data)
    decoded_str = decoded_bytes.decode('ISO-8859-1')  

    print(decoded_str)
   

image = PIL.Image.open("result.png")
#make_histogram(image)
analyze_bytes(image)
decode_image(image)
