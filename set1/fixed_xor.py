def fixed_xor(hex_str1, hex_str2):
    hex1 = int(hex_str1, 16)
    hex2 = int(hex_str2, 16)
    return hex(hex1 ^ hex2)
