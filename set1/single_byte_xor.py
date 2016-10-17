import binascii
from functools import partial
from string import ascii_letters


def xor(msg, ltr):
    """XOR msg against given letter.

    Takes a hex-encoded string, XOR it against the ord of a given letter,
    returns the result in raw bytes.
    """

    msg_xord = ''
    ltr_ord = ord(ltr)

    n = len(msg)
    # Each letter corresponds to two hex chars.
    for i in range(0, n - 1, 2):
        msg_bits = int(msg[i:i+2], 16)
        # XOR the two hex vs ltr, encode result in hex, leave out prefix '0x'
        msg_bits_xord = hex(msg_bits ^ ltr_ord)[2:]
        # If single digit, pad with zero
        msg_padded = msg_bits_xord.rjust(2, '0')
        msg_xord += msg_padded

    return binascii.unhexlify(msg_xord)


def get_freq_score(phrase):
    """Return the frequency score of a phrase.

    Based on the freq ranking of each letter in the English language, score
    the phrase based on the letters it contains. A higher score means a
    closer resemblance to the natural frequencies.
    """
    freq_rank = {
        'a': .0651738, 'b': .0124248, 'c': .0217339, 'd': .0349835,
        'e': .1041442, 'f': .0197881, 'g': .0158610, 'h': .0492888,
        'i': .0558094, 'j': .0009033, 'k': .0050529, 'l': .0331490,
        'm': .0202124, 'n': .0564513, 'o': .0596302, 'p': .0137645,
        'q': .0008606, 'r': .0497563, 's': .0515760, 't': .0729357,
        'u': .0225134, 'v': .0082903, 'w': .0171272, 'x': .0013692,
        'y': .0145984, 'z': .0007836, ' ': .1918182,
    }

    # Tally total score of phrase based on freq_rank
    total = 0
    for ltr in phrase.lower():
        total += freq_rank.get(chr(ltr), 0)
    # Weight total score by length of phrase
    weighted_total = total / len(phrase)
    return weighted_total


def decipher(msg):
    """XOR msg against all letters in the alphabet.

    Takes a hex-encoded string that has been XOR'ed against a letter. XOR it
    against each letter in A-Z & a-z, analyze the frequencies of letters in
    the resultant decoded string to determine the correct letter.
    """
    xor_msg = partial(xor, msg=msg)
    # Remember the phrase with the highest freq score
    highest_score = 0
    best_phrase = ''
    # Iterate the alphabet, decode message against each letter
    for ltr in ascii_letters:
        decoded_str = xor_msg(ltr=ltr)
        score = get_freq_score(decoded_str)
        if score >= highest_score:
            highest_score = score
            best_phrase = decoded_str

    return best_phrase
