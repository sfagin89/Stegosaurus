from PIL import Image

# Set Debug State
# 1 = On, 0 = Off
debug = 1

# Function to convert Message ASCII to Binary
# Returns list of binary values
def asciiToBinary(msg_ascii):
    msg_bin = []

    for i in msg_ascii:
        msg_bin.append(format(ord(i), '08b'))
    return msg_bin

def shiftPixelValue(pixel, msg_ascii):
    msg_bin = asciiToBinary(msg_ascii)
    msg_len = len(msg_bin)
    img_data = iter(pixel)

    for i in range(msg_len):
        pixel = [value for value in img_data.__next__()[:3] + img_data.__next__()[:3] + img_data.__next__()[:3]]

        for j in range(0, 8):
            if (msg_bin[i][j] == '0' and pixel[j]% 2 != 0):
                pixel[j] -= 1
            elif (msg_bin[i][j] == '1' and pixel[j]% 2 == 0):
                if (pixel[j] != 0):
                    pixel[j] -= 1
                else:
                    pixel[j] += 1

        if (i == (msg_len - 1)):
            if (pixel[-1] % 2 == 0):
                if(pixel[-1] != 0):
                    pixel[-1] -= 1
                else:
                    pixel[-1] += 1
        else:
            if (pixel[-1]% 2 != 0):
                pixel[-1] -= 1

        pixel = tuple(pixel)
        yield pixel[0:3]
        yield pixel[3:6]
        yield pixel[6:9]

def encode_enc(img_new, msg_ascii):
    wr = img_new.size[0]
    (x,y) = (0,0)

    for pixel in shiftPixelValue(img_new.getdata(), msg_ascii):
        img_new.putpixel((x,y), pixel)
        if (x == wr - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode(img, msg):
#    if debug:
#        print("Encoding Data Into Image")

    #img = input("Enter image name (with extension): ")
    image = Image.open(img, 'r')

    #msg = input("Enter data to be encoded: ")
    if (len(msg) == 0):
        raise ValueError('Data is empty')

    img_new = image.copy()
    encode_enc(img_new, msg)

    #img_new_name = input("Enter the name of the new image (with extension): ")
    img_new_name = "encoded_"+img
    img_new.save(img_new_name, str(img_new_name.split(".")[1].upper()))

def decode(img):
    if debug:
        print("Decoding Data From Image")

    #img = input("Enter image name (with extension): ")
    image = Image.open(img, 'r')

    msg = ''
    img_data = iter(image.getdata())

    while (True):
        pixels = [value for value in img_data.__next__()[:3] + img_data.__next__()[:3] + img_data.__next__()[:3]]
        msg_bin = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                msg_bin += '0'
            else:
                msg_bin += '1'

        msg += chr(int(msg_bin, 2))
        if (pixels[-1] % 2 != 0):
            return msg

def main():
    a = int(input("1. Encode\n2. Decode\n"))
    if (a == 1):
        img = input("Enter image name (with extension): ")
        msg = input("Enter data to be encoded: ")
        encode(img, msg)
    elif (a == 2):
        img = input("Enter image name (with extension): ")
        print("Decoded Message: " + decode(img))
    else:
        raise Exception("Enter correct input")

if __name__ == '__main__':
    main()
