degrees_galois_field = [[0, 1], [1, 2]]
galois_row = [1, 148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148]


# Генерация таблицы степеней поля Галуа GF(256) / Generating a table of degrees of the Galois field GF(256)
def generate_table_galois():
    degree = []
    for i in range(2, 256):
        degree.append(i)
        x = degrees_galois_field[i - 1][1]
        add = x * 2
        if add > 255:
            add = (add ^ 195) - 256
            degree.append(add)
        else:
            degree.append(add)
        degrees_galois_field.append(degree)
        degree = []
    return degrees_galois_field


# Умножение в поле Галуа / multiplication in the galois field
def multiply_in_galois_field(x, y):
    x1 = 0
    y1 = 0
    result = 0
    if x == 0 or y == 0:
        result = 0
        return result
    for i in range(256):
        if x == galois_field[i][1]:
            x1 = galois_field[i][0]
            break
    for i in range(256):
        if y == galois_field[i][1]:
            y1 = galois_field[i][0]
            break
    z = x1 + y1
    if z > 255:
        z = z - 255
    for i in range(256):
        if z == galois_field[i][0]:
            result = galois_field[i][1]
    return result


# Генерация итерационных констант по ГОСТ Р 34.12-2015

def generate_iter_consts():
    iterative_consts = []
    for _ in range(1, 33):
        x_const = []
        constant = [0 for k in range(15)]
        constant.append(_)
        byte = 0
        shift = 0
        iter_constant = []
        for i in range(16):
            byte = multiply_in_galois_field(constant[i], galois_row[i])
            if byte != 0:
                constant.append(byte)
                shift += 1

        for k in range(14):
            xor_byte = 0
            for i in range(16):
                byte = multiply_in_galois_field(constant[i + shift], galois_row[i])
                iter_constant.append(byte)
                xor_byte = xor_byte ^ byte
            constant.append(xor_byte)
            shift += 1

        const_1 = constant[15:]
        const_1.reverse()
        # print(const_1)
        # ans = ''
        # for i in range(len(const_1)):
        #     x = hex(const_1[i])[2:]
        #     if len(x) < 2:
        #         ans = ans + '0' + x
        #     else:
        #         ans = ans + x
        # x_const.append('C' + str(_))
        # x_const.append(ans)
        iterative_consts.append(const_1)
    return iterative_consts


galois_field = generate_table_galois()
iterative_constants = generate_iter_consts()
# print(iterative_constants)

