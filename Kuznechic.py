from TEXT_to_HEX import hex_to_text, text_to_hex
from generating_round_keys import encrypt, decrypt, gen_round_keys, int_to_hex, hex_to_int, block_to_xor
from private_key_generator import gen_gamma, generate_random_key
import textwrap


# Упаковка входных данных в список поблочно по 128 бит

def to_pack_data(text):
    chip_box = textwrap.wrap(text, 32)
    i = len(chip_box)
    if len(chip_box[i - 1]) < 32:
        x = 32 - len(chip_box[i - 1])
        last_chip = chip_box[i - 1]
        last_chip = last_chip + '0' * x
        chip_box[i - 1] = last_chip
    return chip_box


# Шифрование в режиме гаммирования по ГОСТ-34.13-2015

def gamma_mode_encrypt(data, round_keys, gamma):
    chip_data_block = ''
    for i in range(len(data)):
        gamma = gamma[:len(gamma) - len(str(i))]
        gamma = gamma + str(i)
        chip_gamma = encrypt(gamma, round_keys)
        data_n = hex_to_int(data[i])
        chip_data = block_to_xor(chip_gamma, data_n)
        chip_data = int_to_hex(chip_data)
        chip_data_block += chip_data
    return chip_data_block


# Расшифрование в режиме гаммирования по ГОСТ-34.13-2015

def gamma_mode_decrypt(chip, round_keys, gamma):
    open_text = ''
    for i in range(len(chip)):
        gamma = gamma[:len(gamma) - len(str(i))]
        gamma = gamma + str(i)
        chip_gamma = encrypt(gamma, round_keys)
        data_n = hex_to_int(chip[i])
        message = block_to_xor(data_n, chip_gamma)
        open_text += int_to_hex(message)
    return open_text


# Аналог встроенной функции wrap
# def to_wrap(text):
#     cnt = 0
#     chip_box = []
#     chip = ''
#     x = 0
#     for i in range(len(text)):
#         cnt += 1
#         m = cnt % 32
#         chip += text[i]
#         if cnt == 32:
#             chip_box.append(chip[0:cnt])
#             x = cnt
#             chip = ''
#         elif m == 0 and cnt > 32:
#             chip_box.append(text[x:cnt])
#             x = cnt
#             chip = ''
#         elif m != 0 and cnt == len(text):
#             chip_box.append(text[x:])
#     return chip_box


