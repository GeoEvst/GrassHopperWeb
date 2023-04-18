# Функции преобразования текста в HEX (UTF-8)

def text_to_hex(text):
    chip = ''
    for i in range(len(text)):
        text_hex = hex(ord(text[i]))
        text_hex = text_hex.replace('x', '')
        if text[i].isascii() is True or text[i].isalnum() is False:
            chip = chip + '0' + text_hex
        else:
            chip = chip + text_hex
    return chip


def hex_to_text(chip):
    hex_box = []
    text = ''
    for i in range(0, len(chip), 4):
        hex_box.append(chip[i:i + 4])
    for i in hex_box:
        text = text + chr(int(i, 16))
    return text


