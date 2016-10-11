import base64
import binascii


def hex_to_b64(hex_str):
    bin_code = binascii.unhexlify(hex_str)
    encoded = base64.b64encode(bin_code)
    return encoded
