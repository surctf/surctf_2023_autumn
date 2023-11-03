import collections
import itertools

def analyze_text(text):
    letter_frequencies = collections.Counter(text)

    sorted_frequencies = sorted(letter_frequencies.items(), key=lambda x: x[1], reverse=True)

    for letter, frequency in sorted_frequencies:
        return letter

with open("RUVigenere.txt", "r") as f:
    text = f.readline()

found = False

for key_len in range(2,10):

    print(f'Длина ключа: {key_len}')

    parts_of_text = []
    for i in range(key_len):
        d=''
        for j in range(i, len(text), key_len):
            d += text[j]
        parts_of_text.append(d)

    ru_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    most_common_letters = ['о','е','а','и']

    decoded_parts_of_text = []
    for part in range(len(parts_of_text)):
        letter = analyze_text(parts_of_text[part])
        enc = ru_alphabet.find(letter)

        better_rots = []
        for better in most_common_letters:
            dec = ru_alphabet.find(better)

            if dec > enc:
                rot = len(ru_alphabet) - dec + enc
                better_rots.append(rot)

            else:
                rot = enc - dec
                better_rots.append(rot)


        decoded_part_variants = []
        for rot in better_rots:
            decoded_part = ''
            for i in parts_of_text[part]:
                enc = ru_alphabet.find(i)

                if rot > enc:
                    index = len(ru_alphabet) - rot + enc
                else:
                    index = enc - rot

                decoded_part += ru_alphabet[index]

            decoded_part_variants.append(decoded_part)
        decoded_parts_of_text.append(decoded_part_variants)

    len_part_of_text = len(parts_of_text[0])

    new_list = [
        [decoded_parts_of_text[i][j] for i, j in enumerate(indices)]
        for indices in itertools.product(range(len(most_common_letters)), repeat=key_len)
    ]

    for z in range(len(new_list)):
        decoded_text = ''
        for i in range(len_part_of_text):
            for j in range(len(new_list[z])):
                try:
                    decoded_text += new_list[z][j][i]
                except IndexError:
                    continue

        if ('сурктф' in decoded_text) or ('сурцтф' in decoded_text):
            print(f'Текст: {decoded_text}')
            found = True

    if found:
        break

    print('Nope')
