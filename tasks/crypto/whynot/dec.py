from Crypto.Util.strxor import strxor
import string

def is_valid(s):
    valid_chars = set(string.ascii_letters + string.digits + string.punctuation)
    return all(char in valid_chars or char.isspace() for char in s)


with open("output.txt", "r") as f:
    text = f.readline()

unhex_text = b''.fromhex(text)

len_unhex_text = len(unhex_text)

for i in range(13, 38):
    if len_unhex_text % i == 0:
        a={}

        len_flag = len_unhex_text // i
        for j in range(len_unhex_text):
            if j % i == 0:
                a[j % len_flag] = unhex_text[j]


        if len_flag == len(a):
            items = (dict(sorted(a.items()))).values()
            output=b''
            for m in items:
                output += bytes([m])


            for output_text in range(0,256):
                flag = strxor(output, bytes([output_text])*len_flag)

                try:
                    string_flag = flag.decode('utf-8')
                except UnicodeDecodeError:
                    continue

                for word in string_flag.split():
                    if is_valid(word):
                        print(word)
