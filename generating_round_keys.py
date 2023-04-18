from iterative_constants import generate_iter_consts, generate_table_galois, multiply_in_galois_field
import time
# t0 = time.process_time()

# Ряд Галуа

galois_row = (1, 148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148)

# Таблица нелинейного преобразования Кузнечика (s-box)
# Прямого

s_box = (252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77,
         233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193,
         249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79,
         5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31,
         235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204,
         181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135,
         21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177,
         50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87,
         223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3,
         224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74,
         167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65,
         173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59,
         7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137,
         225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97,
         32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82,
         89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182)

# обратного
s_box_inv = (165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158, 57, 85, 126, 82, 145,
             100, 3, 87, 90, 28, 96, 7, 24, 33, 114, 168, 209, 41, 198, 164, 63, 224,
             39, 141, 12, 130, 234, 174, 180, 154, 99, 73, 229,66, 228, 21, 183, 200,
             6, 112, 157, 65, 117, 25, 201, 170, 252, 77, 191, 42, 115, 132, 213, 195,
             175, 43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212, 15, 156, 47, 155,
             67, 239, 217, 121, 182, 83, 127, 193, 240, 35, 231, 37, 94, 181, 30, 162, 223,
             166, 254, 172, 34, 249, 226, 74, 188, 53, 202, 238, 120, 5, 107, 81, 225, 89,
             163, 242, 113, 86, 17, 106, 137, 148, 101, 140, 187, 119, 60, 123, 40, 171, 210,
             49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46, 54, 219, 105, 179, 20, 149,190,
             98, 161, 59, 22, 102, 233, 92, 108, 109, 173, 55, 97, 75, 185, 227, 186, 241, 160,
             133, 131, 218, 71, 197, 176, 51, 250, 150, 111, 110, 194, 246, 80, 255, 93, 169, 142,
             23, 27, 151, 125, 236, 88, 247, 31, 251, 124, 9, 13, 122, 103, 69, 135, 220, 232, 79,
             29, 78, 4, 235, 248, 243, 62, 61, 189, 138, 136, 221, 205, 11, 19, 152, 2, 147, 128,
             144, 208, 36, 52, 203, 237, 244, 206, 153, 16, 68, 64, 146, 58, 1, 38, 18, 26, 72,
             104, 245, 129, 139, 199, 214, 32, 10, 8, 0, 76, 215, 116)


# Преобразование из HEX в десятичное число

def hex_to_int(x):
    cnt = 2
    block = []
    for i in range(len(x)//2):
        x_1 = x[2 * i:cnt]
        cnt += 2
        x_i = int(x_1, 16)
        block.append(x_i)
    return block


# Преобразование из десятичного числа в HEX

def int_to_hex(bytes_list):
    block_hex = ''
    for i in range(len(bytes_list)):
        y = hex(bytes_list[i])[2:]
        if len(y) < 2:
            block_hex += '0' + y
        else:
            block_hex += y
    return block_hex


# Сложение блоков по модулю 2 (Побитовый XOR)

def block_to_xor(left_block, right_block):
    x_conv = []
    for i in range(16):
        x_conv.append(left_block[i] ^ right_block[i])
    return x_conv


# Линейное преобразование (L - преобразование)

def l_conv(x):
    for i in range(16):
        xor_byte = 0
        for j in range(16):
            byte = multiply_in_galois_field(x[i + j], galois_row[j])
            xor_byte = xor_byte ^ byte
        x.append(xor_byte)
    return x[16:]


# Сложение по модулю 2 и нелинейное преобразование (X, S - преобразование)

def x_s_conversion(k_1, c_n):
    x_conv = block_to_xor(k_1, c_n)
    s_conversion = []
    s_x_s = ''
    for i in range(16):
        s_conversion.append(s_box[x_conv[i]])
        s_x_s += hex(s_box[x_conv[i]])[2:]
    return s_conversion


def s_conversion_inv(k_1):
    s_conversion = []
    s_x_s = ''
    for i in range(16):
        s_conversion.append(s_box_inv[k_1[i]])
        s_x_s += hex(s_box[k_1[i]])[2:]
    return s_conversion


# Функция формирования десяти раундовых ключей (X, S, L - преобразования на основе мастер ключа и итерационных констант)

def gen_round_keys(key):
    round_keys = []
    key = hex_to_int(key)
    round_keys.append(key[:16])
    round_keys.append(key[16:])
    constants = generate_iter_consts()

    for i in range(32):
        k = key[:16]
        left = key[:16]
        right = key[16:]
        left = x_s_conversion(left, constants[i])
        left.reverse()
        left = l_conv(left)
        left.reverse()
        left = block_to_xor(left, right)
        left.extend(k)
        key = left
        if (i + 1) % 8 == 0:
            round_keys.append(key[:16])
            round_keys.append(key[16:])
    return round_keys


# Функция шифрования
def encrypt(text, key):
    text = hex_to_int(text)
    for i in range(10):
        if i != 9:
            x = x_s_conversion(text, key[i])
            x.reverse()
            x = l_conv(x)
            x.reverse()
            text = x
        else:
            text = block_to_xor(text, key[i])
    return text


# Функция расшифрования
def decrypt(text, key):
    text = hex_to_int(text)
    for i in range(10):
        if i != 9:
            x = block_to_xor(text, key[9 - i])
            s = l_conv(x)
            s = s_conversion_inv(s)
            text = s
        else:
            text = block_to_xor(key[9 - i], text)
    return text


round_key = gen_round_keys('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef')
open_text = '1122334455667700ffeeddccbbaa9988'
# open_text = hex_to_int(open_text)
# encrypted_block = encrypt(open_text, round_key)
# ans = decrypt(encrypted_block, round_key)
#
# print(int_to_hex(encrypted_block))
# print(int_to_hex(ans))

# t1 = time.process_time() - t0
# # CPU seconds elapsed (floating point)
# print("Time elapsed: ", t1 - t0)
