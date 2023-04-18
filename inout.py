from Kuznechic import gamma_mode_encrypt, gamma_mode_decrypt, to_pack_data
from generating_round_keys import encrypt, decrypt, hex_to_int, int_to_hex, gen_round_keys
from TEXT_to_HEX import text_to_hex, hex_to_text


def kuz_encrypt(text, key):
    master_key = key
    round_keys = gen_round_keys(master_key)
    data = text
    chip = encrypt(data, round_keys)
    return int_to_hex(chip)


def kuz_decrypt(text, key):
    master_key = key
    round_keys = gen_round_keys(master_key)
    data = text
    res = decrypt(data, round_keys)
    return int_to_hex(res)


def gam_encrypt(text, key, IV):
    master_key = key
    round_keys = gen_round_keys(master_key)
    data = to_pack_data(text)
    gamma = IV + '0' * 16
    chip = gamma_mode_encrypt(data, round_keys, gamma)
    return chip


def gam_decrypt(text, key, IV):
    master_key = key
    round_keys = gen_round_keys(master_key)
    data = to_pack_data(text)
    gamma = IV + '0' * 16
    res = gamma_mode_decrypt(data, round_keys, gamma)
    return res


def text_encrypt(text, key, IV):
    master_key = key
    round_keys = gen_round_keys(master_key)
    text = text_to_hex(text)
    data = to_pack_data(text)
    preamble = (len(data) * 32 - len(text))
    gamma = IV + '0' * 16
    chip = gamma_mode_encrypt(data, round_keys, gamma)
    if len(str(preamble)) < 2:
        chip = '0' + str(preamble) + chip
    else:
        chip = str(preamble) + chip
    return chip


def text_decrypt(chip, key, IV):
    preamble = chip[:2]
    chip = chip[2:]
    master_key = key
    round_keys = gen_round_keys(master_key)
    chip_data = to_pack_data(chip)
    gamma = IV + '0' * 16
    text = gamma_mode_decrypt(chip_data, round_keys, gamma)
    text = text[:-int(preamble)]
    text = hex_to_text(text)
    return text





