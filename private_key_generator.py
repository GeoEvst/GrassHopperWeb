import random


def generate_random_key():
    n = 64
    valid_chars = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    master_key = ''
    master_key_list = random.sample(valid_chars, n)

    for i in range(len(master_key_list)):
        master_key = master_key + master_key_list[i]

    return master_key


def gen_gamma():
    n = 16
    valid_chars = "0123456789abcdef"
    gamma = ''
    gamma_list = random.sample(valid_chars, n)
    for i in range(len(gamma_list)):
        gamma = gamma + gamma_list[i]
    return gamma

