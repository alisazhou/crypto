import binascii
from collections import Counter, defaultdict
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


def get_freq_rank():
    """Generate a ranking system based on freq of each letter in English.

    The more frequent a letter appears in the language, the higher its score.
    """

    freq_order = 'etaoinshrdlcumwfgypbvkjxqz'
    freq_rank = defaultdict(int)
    score = 26
    for ltr in freq_order:
        freq_rank[ltr] = score
        score -= 1
    return freq_rank


def get_freq_score(freq_rank, phrase):
    """Return the frequency score of a phrase.

    Based on the freq ranking of each letter in the English language, score
    the phrase based on the letters it contains. A higher score means a
    closer resemblance to the natural frequencies.
    """
    # Transform phrase into lowercase, count each letter's occurrence
    counted = Counter(phrase.lower())
    # Tally total score of phrase based on freq_rank
    total = 0
    for ltr, score in counted.items():
        # Letters in phrase is bytes, needs to be converted to alphabet
        total += freq_rank[chr(ltr)]
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
    # Get the freq rank of the alphabet
    freq_rank = get_freq_rank()

    # Remember the phrase with the highest freq score
    highest_score = 0
    best_phrase = ''
    # Iterate the alphabet, decode message against each letter
    for ltr in ascii_letters:
        decoded_str = xor_msg(ltr=ltr)
        score = get_freq_score(freq_rank, decoded_str)
        if score >= highest_score:
            highest_score = score
            best_phrase = decoded_str

    return best_phrase
