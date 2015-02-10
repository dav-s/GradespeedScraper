"""
A simple module for decoding and encoding the Gradespeed strings.
"""


keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="


def get_char_safe(string, index, func, oth):
    """
    A helper function to help with evaluating values with chars painlessly.

    :param string: The string to retrieve the character from.
    :param index: The index of the character desired from the string.
    :param func: A function to call with the character retrieved.
    :param oth: An alternate value to return if the function fails.
    :return:
    """
    try:
        return func(string[index])
    except Exception:
        pass
    return oth


def decode_string(to_dec):
    """
    Decodes an encoded string.

    :param to_dec: The string to decode.
    :return: The decoded string.
    """
    output = ""
    i = 0
    while i < len(to_dec):

        enc1 = get_char_safe(to_dec, i, keyStr.find, 0)
        i += 1
        enc2 = get_char_safe(to_dec, i, keyStr.find, 0)
        i += 1
        enc3 = get_char_safe(to_dec, i, keyStr.find, 0)
        i += 1
        enc4 = get_char_safe(to_dec, i, keyStr.find, 0)
        i += 1
        
        chr1 = (enc1 << 2) | (enc2 >> 4)
        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2)
        chr3 = ((enc3 & 3) << 6) | enc4

        output += chr(chr1)
        
        if enc3 != 64:
            output += chr(chr2)

        if enc4 != 64:
            output += chr(chr3)
    return output


def encode_string(to_enc):
    """
    Encodes an decoded string.

    :param to_enc: The string to encode.
    :return: The encoded string.
    """
    output = ""
    i = 0
    while i < len(to_enc):
        chr1 = get_char_safe(to_enc, i, ord, 0)
        i += 1
        chr2 = get_char_safe(to_enc, i, ord, 0)
        i += 1
        chr3 = get_char_safe(to_enc, i, ord, 0)
        i += 1

        enc1 = chr1 >> 2
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4)
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6)
        enc4 = chr3 & 63

        if chr2 == 0:
            enc3 = 64
            enc4 = 64
        elif chr3 == 0:
            enc4 = 64

        output += keyStr[enc1] + keyStr[enc2] + keyStr[enc3] + keyStr[enc4]
    return output

